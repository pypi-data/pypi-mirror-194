#!/usr/bin/bash

#
# This script installs IOCBio kinetics program to python virtual environment iocbio-kinetics
#

set -e
RNAME=iocbio-kinetics_requirements.txt
python3 -m venv iocbio-kinetics
if command -v wget &> /dev/null
then
  wget -q -O $RNAME https://gitlab.com/iocbio/kinetics/-/raw/master/requirements.txt
else
  curl https://gitlab.com/iocbio/kinetics/-/raw/master/requirements.txt --output $RNAME
fi
iocbio-kinetics/bin/pip3 install -r $RNAME
rm $RNAME
# iocbio-kinetics/bin/pip3 install git+https://gitlab.com/iocbio/kinetics
iocbio-kinetics/bin/pip3 install iocbio.kinetics

echo Start the program by running iocbio-kinetics/bin/iocbio-kinetics
