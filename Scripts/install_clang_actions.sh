#!/bin/bash

set -e
pip3 install clint
sudo apt install -fy cppcheck clang-format-8
if [ ! -f /usr/bin/clang-format ]; then
    sudo ln -s /usr/bin/clang-format-8 /usr/bin/clang-format
fi