# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylacus']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

extras_require = \
{'docs': ['Sphinx>=6.1.3,<7.0.0']}

entry_points = \
{'console_scripts': ['pylacus = pylacus:main']}

setup_kwargs = {
    'name': 'pylacus',
    'version': '1.3.0',
    'description': 'Python CLI and module for lacus',
    'long_description': '# Python client and module for Lacus\n\nUse this module to interact with a [Lacus](https://github.com/ail-project/lacus) instance.\n\n## Installation\n\n```bash\npip install pylacus\n```\n\n## Usage\n\n### Command line\n\nYou can use the `pylacus` command:\n\n```bash\n$ pylacus -h\nusage: pylacus [-h] --url-instance URL_INSTANCE [--redis_up] {enqueue,status,result} ...\n\nQuery a Lacus instance.\n\npositional arguments:\n  {enqueue,status,result}\n                        Available commands\n    enqueue             Enqueue a url for capture\n    status              Get status of a capture\n    result              Get result of a capture.\n\noptions:\n  -h, --help            show this help message and exit\n  --url-instance URL_INSTANCE\n                        URL of the instance.\n  --redis_up            Check if redis is up.\n\n```\n\n### Library\n\nSee [API Reference](https://pylacus.readthedocs.io/en/latest/api_reference.html)\n\n# Example\n\n## Enqueue\n\n```python\n\nfrom redis import Redis\nfrom lacuscore import LacusCore\n\nredis = Redis()\nlacus = lacus = PyLacus("http://127.0.0.1:7100")\nuuid = lacus.enqueue(\'google.fr\')\n```\n\n## Status of a capture\n\n```python\nstatus = lacus.get_capture_status(uuid)\n```\n\n## Capture result\n\n```python\nresult = lacus.get_capture(uuid)\n```\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ail-project/PyLacus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
