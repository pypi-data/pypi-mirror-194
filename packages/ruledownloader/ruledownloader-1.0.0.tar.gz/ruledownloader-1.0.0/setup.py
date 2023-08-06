# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ruledownloader']

package_data = \
{'': ['*']}

install_requires = \
['configparser']

entry_points = \
{'console_scripts': ['rulechanges = ruledownloader.rulechanges:entry',
                     'ruledownloader = ruledownloader.ruledownloader:main']}

setup_kwargs = {
    'name': 'ruledownloader',
    'version': '1.0.0',
    'description': 'A tool for downloading and archiving Snort and Suricata rules',
    'long_description': "Rule Downloader\n===============\n\nThis is a tool to aid in the downloading and archival of Snort\nrulesets.  It also includes a tool, rulechanges.py to itemize the\nchanges from one version of a ruleset to another.\n\nConfiguration\n-------------\n\nThe ruledownloader is configured with an INI style file.  The\nconfiguration file is passed to the ruledownloader with the -c command\nline switch.  Alternatively, the ruledownloader will look for a file\nnamed ruledownloader.conf in the current directory and use that.\n\n### Example Configuration\n\n    [general]\n    \n    # The dest-dir parameter tells ruledownloader where to place the\n    # files it downloads.  Subdirectories will be created under this\n    # directory for each conifgured ruleset.\n    dest-dir = .\n    \n    # A ruleset configuration for a VRT subscription ruleset for Snort\n    # 2.9.0.4.\n    [ruleset vrt-subscription-2904]\n\n    # Set to no to skip downloading this ruleset.\n    enabled = yes\n\n    # The URL this ruleset is found at.\n    url = http://www.snort.org/sub-rules/snortrules-snapshot-2904.tar.gz/<yourOinkCodeHere>\n    \n    # Another ruleset configuration.\n    [ruleset et-open-290]\n    enabled = yes\n    url = http://rules.emergingthreats.net/open/snort-2.9.0/emerging.rules.tar.gz\n\nDirectory Structure\n-------------------\n\nWithin the configured destination directory each policy will get its\nown directory based on on the name of the policy.  That directory will\ncontained timestamped directory names based on when the ruleset was\ndownloaded.  A symlink names 'latest' will point to the most recently\ndownloader version of the ruleset.\n\n### Example\n\nGiven the et-open-290 ruleset configuration above the following\ndirectory structure will be created.\n\n    ./et-open-290/201104070917/emerging.rules.tar.gz\n    ./et-open-290/201104071531/emerging.rules.tar.gz\n    ./et-open-209/latest -> 201104070917\n\nReporting Changes\n-----------------\n\nThe rulechanges script can report the difference between an old and\nnew version of a ruleset.\n\n### Usage:\n\n    ./rulechanges.py <oldRuleset.tar.gz> <newRuleset.tar.gz>\n",
    'author': 'Jason Ish',
    'author_email': 'None',
    'maintainer': 'Paige Thompson',
    'maintainer_email': 'paige@paige.bio',
    'url': 'https://github.com/paigeadelethompson/ruledownloader',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
