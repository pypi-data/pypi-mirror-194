# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['boinc_client', 'boinc_client.clients', 'boinc_client.models']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.19.0,<4.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'boinc-client',
    'version': '1.0.0',
    'description': 'Python API for interacting with a BOINC client via RPC',
    'long_description': '# BOINC Client\n\nPython native library for interacting with a BOINC client via RPC. This library has been designed to have consistent response types.\n\n## Usage\n\n### Setup\n\n```python\nfrom boinc_client import Boinc\nfrom boinc_client.clients.rpc_client import RpcClient\n\n# Hostname or IP of the running BOINC client\nBOINC_HOSTNAME = "192.168.0.2"\n\n# Create an RPC client to connect to the BOINC socket\nrpc_client = RpcClient(hostname=BOINC_HOSTNAME)\nrpc_client.authenticate()\n\n# Create a BOINC client to interact with the RPC socket\nboinc_client = Boinc(rpc_client=rpc_client)\n```\n\n#### RPC Client options\nThe following options can be passed when creating an `RpcClient` instance\n\n| Argument   | Description                                                                | Required | Default |\n|------------|----------------------------------------------------------------------------|----------|---------|\n| `hostname` | Hostname or IP address of the BOINC client                                 | Yes      | None    |\n| `port`     | Exposed port of the BOINC client                                           | No       | 31416   |\n| `timeout`  | Seconds to wait for a successful connection to the RPC socket              | No       | 30      |\n| `password` | Password to authenticate to the BOINC client, required for most operations | No       | None    |\n\n#### Boinc options\nThe following options can be passed when creating a `Boinc` instance\n\n| Argument     | Description                        | Required | Default |\n|--------------|------------------------------------|----------|---------|\n| `rpc_client` | Instance of a configured RpcClient | Yes      | None    |\n\n### Interacting with Boinc\n\n* [Unauthorised Operations](docs/unauthorised.md)\n\n## Contributing\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies, environments and execution.\nIt also uses [Docker](https://www.docker.com/) for running integration tests\n\nInstall all dependencies:\n```bash\npoetry install\n```\nEverything should be covered by tests, this project has been put together following TDD using `pytest`\n\nCheck all the tests are executing properly:\n```bash\n# Run only the Unit tests\npoetry run pytest -m "not integration"\n\n# Run only the Integration tests\npoetry run pytest -m integration\n\n# Run all tests (recommended)\npoetry run pytest\n```\n\nOnce changes have been made, use `black` and `isort` to format all the files:\n```bash\n# Format with black\npoetry run black src/ tests/\n\n# Format with isort\npoetry run isort --profile=black src/ tests/\n```',
    'author': 'Lewis England',
    'author_email': 'lewis2004@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
