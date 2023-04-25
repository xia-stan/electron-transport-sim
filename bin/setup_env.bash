#!/usr/bin/env bash

python3 -m venv venv && \
source venv/bin/activate && \
pip3 install --upgrade pip setuptools wheel && \
pip3 install -r requirements.txt && \
pip3 install git+https://github.com/UTA-REST/PyGasMix.git && \
pip3 install git+https://github.com/UTA-REST/PyBoltz.git