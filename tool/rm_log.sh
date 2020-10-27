#!/bin/bash

find /home/xcl/centos_shizhan/spider/beiyouluntan/log/ -name '*.log' -atime +10 -exec rm -f {} \;

