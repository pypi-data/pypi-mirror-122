# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nemo_text_processing.inverse_text_normalization.de.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    delete_extra_space,
    delete_space,
)
from nemo_text_processing.inverse_text_normalization.de.utils import get_abs_path

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


def get_quantity(decimal: 'pynini.FstLike', cardinal_up_to_hundred: 'pynini.FstLike') -> 'pynini.FstLike':
    """
    Returns FST that transforms either a cardinal or decimal followed by a quantity into a numeral,
    e.g. eine million -> integer_part: "1" quantity: "million"
    e.g. eins komma vier millionen -> integer_part: "1" fractional_part: "4" quantity: "millionen"

    Args: 
        decimal: decimal FST
        cardinal_up_to_hundred: cardinal FST
    """
    numbers = cardinal_up_to_hundred @ (
        pynutil.delete(pynini.closure("0")) + pynini.difference(NEMO_DIGIT, "0") + pynini.closure(NEMO_DIGIT)
    )
    suffix = pynini.union(
        "million",
        "millionen",
        "milliarde",
        "milliarden",
        "billion",
        "billionen",
        "billiarde",
        "billiarden",
        "trillion",
        "trillionen",
        "trilliarde",
        "trilliarden",
    )
    res = (
        pynutil.insert("integer_part: \"")
        + numbers
        + pynutil.insert("\"")
        + delete_extra_space
        + pynutil.insert("quantity: \"")
        + suffix
        + pynutil.insert("\"")
    )
    res |= decimal + delete_extra_space + pynutil.insert("quantity: \"") + suffix + pynutil.insert("\"")
    return res


class DecimalFst(GraphFst):
    """
    Finite state transducer for classifying decimal
        e.g. minus elf komma zwei null null sechs billionen -> decimal { negative: "true" integer_part: "11"  fractional_part: "2006" quantity: "billionen" }
        e.g. eine billion -> decimal { integer_part: "1" quantity: "billion" }
    Args:
        cardinal: CardinalFst
    """

    def __init__(self, cardinal: GraphFst):
        super().__init__(name="decimal", kind="classify")

        cardinal_graph = cardinal.graph_no_exception

        graph_decimal = pynini.string_file(get_abs_path("data/numbers/digit.tsv"))
        graph_decimal |= pynini.string_file(get_abs_path("data/numbers/zero.tsv")) | pynini.cross("null", "0")

        graph_decimal = pynini.closure(graph_decimal + delete_space) + graph_decimal
        self.graph = graph_decimal

        point = pynutil.delete("komma")

        optional_graph_negative = pynini.closure(
            pynutil.insert("negative: ") + pynini.cross("minus", "\"true\"") + delete_extra_space, 0, 1
        )

        graph_fractional = pynutil.insert("fractional_part: \"") + graph_decimal + pynutil.insert("\"")
        graph_integer = pynutil.insert("integer_part: \"") + cardinal_graph + pynutil.insert("\"")
        final_graph_wo_sign = graph_integer + delete_extra_space + point + delete_extra_space + graph_fractional
        final_graph = optional_graph_negative + final_graph_wo_sign

        self.final_graph_wo_negative = (
            final_graph_wo_sign
            | get_quantity(final_graph_wo_sign, cardinal.graph_hundred_component_at_least_one_none_zero_digit)
        ).optimize()
        final_graph |= optional_graph_negative + get_quantity(
            final_graph_wo_sign, cardinal.graph_hundred_component_at_least_one_none_zero_digit
        )
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
