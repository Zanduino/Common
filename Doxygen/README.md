# Doxygen
Standard [doxygen](https://www.doxygen.nl/index.html) files

## Doxyfile
Common Doxygen configuration file for all projects. The following project-specific values are passed in using environment variables:

| Environment Variable | Description                     |
| -------------------- | ------------------------------- |
| $(PROJECT_NAME)      | Title of project                |
| $(PROJECT_NUMBER)    | Version number                  |
| $(PROJECT_BRIEF)     | Short project description       |
| $(PROJECT_LOGO)      | (optional) Link to project logo |