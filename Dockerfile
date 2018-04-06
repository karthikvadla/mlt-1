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

FROM ubuntu:16.04

# separately install software properties for adding apt-repo; then 1 update is needed rather than 2
RUN apt-get update && apt-get install -yq --no-install-recommends --fix-missing \
    apt-transport-https \
    ca-certificates \
    curl \
    git \
    jq \
    make \
    netcat \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    python-wheel \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -yq --no-install-recommends --fix-missing \
    docker-ce && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

# install ksonnet + kubeflow so we can support TFJob

COPY ./resources/config.yaml /root/.kube/config

ENV NAMESPACE kubeflow
ENV VERSION v0.1.0-rc.4
ENV APP_NAME kubeflow
ENV KUBECONFIG /root/.kube/config
# workaround for https://github.com/ksonnet/ksonnet/issues/298
ENV USER root

# pull ksonnet from web
RUN curl -LO https://github.com/ksonnet/ksonnet/releases/download/v0.9.2/ks_0.9.2_linux_amd64.tar.gz
RUN tar -xvf ks_0.9.2_linux_amd64.tar.gz
RUN mv ./ks_0.9.2_linux_amd64/ks /usr/local/bin/ks

# create basic ks app
RUN ks init $APP_NAME
WORKDIR $APP_NAME
RUN ks env set default --namespace $NAMESPACE

# install kubeflow components for TFJob support
RUN ks registry add kubeflow github.com/kubeflow/kubeflow/tree/$VERSION/kubeflow
RUN ks pkg install kubeflow/core@$VERSION
RUN ks pkg install kubeflow/tf-job@$VERSION
RUN ks generate kubeflow-core kubeflow-core

ADD . /usr/share/mlt

WORKDIR /usr/share/mlt
# need to clean so as to not get conftest importmismatch error
RUN make clean

RUN git config --global user.email "test@example.com"
RUN git config --global user.name "Test Docker User"
