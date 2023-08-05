# serverlla
[![Build Status](https://img.shields.io/github/stars/dylanmeca/serverlla.svg)](https://github.com/dylanmeca/serverlla)
[![License](https://img.shields.io/github/license/dylanmeca/serverlla.svg)](https://github.com/dylanmeca/serverlla/blob/main/LICENSE)
[![dylanmeca](https://img.shields.io/badge/author-dylanmeca-green.svg)](https://github.com/dylanmeca)
[![bug_report](https://img.shields.io/badge/bug-report-red.svg)](https://github.com/dylanmeca/serverlla/blob/main/.github/ISSUE_TEMPLATE/bug_report.md)
[![security_policy](https://img.shields.io/badge/security-policy-cyan.svg)](https://github.com/dylanmeca/serverlla/blob/main/.github/SECURITY.md)
[![Python](https://img.shields.io/badge/language-Python%20-yellow.svg)](https://www.python.org)

Configure your linux server and check for vulnerabilities with serverlla.

Serverlla has a menu with options and allows you to configure your server through that menu but you can also import the adminserver module in another file.

## Pre-requirements

The requirements to use the system is to have the following python modules installed:

```
colorama
requests
```

The apt packages that you must have installed are:

```
curl
wget
net-tools 
strace 
iftop 
lsof 
chkrootkit 
inxi 
lshw 
git 
python3 
python3-pip 
build-essential 
libssl-dev 
libffi-dev 
python3-dev 
```

## Installation

To install serverlla on linux run these commands on your Linux Terminal.

```shell

pip3 install serverlla

```

Once done, it begins to install.

to start serverlla you just have to put the ``` serverlla ``` command in the terminal.

Ready

## Usage:

To use the serverlla command you just have to put the ```serverlla``` command, and once that is done the system menu will be loaded.

## Custom script

If you want to create your own menu and your own code using the adminserver module you must do the following:

```python 

import adminserver as server

server.systeminfo () # Shows you system information
server.verifylogin () # Check who logged in
server.addnewuser () # Add new users

# Removing information from my website
link = "127.0.0.1"
server.scanweb (link) # Get information from a website

```

## Authors

* **Dylan Meca** - *Initial Work* - [dylanmeca](https://github.com/dylanmeca)

You can also look at the list of all [contributors](https://github.com/dylanmeca/serverlla/contributors) who have participated in this project.


## Contributing

Please read [CONTRIBUTING.md](https://github.com/dylanmeca/serverlla/blob/main/.github/CONTRIBUTING.md) for details of our code of conduct, and the process for submitting pull requests.

## License

The license for this project is [MIT](https://github.com/dylanmeca/serverlla/blob/main/LICENSE)
