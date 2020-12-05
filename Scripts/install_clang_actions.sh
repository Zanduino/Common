#!/bin/bash

set -e
pip3 install clint
sudo apt install -fy cppcheck clang-format
## Copy the standard clang-format file to start directory but don't overwrite existing file
cp -n ${GITHUB_WORKSPACE}/Common/clang-format/.clang-format ${GITHUB_WORKSPACE}/.clang-format
