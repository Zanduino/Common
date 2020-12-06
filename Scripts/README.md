# Shell Scripts
All Shell scripts are stored in this directory

## doxy_gen_and_deploy.sh
Script cloned from[Adafruit CI](https://github.com/adafruit/ci-arduino) and slightly modified which will generate
[doxygen](https://www.doxygen.nl/index.html) style html documentation and deploy it to the appropriate gh-pages url

## install_arduino_cli.sh
Script as defined by [Arduino CLI](https://github.com/arduino/arduino-cli) to install the CLI in a runner so that
compiles can be done on the command line.

## install_clang_actions.sh
Script to load the [clang-format](https://clang.llvm.org/docs/ClangFormat.html) package to the runner and also to copy the default .clang-format file to the project
root directory if there is no file there.
