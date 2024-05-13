#!/bin/bash

base_dir=$(dirname $(readlink -f $0))

docker build -t docker.nlp.nytud.hu/multitess:20230319 $base_dir