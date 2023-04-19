# Electron Transport Simulation

This project serves to ease the installation and execution of the
[PyBoltz](https://github.com/UTA-REST/PyBoltz) package. We've found a number of issues with the
package's documented installation procedure, which we'll smooth over here. We'll also be creating
some helper scripts to ease the python installation for our team members without a ton of python
experience.

## Prerequisites

1. Linux Based system
2. Python 3.9+
2. GCC 10+

## Installation Instructions

1. From the command line execute `bash bin/setup_env.bash`.

That _should_ be it. The bash script will create the virtual environment, activate it, install
the packages, etc.