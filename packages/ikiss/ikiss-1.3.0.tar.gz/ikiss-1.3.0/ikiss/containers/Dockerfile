#INFORMATION
#MAINTAINER Julie Orjuela
#version="1.0"
#software="base dockerfile to launch pypi packages test"
#description="contains minimal dependencies for gitlab dojo test"

FROM ubuntu:jammy
USER root

# INSTALL, Global
RUN apt update
ENV TZ=Europe/Paris
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive apt -y install keyboard-configuration git vim curl wget less locate openssh-server
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3-all-dev python3-pip python3-venv
#RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#RUN python3.9 get-pip.py

RUN apt install -y graphviz build-essential libssl-dev uuid-dev libgpgme11-dev libseccomp-dev pkg-config rsync gzip libcairo2-dev libxt-dev zlib1g-dev cmake cryptsetup
RUN apt-get -y install tzdata
RUN apt install -y squashfs-tools zip util-linux libbz2-dev liblzma-dev
#RUN dpkg-reconfigure --frontend noninteractive tzdata

# installing Singularity
RUN wget https://dl.google.com/go/go1.16.4.linux-amd64.tar.gz
RUN tar -C /usr/local -xzvf go1.16.4.linux-amd64.tar.gz
RUN rm go1.16.4.linux-amd64.tar.gz
ENV PATH=/usr/local/go/bin:$PATH

## Install Singularity itself
RUN wget https://github.com/sylabs/singularity/releases/download/v3.8.1/singularity-ce-3.8.1.tar.gz
RUN tar -xzf singularity-ce-3.8.1.tar.gz
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig/
RUN cd /singularity-ce-3.8.1 && ./mconfig -p /usr/local && make -C builddir && make -C builddir install

