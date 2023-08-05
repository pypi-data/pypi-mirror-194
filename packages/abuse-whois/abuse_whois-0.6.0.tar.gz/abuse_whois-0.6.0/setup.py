# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abuse_whois',
 'abuse_whois.api',
 'abuse_whois.api.endpoints',
 'abuse_whois.matchers',
 'abuse_whois.matchers.shared_hosting',
 'abuse_whois.matchers.whois',
 'abuse_whois.schemas']

package_data = \
{'': ['*'],
 'abuse_whois.matchers.shared_hosting': ['rules/*'],
 'abuse_whois.matchers.whois': ['rules/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiometer>=0.4.0,<0.5.0',
 'asyncache>=0.3.1,<0.4.0',
 'asyncer>=0.0.2,<0.0.3',
 'azuma==0.1.0',
 'cachetools>=5.3.0,<6.0.0',
 'email-validator>=1.3.1,<2.0.0',
 'fastapi>=0.92.0,<0.93.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyhumps>=3.8.0,<4.0.0',
 'tldextract>=3.4.0,<4.0.0',
 'typer>=0.7.0,<0.8.0',
 'whois-parser>=0.1.4,<0.2.0']

extras_require = \
{'api': ['gunicorn>=20.1.0,<21.0.0', 'uvicorn[standard]>=0.20.0,<0.21.0']}

entry_points = \
{'console_scripts': ['abuse_whois = abuse_whois.cli:app']}

setup_kwargs = {
    'name': 'abuse-whois',
    'version': '0.6.0',
    'description': 'Find where to report a domain for abuse',
    'long_description': '# abuse_whois\n\n[![PyPI version](https://badge.fury.io/py/abuse-whois.svg)](https://badge.fury.io/py/abuse-whois)\n[![Python CI](https://github.com/ninoseki/abuse_whois/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/abuse_whois/actions/workflows/test.yml)\n[![Coverage Status](https://coveralls.io/repos/github/ninoseki/abuse_whois/badge.svg?branch=main)](https://coveralls.io/github/ninoseki/abuse_whois?branch=main)\n\nYet another way to find where to report an abuse.\n\n![img](./images/overview.jpg)\n\nThis tool is highly inspired from the following libraries:\n\n- https://github.com/bradleyjkemp/abwhose\n- https://github.com/certsocietegenerale/abuse_finder\n\n## Requirements\n\n- Python 3.10+\n- whois\n\n## Installation\n\n```bash\npip install abuse_whois\n\n# or if you want to use built-in REST API\npip install abuse_whois[api]\n```\n\n## Usage\n\n### As a library\n\n```python\nfrom abuse_whois import get_abuse_contacts\n\nget_abuse_contacts("1.1.1.1")\nget_abuse_contacts("github.com")\nget_abuse_contacts("https://github.com")\nget_abuse_contacts("foo@example.com")\n```\n\n### As a CLI tool\n\n```bash\n$ abuse_whois 1.1.1.1 | jq .\n```\n\n### As a REST API\n\n```bash\n$ uvicorn abuse_whois.api.app:app\nINFO:     Started server process [2283]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\n\n$ http localhost:8000/api/whois/ address=https://github.com\n```\n\n### With Docker\n\n```bash\ngit clone https://github.com/ninoseki/abuse_whois\ncd abuse_whois\ndocker build . -t abuse-whois\ndocker run -i -d -p 8000:8000 abuse-whois\n```\n\n## Settings\n\nAll settings can be done via environment variables or `.env` file.\n\n| Name                                       | Type                   | Default  | Desc.                                                    |\n| ------------------------------------------ | ---------------------- | -------- | -------------------------------------------------------- |\n| WHOIS_LOOKUP_TIMEOUT                       | int                    | 10       | Timeout value for whois lookup (seconds)                 |\n| WHOIS_LOOKUP_CACHE_SIZE                    | int                    | 1024     | Cache size for whois lookup                              |\n| WHOIS_LOOKUP_CACHE_TTL                     | int                    | 3600     | Cache TTL value for whois lookup (seconds)               |\n| IP_ADDRESS_LOOKUP_TIMEOUT                  | int                    | 10       | Timeout value for IP address lookup (seconds)            |\n| IP_ADDRESS_LOOKUP_CACHE_SIZE               | int                    | 1024     | Cache size for IP address lookup                         |\n| IP_ADDRESS_LOOKUP_CACHE_TTL                | int                    | 3600     | Cache TTL value for IP address lookup (seconds)          |\n| RULE_EXTENSIONS                            | CommaSeparatedStrings  | yaml,yml | Rule file extensions                                     |\n| ADDITIONAL_WHOIS_RULE_DIRECTORIES          | CommaSeparatedStrings] |          | Additional directories contain whois rule files          |\n| ADDITIONAL_SHARED_HOSTING_RULE_DIRECTORIES | CommaSeparatedStrings] |          | Additional directories contain shared hosting rule files |\n\n## Contributions\n\n`abuse_whois` works based on a combination of static rules and a parsing result of whois response.\n\n- Rules:\n  - [Registrar and hosting provider](https://github.com/ninoseki/abuse_whois/wiki/Registrar-and-Hosting-Provider)\n  - [Shared hosting provider](https://github.com/ninoseki/abuse_whois/wiki/Shared-Hosting)\n\nPlease submit a PR (or submit a feature request) if you find something missing.\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ninoseki/abuse_whois',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
