FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

ARG http_proxy=""
ENV https_proxy=$http_proxy
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Europe/Budapest /etc/localtime

RUN apt-get clean && apt-get update
RUN apt-get install -y locales
RUN mv /bin/sh /bin/sh.orig && ln -s /bin/bash /bin/sh

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN apt-get update && apt install -y poppler-utils \
                   git \
                   g++ \
                   autoconf automake libtool \
                   pkg-config \
                   libpng-dev \
                   libjpeg8-dev \
                   libtiff5-dev \
                   zlib1g-dev \
                   libwebpdemux2 libwebp-dev \
                   libopenjp2-7-dev \
                   libgif-dev \
                   libarchive-dev libcurl4-openssl-dev \
                   libleptonica-dev \
                   default-jre \
                   python3 python3-pip \
                   protobuf-compiler

ARG TESSERACT_COMMIT=24da4c7
RUN git clone https://github.com/tesseract-ocr/tesseract.git /tmp/tesseract && \
    cd /tmp/tesseract && \
    git checkout ${TESSERACT_COMMIT} && \
    bash ./autogen.sh && \
    ./configure --prefix=/tesseract && \
    make && \
    make install && \
    rm -rf /tmp/tesseract
ENV PATH=/tesseract/bin:$PATH

#ARG TESSDATA_COMMIT=4767ea9
#RUN git clone https://github.com/tesseract-ocr/tessdata.git /tmp/tessdata && \
#    cd /tmp/tessdata && \
#    git checkout ${TESSDATA_COMMIT}

ARG TESSDATA_BEST_COMMIT=e2aad9b
RUN git clone https://github.com/tesseract-ocr/tessdata_best.git /tmp/tessdata && \
    cd /tmp/tessdata && \
    git checkout ${TESSDATA_BEST_COMMIT} && \
    mkdir /tessdata && \
    mv /tmp/tessdata/hun.traineddata /tessdata && \
    mv /tmp/tessdata/eng.traineddata /tessdata && \
    mv /tmp/tessdata/osd.traineddata /tessdata && \
    rm -rf /tmp/tessdata
ENV TESSDATA_PREFIX=/tessdata

COPY ./requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /tmp/requirements.txt

COPY ./src /code/src

WORKDIR /code/src