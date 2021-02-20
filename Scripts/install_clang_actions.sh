#!/bin/bash
################################################################################
## Script to get software installed and set up for running "clang-format".    ##
## If no ".clang-format" file is present in the project root directory, then  ##
## the default file is copied there in order to always have a a correct style ##
## file to use when running the clang-format command                          ##
##                                                                            ##
## Version Date       Developer  Description                                  ##
## ======= ========== ========== ============================================ ##
## 1.0.0   2020-12-05 SV-Zanshin Initial coding                               ##
##                                                                            ##
################################################################################
set -e
pip3 install clint
##sudo apt install -fy cppcheck clang-format-10
sudo apt install -fy cppcheck clang-format-12
if [ ! -f /usr/bin/clang-format ]; then
    sudo ln -s /usr/bin/clang-format-10 /usr/bin/clang-format
fi
cp -n ${GITHUB_WORKSPACE}/Common/clang-format/.clang-format ${GITHUB_WORKSPACE}/.clang-format
