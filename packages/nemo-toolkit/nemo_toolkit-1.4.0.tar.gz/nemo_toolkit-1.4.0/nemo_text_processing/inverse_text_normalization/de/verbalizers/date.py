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
    NEMO_NOT_QUOTE,
    GraphFst,
    delete_extra_space,
    delete_space,
)

try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class DateFst(GraphFst):
    """
    Finite state transducer for verbalizing date, e.g.
        date { day: "5" month: "januar" year: "2012" preserve_order: true } -> 5 januar 2012
    """

    def __init__(self):
        super().__init__(name="date", kind="verbalize")
        month = (
            pynutil.delete("month:")
            + delete_space
            + pynutil.delete("\"")
            + pynini.closure(NEMO_NOT_QUOTE, 1)
            + pynutil.delete("\"")
        )
        day = (
            pynutil.delete("day:")
            + delete_space
            + pynutil.delete("\"")
            + pynini.closure(NEMO_NOT_QUOTE, 1)
            + pynutil.insert('.')
            + pynutil.delete("\"")
        )
        year = (
            pynutil.delete("year:")
            + delete_space
            + pynutil.delete("\"")
            + pynini.closure(NEMO_NOT_QUOTE, 1)
            + delete_space
            + pynutil.delete("\"")
        )

        # (day) month year
        graph_dmy = (
            pynini.closure(day + delete_extra_space, 0, 1) + month + pynini.closure(delete_extra_space + year, 0, 1)
        )

        optional_preserve_order = pynini.closure(
            pynutil.delete("preserve_order:") + delete_space + pynutil.delete("true") + delete_space
            | pynutil.delete("field_order:")
            + delete_space
            + pynutil.delete("\"")
            + NEMO_NOT_QUOTE
            + pynutil.delete("\"")
            + delete_space
        )

        final_graph = (year | graph_dmy) + delete_space + optional_preserve_order

        delete_tokens = self.delete_tokens(final_graph)
        self.fst = delete_tokens.optimize()
