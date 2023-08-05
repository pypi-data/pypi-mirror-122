# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
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

from nemo.collections.common.tokenizers.bytelevel_tokenizers import ByteLevelTokenizer
from nemo.collections.common.tokenizers.char_tokenizer import CharTokenizer
from nemo.collections.common.tokenizers.tokenizer_spec import TokenizerSpec
from nemo.collections.common.tokenizers.word_tokenizer import WordTokenizer

# TODO @blisc: Perhaps refactor instead of import guarding
try:
    from nemo.collections.common.tokenizers.huggingface.auto_tokenizer import AutoTokenizer
    from nemo.collections.common.tokenizers.sentencepiece_tokenizer import SentencePieceTokenizer
except ModuleNotFoundError:
    from nemo.utils.exceptions import CheckInstall

    # fmt: off
    class AutoTokenizer(CheckInstall): pass
    class SentencePieceTokenizer(CheckInstall): pass
    # fmt: on
