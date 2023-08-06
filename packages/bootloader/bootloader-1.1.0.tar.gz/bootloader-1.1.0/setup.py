# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bootloader',
 'bootloader.commands',
 'bootloader.console',
 'bootloader.exceptions',
 'bootloader.utilities']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.44,<2.0.0',
 'cleo>=2.0.1,<3.0.0',
 'flexsea>=10.0.0,<11.0.0',
 'pyserial>=3.5,<4.0',
 'semantic-version>=2.10.0,<3.0.0']

entry_points = \
{'console_scripts': ['bootload = bootloader.console.main:main']}

setup_kwargs = {
    'name': 'bootloader',
    'version': '1.1.0',
    'description': 'A tool for loading firmware onto Dephy devices.',
    'long_description': '# Dephy Bootloader\n\nThis is a tool for loading firmware onto Dephy\'s devices.\n\n## AWS Keys\n\n`flexsea` requires a pre-compiled C library in order to communicate with your device.\nThese libraries are hosted in a public AWS S3 bucket called `dephy-public-binaries`. You\ncan use the `list` command to view the available versions (see below).\n\nAdditionally, you will need a firmware file (or files) to put on your device. These\nfiles are hosted in a private AWS S3 bucket. You should have received access keys as\na part of your purchase. If you did not, please contact `support@dephy.com`.\n\nOnce you receive your keys, you\'ll need to store them in a credentials file to be read\nby `boto3` (the Python module for interacting with S3).\n\n```bash\nmkdir ~/.aws\ntouch ~/.aws/credentials # Note that there is no extension!\n```\n\nEdit the credentials file to contain the following:\n\n```bash\n[default]\naws_access_key_id=<YOUR ACCES KEY ID HERE>\naws_secret_access_key=<YOUR SECRET ACCESS KEY HERE>\n\n[dephy]\naws_access_key_id=<YOUR ACCES KEY ID HERE>\naws_secret_access_key=<YOUR SECRET ACCESS KEY HERE>\n```\n\n**NOTE**: If you already have an S3 account, you\'ll want to put those keys under `default`\nand the Dephy keys under `dephy`. If your Dephy access keys are the only ones you have,\nyou\'ll want to put the same keys in both sections. `boto3` will fail if it does not\nfind a `default` section, but the bootloader explicitly looks for a `dephy` section in\ncase you have other keys.\n\n## Installation\n\nIt is **highly recommended**, but not required, that you install `flexsea` in a virtual\nenvironment. This helps keep your python and associated packages sandboxed from the\nrest of your system and, potentially, other versions of the same packages required by\n`flexsea`.\n\nYou can create a virtual environment via (these commands are for Linux. See the **NOTE**\nbelow for Windows):\n\n```bash\nmkdir ~/.venvs\npython3 -m venv ~/.venvs/dephy\n```\n\nActivate the virtual environment with:\n\n```bash\nsource ~/.venvs/dephy/bin/activate\n```\n\n**NOTE**: If you\'re on Windows, the activation command is: `source ~/.venvs/dephy/Scripts/activate`.\nAdditionally, replace `python3` with `python`.\n\n\n### From Source\n\nTo install from source:\n\n```bash\ngit clone https://github.com/DephyInc/boot-loader.git\ncd boot-loader/\ngit checkout main # Or whichever branch you\'re interested in\npython3 -m pip install .\n```\n\n\n### From PyPI\n\n```bash\npython3 -m pip install dephy-bootloader\n```\n\n\n## Usage\n\nThis package provides the `bootload` command-line tool. To see the available commands,\nsimply run `bootload --help`. Additionally, each subcommand has a `--help` option\nthat will give you more information on its usage.\n\nThe main commands of interest are:  `microcontroller`, `bt121`, `xbee`, and `list`.\n\n### Microcontroller\n\nThe `microcontroller` command is used for updating the firmware on Manage, Execute,\nRegulate, and Habsolute. The usage pattern is:\n\n```bash\nbootload microcontroller <target> [options]\n```\n\n`target` is the microcontroller you want to bootload. It can be:\n    * `mn`\n    * `ex`\n    * `re`\n    * `habs`\n\nThe available options are:\n    * `--from` : The semantic version string of the firmware currently on the device. This is not required for devices running version "10.0.0" or higher. If not given, but needed, the bootloader will prompt you for this information.\n    * `--to` : The semantic version string of the firmware you\'d like to bootload onto the device. If not given, the bootloader will prompt you to enter this information.\n    * `--hardware` : The version of the device\'s rigid board. This is not needed for devices running version "10.0.0" or higher. If not given, but needed, the bootloader will prompt you for this information.\n    * `--port` : The name of the serial port the device is connected to, e.g., "COM3" or "/dev/ttyACM0". If this is not given, the bootloader will attempt to find the device automatically.\n    * `--file` : If you\'d like to manually specify the firmware file to bootload, this is the option for you. If the file is not found locally in the `~/.dephy/bootloader/firmware` directory, then the `dephy-firmware` bucket on S3 will be searched and the file downloaded, if found.\n    * `--device` : The name of the device being bootloaded, e.g., "actpack" or "eb60". This is not needed if the device is running version "10.0.0" or higher. If not given, but needed, the bootloader will prompt you for this information.\n    * `--side` : When bootloading "Mn" for a device with chirality, this allows you to specify either "left" or "right". This is not needed if the device is running version "10.0.0" or higher. If not given, but needed, the bootloader will prompt you for this information.\n    * `--baudRate` : Allows you to specify the baud rate used for communicating with the device. This is only needed if the required baud rate is different than the default value of `230400`.\n\nThe bootloader will check to make sure that you have all of the required tools needed to update the firmware. If you do not, then it will download them for you.\n\n#### Examples\nThe goal is to have the command "read" fluidly. To that end, in order to bootload Regulate on an actpack from version 7.2.0 to version 9.1.0, we would do\n\n```bash\nbootload microcontroller re --from 7.2.0 --to 9.1.0 --hardware 4.1B --device actpack\n```\n\n\n### List\n\nThe `list` command is used to display information about what firmware is available to be bootloaded. The usage is:\n\n```bash\nbootload list [options]\n```\n\nThe available options are:\n    * `--devices` : Displays the types of devices that can be bootloaded\n    * `--hardware` : Displays the rigid board versions that can be bootloaded\n    * `--versions` : Displays the firmware versions available to be bootloaded\n\nIf no options are given, then the available devices, hardware, and versions are all shown.\n',
    'author': 'Jared',
    'author_email': 'jcoughlin@dephy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11.0rc1,<4.0.0',
}


setup(**setup_kwargs)
