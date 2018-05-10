#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

import os

BASE = "/home/bduser/unet/data/"
DATA_PATH = "/tmp/data"
OUT_PATH = "/tmp/data"
IMG_ROWS = 128
IMG_COLS = 128
RESCALE_FACTOR = 1
SLICE_BY = 5

IN_CHANNEL_NO = 1
OUT_CHANNEL_NO = 1

EPOCHS = 10

BLOCKTIME = 0
NUM_INTRA_THREADS = 50
NUM_INTER_THREADS = 2
BATCH_SIZE = 128

LEARNINGRATE = 0.0005  # 0.0005
DECAY_STEPS = 100
LR_FRACTION = 0.2
CONST_LEARNINGRATE = True

USE_UPSAMPLING = False
# True = Use upsampling; False = Use transposed convolution

MODEL_FN = "brainWholeTumor"  # Name for Mode=1
# MODEL_FN = "brainActiveTumor" #Name for Mode=2
# MODEL_FN = "brainCoreTumor" #Name for Mode=3

# Use flair to identify the entire tumor: test reaches 0.78-0.80: MODE=1
# Use T1 Post to identify the active tumor: test reaches 0.65-0.75: MODE=2
# Use T2 to identify the active core (necrosis, enhancing, non-enh):
# test reaches 0.5-0.55: MODE=3
MODE = 1


CHECKPOINT_DIRECTORY = os.environ.get("OUTPUT_PATH", "/data03/checkpoints/")
TENSORBOARD_IMAGES = 3  # How many images to display on TensorBoard
