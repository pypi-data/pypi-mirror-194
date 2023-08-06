# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_network_backup',
 'nornir_network_backup.config',
 'nornir_network_backup.models',
 'nornir_network_backup.nornir',
 'nornir_network_backup.nornir.plugins',
 'nornir_network_backup.nornir.plugins.inventory',
 'nornir_network_backup.nornir.plugins.processors',
 'nornir_network_backup.nornir.tasks',
 'nornir_network_backup.utils']

package_data = \
{'': ['*']}

install_requires = \
['archive-rotator>=0.2.1,<0.3.0',
 'click>=8.1.3,<9.0.0',
 'nornir-inspect>=1.0.3,<2.0.0',
 'nornir-netmiko>=0.2.0,<0.3.0',
 'nornir-salt>=0.18.0,<0.19.0',
 'nornir-task-duration>=0.0.1a0,<0.0.2',
 'nornir-utils>=0.2.0,<0.3.0',
 'nornir>=3.3.0,<4.0.0',
 'prettytable>=3.6.0,<4.0.0',
 'pydantic>=1.10.2',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['nnb = nornir_network_backup.cli:base'],
 'nornir.plugins.inventory': ['NMAPInventory = '
                              'nornir_network_backup.nornir.plugins.inventory.nmap_discovery:NMAPDiscoveryInventory'],
 'nornir.plugins.processors': ['BackupReporter = '
                               'nornir_network_backup.nornir.plugins.processors.backup_reporter:BackupReporter']}

setup_kwargs = {
    'name': 'nornir-network-backup',
    'version': '0.1.2a1',
    'description': '',
    'long_description': '# nornir-network-backup\n\n> This is a beta version. Extra options and documentation will follow soon !\n\nThis python library installs the `nnb` command which will generate configuration backups of network equipment via SSH (routers, switches, ..). This tool will replace `RANCID` which - surprisingly - still is commonly being used.\n\nThis tool uses the `Nornir` framework and connects to network devices using the `Netmiko` library.\n\nFeatures:\n\n- Uses the Nornir framework and expects the same files as nornir (config.yaml, hosts.yaml, groups.yaml)\n- Generates backup config files for each device (ex. show running-config)\n- Includes "meta" data on top of each backup config (ex. hostname, serial number, hardware type, ..)\n- Takes `facts` from the devices and store them in separate files\n- Parse facts using `textfsm` and store the results as yaml\n- Define all fact commands in the nornir config files, different facts per group can be defined\n- Store the .diff file for each backup config file\n- Generate summary reports to keep track of historical backup info\n- Include reports that can give summaries based on the gathered fact data\n\n## REQUIREMENTS\n\nThe following python libraries are required:\n\n- nornir\n- nornir-utils\n- nornir-netmiko\n\n  If you want to used different Nornir runner or inventory plugins then you may need those as well.  \n  The `nornir_salt RetryRunner` plugin for example allows automatic re-tries if a connection fails.\n\n## INSTALLATION\n\nThe library can be installed as a standard python library using pip, poetry, ..\n\n```shell\npip3 install nornir_network_backup\n```\n\n## USAGE\n\nCheckout <TODO> this repo to have a complete example with all the parameters to get you started immediately. This also has Dockerfile so you can start taking backups immediately.\n\nOnce this library is installed it will allow you to start backups using the `nnb backup` command.  \nYou can then refer to a nornir group or individual nornir hosts. If the host you want to backup does not exist in the nornir inventory then you will have to specify the driver manually and it will still allow you to run the backup for the unknown host.\n\nThe following examples assume \n\nExamples:\n\n```shell\n# take a backup for 2 hosts, both hosts will be lookuped up in the nornir inventory\nnnb backup -h host1 -h 1.2.3.4 -u someuser -p somepass\n\n# take a backup for a group of hosts, the group should be defined\nnnb backup -g cisco -u someuser -p somepass\n\n# show all hosts that will backed up\nnnb backup --all --dry-run\n```\n\n\n### Credentials\n\nYou can provide credentials in different ways:\n\n- defined the nornir config files\n- as CLI argument\n- by setting environment variables NORNIR_USERNAME and NORNIR_PASSWORD\n- by running the nnb command and prepending the environment variables\n\n## Function\n\n- take the running config of 1 or more hosts and save it to a file\n  - the file will be overwritten every day\n  - optional take a diff of the previous file and save it as well\n- run "show" commands and save each output to a separate file in a facts folder\n  - files will be overwritten every time\n  - all files in a single facts folder\n  - save a file with meta data: info about the last backup time, commands executed, failed + successful commands\n  - the commands may change depending on vendor or hw type or software\n  - commands which can be parsed with textfsm will be saved as YAML, if they cannot be parsed then it will be .config text files\n- it should be possible to run the backup file for a single host\n- or run agains a complete file\n- generate an overall report with:\n  - last run time\n  - hosts succeeded\n  - hosts failed\n  - hosts skipped\n\n## Output folder structure\n\n```text\n|- backup folder\n|  |-- facts folder\n|  |-- reports folder  \n```\n\n## Commands\n\n```shell\nnnb backup\nnnb backup-single-host\n```\n\n## Usage\n\n```shell\npoetry run nnb backup-single-host\n```\n\n## Environment Variables\n\nUsed by nornir_utils.plugins.inventory.load_credentials transform function, in case username + password are not defined by CLI\n\nNORNIR_USERNAME\n\nNORNIR_PASSWORD\n\n## TEXTFSM\n\nFacts command output can be parsed by NTC Textfsm. It depends on the configuration settings if Textfsm parsing is done.  \nThe path to the NTC textfsm templates should be valid and include the `index` file. If Textfsm is enabled and no `templates_folder` path is provided then it\'s expected that the environment variable `NTC_TEMPLATES_DIR` is set.\n\n```python\nuser_defined:\n  textfsm:\n    enabled: True\n    templates_folder: /home/mwallraf/ntc-templates/ntc_templates/templates/\n```\n\nOptions:\n\n  **enabled**: Use textfsm or not\n\n  **templates_folder**: path to the NTC textfsm templates, this should be a folder containing an index file. If the folder is not set then the environment variable NTC_TEMPLATES_DIR should exist and have a valid path.\n\n\n\n## CAVEATS\nSometimes fact commands may fail and netmiko may generate unexpected timeouts. In that case you can make sure that certain commands are never executed for device groups by prepending the command with a ^ (carret).\n\nExample:\n\npbxplug:\n  data:\n    cmd_facts:\n      - show voice voice-port all\n      - show isdn active\n      - show voice voice-port pri all\n      - show voice voice-port pri all reset\n      - ^show cellular equipment\n      - ^show cellular network\n\n\n',
    'author': 'mwallraf',
    'author_email': 'maarten.wallraf@orange.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
