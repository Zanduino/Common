#!/bin/bash

set -e
pip3 install clint
sudo apt install -fy cppcheck clang-format-8
if [ ! -f /usr/bin/clang-format ]; then
    sudo ln -s /usr/bin/clang-format-8 /usr/bin/clang-format
fi
## Copy the standard clang-format file to start directory but don't overwrite existing file
echo GithubWorkspace is ${GITHUB_WORKSPACE}
cp -n ${GITHUB_WORKSPACE}/Common/clang-format/.clang-format ${GITHUB_WORKSPACE}/.clang-format