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

from nemo.collections.tts.modules.degli import DegliModule
from nemo.collections.tts.modules.ed_mel2spec import EDMel2SpecModule
from nemo.collections.tts.modules.glow_tts import GlowTTSModule
from nemo.collections.tts.modules.melgan_modules import (
    MelGANDiscriminator,
    MelGANGenerator,
    MelGANMultiScaleDiscriminator,
)
from nemo.collections.tts.modules.squeezewave import SqueezeWaveModule
from nemo.collections.tts.modules.tacotron2 import Decoder as Taco2Decoder
from nemo.collections.tts.modules.tacotron2 import Encoder as Taco2Encoder
from nemo.collections.tts.modules.tacotron2 import Postnet as Taco2Postnet
from nemo.collections.tts.modules.waveglow import WaveGlowModule
