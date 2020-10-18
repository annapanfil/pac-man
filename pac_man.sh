#!/bin/bash

python3 -m venv myVenv
source myVenv/bin/activate
pip3 install -r requirements.txt
python3 -m pac_man
