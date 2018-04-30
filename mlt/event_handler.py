#
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
import time
from subprocess import call
from threading import Timer


class EventHandler(object):
    def __init__(self, callback):
        self.last_changed = time.time()
        self.dirty = False
        self.timer = None
        self.callback = callback
        self.ignore_directories = ["./.git"]
        self.ignore_files = ["./"]

    def dispatch(self, event):
        # TODO(niklas): Could be smarter with a os.path.basename(),
        #               but doing a prefix check for now.
        for directory in self.ignore_directories:
            if event.src_path.startswith(directory):
                return

        for f in self.ignore_files:
            if event.src_path == f:
                return

        is_ignored = call(["git", "check-ignore", event.src_path],
                          stdout=open(os.devnull, 'wb')) == 0
        if is_ignored:
            return

        if self.timer:
            self.timer.cancel()

        print("Detected change in {}".format(event.src_path))

        self.timer = Timer(3, lambda: self.callback())
        self.timer.start()
