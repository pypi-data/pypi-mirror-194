# Installation and Upgrade

There are several ways to install the software. The application
requires python3.

To avoid interference with the other packages, it is recommended to
use virtual environments, as described below.

We recommend to install the software using automatic installation
scripts provided for Linux/Mac and Windows.

## Releases

All releases are listed at
[Releases](https://gitlab.com/iocbio/kinetics/-/releases). Releases are
distributed as executable (for Windows) and through The Python Package
Index (PyPI). Due to numerous issues encountered while distributing
through Anaconda, we discontinued Anaconda support.

## Linux/Mac

To use automatic installation script for Linux/Mac make first sure that you have
latest `pip` installed by running:

```
python3 -m pip install --user --upgrade pip
```

Then open terminal and go to folder where you like to install the program.
Then run following command:

```
curl https://gitlab.com/iocbio/kinetics/-/raw/master/install.sh | bash
```

or

```
wget -qO - https://gitlab.com/iocbio/kinetics/-/raw/master/install.sh | bash
```
and run by
```
iocbio-kinetics/bin/iocbio-kinetics
```

## Windows

Note that for Windows we provide also executable, see below. However,
to install IOCBIO Kinetics software using automatic installation script
make sure that you have Python installed. More information about
installing Python in Windows see [Python for
Beginners](https://docs.microsoft.com/en-us/windows/python/beginners).
In addition, install Microsoft Visual C++ Redistributable for Visual
Studio 2015, 2017 and 2019. Respective installer can be found
[here](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-160).

When Python is installed open PowerShell and make first sure that
[Get-ExecutionPolicy](https://go.microsoft.com/fwlink/?LinkID=135170)
is not Restricted. We suggest using `Bypass` to bypass the policy to
get things installed or `AllSigned` for quite a bit more
security. First, run `Get-ExecutionPolicy` in PowerShell. In case, it
returns `Restricted`, then run `Set-ExecutionPolicy AllSigned` or
`Set-ExecutionPolicy Bypass -Scope Process`.  When this is all set you
can install the program by running following command:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://gitlab.com/iocbio/kinetics/-/raw/master/install.ps1'))
```

## pip

To be able to install PySide6 using pip, you have to use python3.5 or
higher. If not available in the system, you can replace `pip3` command
below with `python3 -m pip`.

To install published version, run

```
pip3 install --user iocbio.kinetics
```
This will install all dependencies and it is expected to add a command `iocbio-kinetics` into your `PATH`. 
If the command is missing after installation, check whether the default location
of `pip3` installation is in your path. For Linux, it should be `~/.local/bin`.

To install, use the Git repository directly, for HTTPS users:
```
pip3 install --user git+https://gitlab.com/iocbio/kinetics
```
and for SSH users:
```
python3 -m pip install --user git+ssh://git@gitlab.com/iocbio/kinetics.git
```


For development, use

```
pip3 install --user -e .
```

in the source directory. To install the current version from the source, use

```
pip3 install --user .
```

Note that `--user` is recommended to avoid messing up the system
packages.

For upgrade, add `--upgrade` after install keyword. For example,
```
pip3 install --upgrade --user git+https://gitlab.com/iocbio/kinetics
```
or
```
python3 -m pip install --upgrade --user git+ssh://git@gitlab.com/iocbio/kinetics.git
```


## pip with virtual environment

Sometimes packages for different applications can cause
incompatibilities. To avoid it, you could use virtual environment for
the software installation. To create virtual python environment, run

```
python -m venv iocbio-kinetics
```

This will create folder `iocbio-kinetics` and install scripts, such as
`pip`, into it. To use the environment, call `pip` from that folder
and install iocbio-kinetics into it

```
iocbio-kinetics/bin/pip install iocbio.kinetics
```
and run by
```
iocbio-kinetics/bin/iocbio-kinetics
```


## Windows ZIP binary

Starting from 1.1.1 release, MS Windows executable is provided in the
form of ZIP file. This allows to install and use the program quickly
as all the required packages are included in the provided ZIP.

To install, download the ZIP package from the link provided in the
corresponding [release
notes](https://gitlab.com/iocbio/kinetics/-/releases). Unpack the ZIP
file which would result in folder `Kinetics`. You could place this
folder as you see fit on your PC. To start IOCBIO Kinetics, enter the
folder and start `kinetics.bat` by double clicking on it.

On the first start, after connecting to the database, you would need
to enter "Settings". If you use your own modules, the path to them
will have to be specified as well.


## Use with R

If `iocbio-banova` is used, some additional packges are needed. Install R and the following packages in R:

```
install.packages(c("tidyverse", "BayesFactor", "formula.tools", "ggplot2"))
```

In addition, you will need to install `rpy2` Python package by using
`pip`.