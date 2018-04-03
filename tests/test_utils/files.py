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
from contextlib import contextmanager
import shutil
import tempfile


@contextmanager
def create_work_dir():
    workdir = tempfile.mkdtemp()
    try:
        yield workdir
    finally:
        # even on error we still need to remove dir when done
        # https://docs.python.org/2/library/tempfile.html#tempfile.mkdtemp
        # This is really a bug in 'shutil' as described here:
        # https://bugs.python.org/issue29699
        if os.path.exists(workdir):
            shutil.rmtree(workdir)
