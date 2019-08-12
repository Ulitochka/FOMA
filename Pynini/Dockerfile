FROM ubuntu:xenial
MAINTAINER Martin Jansche <mjansche@google.com>

#ADD goog_af_unison_wav_22k.tar /usr/local/src/

RUN apt-get update && apt-get install -y \
      automake \
      bc \
      curl \
      g++ \
      git \
      libc-dev \
      libreadline-dev \
      libtool \
      make \
      ncurses-dev \
      nvi \
      pkg-config \
      python \
      python-dev \
      python-setuptools \
      unzip \
      wavpack \
      wget \
      zip \
      zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LC_ALL C.UTF-8
ENV OPENFST openfst-1.5.2
ENV THRAX thrax-1.2.2

# Fetch, build, and install the re2 regular expression package
WORKDIR /usr/local/src
RUN git clone https://github.com/google/re2.git
WORKDIR /usr/local/src/re2
RUN git reset --hard 4744450c4880b9445c57d9224495f0e8e29f1c4c && \
    make && make install && make distclean && ldconfig

# Fetch, build, and install the OpenFst Library
WORKDIR /usr/local/src
RUN curl -L http://openfst.org/twiki/pub/FST/FstDownload/$OPENFST.tar.gz | \
    tar xz --no-same-owner --no-same-permissions
WORKDIR /usr/local/src/$OPENFST
RUN ./configure \
      --enable-bin \
      --enable-far \
      --enable-mpdt \
      --enable-ngram-fsts \
      --enable-pdt \
      --enable-python \
    && make -j 7 && make install && make distclean && ldconfig
ENV LD_LIBRARY_PATH /usr/local/lib/fst:$LD_LIBRARY_PATH

# Fetch, build, and install Pynini
WORKDIR /usr/local/src
RUN curl -L http://openfst.org/twiki/pub/GRM/PyniniDownload/pynini-0.9.tar.gz | \
    tar xz --no-same-owner --no-same-permissions
WORKDIR /usr/local/src/pynini-0.9
RUN python setup.py install && python setup.py test


WORKDIR /usr/local/src

