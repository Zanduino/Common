# YAML Github Workflows
All github Workflows are stored in this directory

## ci-clang-format.yml
Used to run [clang-format](https://clang.llvm.org/docs/ClangFormat.html) against all source files in the project

## ci-compile.yml
Workflow cloned from[Adafruit CI](https://github.com/adafruit/ci-arduino) and slightly modified which will compile
the source files on multiple hardware platforms

## ci-doxygen.yml
Workflow to create [doxygen](https://www.doxygen.nl/index.html) style html documentation and deploy it to the appropriate gh-pages.
