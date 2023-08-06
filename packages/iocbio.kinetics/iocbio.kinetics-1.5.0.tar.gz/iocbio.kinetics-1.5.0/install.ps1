
#
# This script installs IOCBio kinetics program to python virtual environment iocbio-kinetics
#

$rname = 'iocbio-kinetics_requirements.txt'
Invoke-WebRequest -Uri 'https://gitlab.com/iocbio/kinetics/-/raw/master/requirements.txt' -OutFile $rname

python.exe -m venv iocbio-kinetics
Write-Output "Python virtual environment for iocbio-kinetics created"
Write-Output ""

# Upgrading pip
.\iocbio-kinetics\Scripts\python.exe -m pip install --upgrade pip

.\iocbio-kinetics\Scripts\pip install pip install msvc-runtime

.\iocbio-kinetics\Scripts\pip install -r $rname
Remove-Item $rname
.\iocbio-kinetics\Scripts\pip install iocbio.kinetics

Write-Output ""
Write-Output "IOCBio-kinetics installed"
Write-Output ""
Write-Output "To run the program use following commands"
Write-Output ".\iocbio-kinetics\Scripts\Activate.ps1"
Write-Output "iocbio-kinetics.exe"
