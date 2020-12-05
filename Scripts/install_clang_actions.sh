#!/bin/bash
################################################################################
## Script to get software instaled and set up for doing "clang-format"        ##
##                                                                            ##
## Version Date       Developer  Description                                  ##
## ======= ========== ========== ============================================ ##
## 1.0.0   2020-12-05 SV-Zanshin Initial coding                               ##
##                                                                            ##
################################################################################
set -e
pip3 install clint
sudo apt install -fy cppcheck clang-format-10
if [ ! -f /usr/bin/clang-format ]; then
    sudo ln -s /usr/bin/clang-format-10 /usr/bin/clang-format
fi
################################################################################
## Copy the standard clang-format file to start directory but don't overwrite ##
## the existing file if it already exists there. This ensures that a valid    ##
## formatting file is used in any case                                        ##
################################################################################
cp -n ${GITHUB_WORKSPACE}/Common/clang-format/.clang-format ${GITHUB_WORKSPACE}/.clang-format
echo The current version of clang-format is 
clang-format --version