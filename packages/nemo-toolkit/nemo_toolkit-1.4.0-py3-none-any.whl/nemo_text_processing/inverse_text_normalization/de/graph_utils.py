# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
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

import os
import string
from pathlib import Path

from nemo_text_processing.inverse_text_normalization.de.utils import get_abs_path

try:
    import pynini
    from pynini import Far
    from pynini.examples import plurals
    from pynini.lib import byte, pynutil, utf8

    NEMO_CHAR = utf8.VALID_UTF8_CHAR

    NEMO_DIGIT = byte.DIGIT
    NEMO_LOWER = pynini.union(*string.ascii_lowercase).optimize()
    NEMO_UPPER = pynini.union(*string.ascii_uppercase).optimize()
    NEMO_ALPHA = pynini.union(NEMO_LOWER, NEMO_UPPER).optimize()
    NEMO_ALNUM = pynini.union(NEMO_DIGIT, NEMO_ALPHA).optimize()
    NEMO_HEX = pynini.union(*string.hexdigits).optimize()
    NEMO_NON_BREAKING_SPACE = u"\u00A0"
    NEMO_SPACE = " "
    NEMO_WHITE_SPACE = pynini.union(" ", "\t", "\n", "\r", u"\u00A0").optimize()
    NEMO_NOT_SPACE = pynini.difference(NEMO_CHAR, NEMO_WHITE_SPACE).optimize()
    NEMO_NOT_QUOTE = pynini.difference(NEMO_CHAR, r'"').optimize()

    NEMO_PUNCT = pynini.union(*map(pynini.escape, string.punctuation)).optimize()
    NEMO_GRAPH = pynini.union(NEMO_ALNUM, NEMO_PUNCT).optimize()

    NEMO_SIGMA = pynini.closure(NEMO_CHAR)

    delete_space = pynutil.delete(pynini.closure(NEMO_WHITE_SPACE))
    insert_space = pynutil.insert(" ")
    delete_extra_space = pynini.cross(pynini.closure(NEMO_WHITE_SPACE, 1), " ")

    suppletive = pynini.string_file(get_abs_path("data/suppletive.tsv"))
    # plural endung n/en maskuline Nomen mit den Endungen e, ent, and, ant, ist, or
    _n = NEMO_SIGMA + pynini.union("e") + pynutil.insert("n")
    _en = (
        NEMO_SIGMA
        + pynini.union("ent", "and", "ant", "ist", "or", "ion", "ik", "heit", "keit", "schaft", "tät", "ung")
        + pynutil.insert("en")
    )
    _nen = NEMO_SIGMA + pynini.union("in") + (pynutil.insert("e") | pynutil.insert("nen"))
    _fremd = NEMO_SIGMA + pynini.union("ma", "um", "us") + pynutil.insert("en")
    # maskuline Nomen mit den Endungen eur, ich, ier, ig, ling, ör
    _e = NEMO_SIGMA + pynini.union("eur", "ich", "ier", "ig", "ling", "ör") + pynutil.insert("e")
    _s = NEMO_SIGMA + pynini.union("a", "i", "o", "u", "y") + pynutil.insert("s")

    graph_plural = plurals._priority_union(
        suppletive, pynini.union(_n, _en, _nen, _fremd, _e, _s), NEMO_SIGMA
    ).optimize()

    SINGULAR_TO_PLURAL = graph_plural
    PLURAL_TO_SINGULAR = pynini.invert(graph_plural)
    TO_LOWER = pynini.union(*[pynini.cross(x, y) for x, y in zip(string.ascii_uppercase, string.ascii_lowercase)])
    TO_UPPER = pynini.invert(TO_LOWER)

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    # Create placeholders
    NEMO_CHAR = None

    NEMO_DIGIT = None
    NEMO_LOWER = None
    NEMO_UPPER = None
    NEMO_ALPHA = None
    NEMO_ALNUM = None
    NEMO_HEX = None
    NEMO_NON_BREAKING_SPACE = u"\u00A0"
    NEMO_SPACE = " "
    NEMO_WHITE_SPACE = None
    NEMO_NOT_SPACE = None
    NEMO_NOT_QUOTE = None

    NEMO_PUNCT = None
    NEMO_GRAPH = None

    NEMO_SIGMA = None

    delete_space = None
    insert_space = None
    delete_extra_space = None

    suppletive = None
    _n = None
    _en = None
    _nen = None
    _fremd = None
    _e = None
    _s = None

    graph_plural = None

    SINGULAR_TO_PLURAL = None
    PLURAL_TO_SINGULAR = None
    TO_LOWER = None
    TO_UPPER = None

    PYNINI_AVAILABLE = False


def get_plurals(fst):
    """
    Given singular returns plurals

    Args:
        fst: Fst

    Returns plurals to given singular forms
    """
    return SINGULAR_TO_PLURAL @ fst


def get_singulars(fst):
    """
    Given plural returns singulars

    Args:
        fst: Fst

    Returns singulars to given plural forms
    """
    return PLURAL_TO_SINGULAR @ fst


def convert_space(fst) -> 'pynini.FstLike':
    """
    Converts space to nonbreaking space.
    Used only in tagger grammars for transducing token values within quotes, e.g. name: "hello kitty"
    This is making transducer significantly slower, so only use when there could be potential spaces within quotes, otherwise leave it. 

    Args:
        fst: input fst

    Returns output fst where breaking spaces are converted to non breaking spaces
    """
    return fst @ pynini.cdrewrite(pynini.cross(NEMO_SPACE, NEMO_NON_BREAKING_SPACE), "", "", NEMO_SIGMA)


class GraphFst:
    """
    Base class for all grammar fsts.

    Args:
        name: name of grammar class
        kind: either 'classify' or 'verbalize'
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, name: str, kind: str, deterministic: bool = True):
        self.name = name
        self.kind = str
        self._fst = None
        self.deterministic = deterministic

        self.far_path = Path(os.path.dirname(__file__) + '/grammars/' + kind + '/' + name + '.far')
        if self.far_exist():
            self._fst = Far(self.far_path, mode="r", arc_type="standard", far_type="default").get_fst()

    def far_exist(self) -> bool:
        """
        Returns true if FAR can be loaded
        """
        return self.far_path.exists()

    @property
    def fst(self) -> 'pynini.FstLike':
        return self._fst

    @fst.setter
    def fst(self, fst):
        self._fst = fst

    def add_tokens(self, fst) -> 'pynini.FstLike':
        """
        Wraps class name around to given fst

        Args: 
            fst: input fst
        
        Returns:
            Fst: fst
        """
        return pynutil.insert(f"{self.name} {{ ") + fst + pynutil.insert(" }")

    def delete_tokens(self, fst) -> 'pynini.FstLike':
        """
        Deletes class name wrap around output of given fst

        Args:
            fst: input fst

        Returns:
            Fst: fst
        """
        res = (
            pynutil.delete(f"{self.name}")
            + delete_space
            + pynutil.delete("{")
            + delete_space
            + fst
            + delete_space
            + pynutil.delete("}")
        )
        return res @ pynini.cdrewrite(pynini.cross(u"\u00A0", " "), "", "", NEMO_SIGMA)
