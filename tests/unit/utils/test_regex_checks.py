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

import pytest

from mlt.utils.regex_checks import k8s_name_is_valid


@pytest.mark.parametrize("app_name, resource_type, is_valid", [
    ("app-name", "pod", True),
    ("app_name", "pod", False),
    ("-appname", "pod", False),
    ("1-appname", "pod", True),
    ("appname-", "pod", False),
    ("app-name-1", "pod", True),
    ("app#1", "pod", False),
    ("AppName", "pod", False),
    ("-namespace1", "namespace", True),
    ("namespace1-", "namespace", True),
    ("name_space", "namespace", False),
    ("NameSpace", "namespace", False),
    ("namespace#1", "namespace", False),
    ("x" * 254, "namespace", False),
    ("k8s-default", "default", True),
    ("-k8s-default-", "default", True),
    ("k8s_default", "default", False),
    ("K8sDefault", "default", False)
])
def test_app_name_regex(app_name, resource_type, is_valid):
    assert k8s_name_is_valid(app_name, resource_type) == is_valid
