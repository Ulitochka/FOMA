#!/usr/bin/env bash
#!/bin/sh
#
# Download and install OpenFST with contributions and all OpenGRM projects
#
# Copyright 2018-2019 Wincent Balin
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

# Specify package versions
OPENFST_VERSION=1.7.2
THRAX_VERSION=1.2.9
PYNINI_VERSION=2.0.7
SFST_VERSION=1.0.0

# Install OpenFST
wget -q -O - http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-$OPENFST_VERSION.tar.gz | tar zxvf -
cd openfst-$OPENFST_VERSION
./configure --enable-compact-fsts --enable-compress --enable-const-fsts --enable-far --enable-linear-fsts --enable-lookahead-fsts --enable-mpdt --enable-ngram-fsts --enable-pdt --enable-python --enable-special --enable-bin --enable-grm
make -j 12
make install
cd ..
# Index libraries
if [ ! -f /etc/ld.so.conf.d/openfst.conf ]
then
    echo /usr/local/lib >> /etc/ld.so.conf.d/openfst.conf
    echo /usr/local/lib/fst >> /etc/ld.so.conf.d/openfst.conf
fi
ldconfig

## Install OpenGRM Pynini
#wget -q -O - http://www.openfst.org/twiki/pub/GRM/PyniniDownload/pynini-$PYNINI_VERSION.tar.gz | tar zxvf -
#cd pynini-$PYNINI_VERSION
#sed -i '/from os import path/a from io import open' setup.py
#python3 setup.py install
#python3 setup.py test
#cd ..
#rm -rf pynini-$PYNINI_VERSION
## Index libraries
#ldconfig

# Install OpenGRM Thrax
wget -q -O - http://www.openfst.org/twiki/pub/GRM/ThraxDownload/thrax-$THRAX_VERSION.tar.gz | tar zxvf -
cd thrax-$THRAX_VERSION

apt-get install libreadline-dev
apt-get install libncurses5-dev

./configure --enable-bin --enable-readline
make -j 5  # This is because the parser compilation uses up to 3 GB
make install
cd ..
# Index libraries
ldconfig
