# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['freakble']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'asyncclick>=8.1.3.4,<9.0.0.0',
 'bleak>=0.19.5,<0.20.0',
 'prompt-toolkit>=3.0.36,<4.0.0']

extras_require = \
{'themes': ['ttkthemes>=3.2.2,<4.0.0']}

entry_points = \
{'console_scripts': ['freakble = freakble.__main__:run']}

setup_kwargs = {
    'name': 'freakble',
    'version': '0.6.0',
    'description': 'A simple tool to send messages into FreakWAN over Bluetooth low energy.',
    'long_description': '# freakble\n\nA simple tool to send messages and commands into [FreakWAN](https://github.com/antirez/freakwan)\nover Bluetooth low energy.\nIt\'s tested under Linux and Windows but it should work also on MacOS.\n\n## Installation\n\n### Using pipx\n\nThe best way to install freakble is using [pipx](https://pypa.github.io/pipx/):\n```console\n$ pipx install freakble\n```\n\nFor the GUI you can optionally install themes using:\n```console\n$ pipx install \'freakble[themes]\'\n```\n\n### Using pip\n\n*When using pip it\'s suggested to work inside a virtualenv.*\n\n```console\n$ python -m pip install freakble\n```\n\n### From source\n\nfreakble uses [Poetry](https://python-poetry.org) as dependency management and\npackaging tool, you need to install it first.\n\nThen:\n\n1. Clone this repository.\n2. From the root of the repository run:\n   ```console\n   $ poetry build\n   ```\n3. Install using pipx or pip (it\'s better to use pipx):\n   ```console\n   $ pipx install dist/freakble-0.1.0-py3-none-any.whl\n   ```\n\n## Usage\n\n```console\nUsage: freakble [OPTIONS] COMMAND [ARGS]...\n\n  A simple tool to send messages into FreakWAN.\n\nOptions:\n  --adapter TEXT  ble adapter  [default: (hci0)]\n  --help          Show this message and exit.\n\nCommands:\n  gui      Start freakble GUI.\n  repl     Start a REPL with the device.\n  scan     Scan to find BLE devices.\n  send     Send one or more words over BLE to a specific device.\n  version  Return freakble version.\n```\n\n### send\n\nThe `send` command is used to send a message to the board. You need to know the\naddress of the device.\nYou can specify the address of a device using the `--device` flag or the\nenvironment variable `FREAKBLE_DEVICE`.\n\nThe complete usage is:\n```console\nUsage: freakble send [OPTIONS] [WORDS]...\n\n  Send one or more words over BLE to a specific device.\n\nOptions:\n  --loop              send forever the message\n  --device TEXT       ble device address  [required]\n  --sleep-time FLOAT  sleep between messages sent with --loop  [default: (1\n                      sec)]\n  --timeout FLOAT     Bluetooth LE connection timeout  [default: (10 secs)]\n  --help              Show this message and exit.\n```\n\nFor example:\n\n```console\n$ freakble send --device AA:AA:AA:AA:AA:AA Hello, there!\n```\n\nwhere you have to substitute `AA:AA:AA:AA:AA:AA` with your device\'s address.\n\nThe `--loop` flag will make freakble to send continuosly the message until\n`CTRL + C` is pressed. The resend interval is defaults to 1 sec and can be\nchanged using `--sleep-time`.\n\n```console\n$ freakble send --device AA:AA:AA:AA:AA:AA --loop FREAKNET\n```\n\n![A photo of a LYLIGO TTGO LoRa v2 1.6 showing the text: you> FREAKNET in multiple lines.](extras/304f4bb6-4f51-4183-95b9-c329b9bf69ab.jpg)\n\nYou can use `FREAKBLE_DEVICE` environment variables to set the device address,\nand to not have to provide it in each commands that need a device address.\n\nFor example, using `send`, if one of your device is called `FW_vuzasu`\nyou can do:\n\n```console\n$ export FREAKBLE_DEVICE=$(freakble scan | grep FW_vuzasu | cut -d\' \' -f1)\n$ freakble send "La violenza è l\'ultimo rifugio degli incapaci. - Isaac Asimov"\n```\n\nFreakWAN supports commands starting with `!` character (see the list on\nFreakWAN README):\n\n```console\n$ freakble send \'!bat\'\nbattery 99%, 4.20 volts\n```\n\nIf you don\'t know what to say, you can always tempt the fates! :)\n```console\nfreakble send "$(fortune)"\n```\n\nPlease note that this command handle also disconnection from Bluetooth LE so it\nruns in a few seconds.\n\n### scan\n\nThe `scan` command is used to discover Bluetooth LE devices.\n\n```console\nUsage: freakble scan [OPTIONS]\n\n  Scan to find BLE devices.\n\nOptions:\n  --scan-time FLOAT  scan duration  [default: (5 secs)]\n  --help             Show this message and exit.\n```\n\nFor example:\n```\n$ freakble scan\nAB:AB:AB:AB:AB:AB (rssi:-52) FW_timatu\nAF:AF:AF:AF:AF:AF (rssi:-57) FW_vuzasu\n```\n\n### repl\n\nThe `repl` command connects to the specified device and stats an interactive\nshell with it.\nThe complete usage is:\n```\nUsage: freakble repl [OPTIONS]\n\n  Start a REPL with the device.\n\nOptions:\n  --device TEXT    ble device address  [required]\n  --timeout FLOAT  Bluetooth LE connection timeout  [default: (10 secs)]\n  --help           Show this message and exit.\n```\n\nFor example:\n\n```console\n$ export FREAKBLE_DEVICE=$(freakble scan | grep FW | cut -d\' \' -f1)\nfreakble 0.3.0a0 on linux\nConnecting to AB:AB:AB:AB:AB:AB...\nΦ]\n```\n\n`Φ]` is the freakble prompt.\n\nYou can then talk to the device remembering that commands start with `!` and\nthe text you write if it\'s not a command is sent as a message in the network.\n\nFor example, the following text is sent as a message in the network:\n```\nΦ] Hello there!\nΦ]\n```\n\nInstead commands make you able to get info or configure your FreakWAN node:\n```\nΦ] !help\nCommands: !automsg !pw !sp !cr !bw !freq !preset !ls !font !last !addkey !delkey !keys !usekey !nokey\nΦ] !bat\nbattery volts: 4.2\n```\n\nPressing `TAB` key or `!` will show the autocompletion menu.\n\nTo exit from the interactive shell use `CTRL + D` or `CTRL + C`\n\n### gui\n\nThe `gui` command starts a GUI of freakble. If you don\'t set the device address\nit will start with the following scan interface:\n\n![A screenshot of the scan inferface of the gui.](extras/gui_scan.png)\n\nafter choosing a device you can click to the connect button to get a graphical\nREPL:\n\n![A screenshot of the graphical REPL of freakble.](extras/gui_repl.png)\n\n\n## License\n\nfreakble is licensed under BSD-3-Clause license.\n',
    'author': 'Daniele Tricoli',
    'author_email': 'eriol@mornie.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eriol/freakble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
