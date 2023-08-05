# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irv_autopkg_client',
 'irv_autopkg_client.api',
 'irv_autopkg_client.api.boundaries',
 'irv_autopkg_client.api.jobs',
 'irv_autopkg_client.api.packages',
 'irv_autopkg_client.api.probes',
 'irv_autopkg_client.api.processors',
 'irv_autopkg_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'httpx>=0.15.4,<0.24.0', 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'irv-autopkg-client',
    'version': '0.2.0',
    'description': 'A client library for accessing the IRV Autopackage API',
    'long_description': '# irv-autopkg-client\nA client library for accessing IRV Autopackage API\n\n## Usage\nFirst, create a client:\n\n```python\nfrom irv_autopkg_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom irv_autopkg_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")\n```\n\nNow call your endpoint and use the models:\n\n```python\n# which countries have already had some data generated?\n\nfrom irv_autopkg_client.api.packages import get_packages_v1_packages_get as get_packages\n\nresponse = get_packages.sync(client=client)\nfor pkg in response:\n    print(pkg.boundary_name, pkg.uri)\n```\n\nAnother example:\n```python\n# which data processors can we deploy against some country boundary?\n\nfrom irv_autopkg_client.api.processors import get_processors_v1_processors_get as get_processors\n\nresponse = get_processors.sync(client=client)\nfor p in response:\n    for v in p.versions:\n        print(v.processor.name)\n        print(f"  {v.processor.description}\\n")\n```\n\nBy default, when you\'re calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    token="SuperSecretToken",\n    verify_ssl="/path/to/certificate_bundle.pem",\n)\n```\n\nYou can also disable certificate validation altogether, but beware that **this is a security risk**.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    token="SuperSecretToken",\n    verify_ssl=False\n)\n```\n\nThere are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info.\n\nThings to know:\n- Every path/method combo becomes a Python module with four functions:\n - `sync`: Blocking request that returns parsed data (if successful) or `None`\n - `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n - `asyncio`: Like `sync` but async instead of blocking\n - `asyncio_detailed`: Like `sync_detailed` but async instead of blocking\n\n- All path/query params, and bodies become method arguments.\n- If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n- Any endpoint which did not have a tag will be in `irv_autopkg_client.api.default`\n\n## Building / publishing this Client\n\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n- Update the metadata in pyproject.toml (e.g. authors, version)\n- Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n- If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n- If that project is not using Poetry:\n - Build a wheel with `poetry build -f wheel`\n - Install that wheel from the other project `pip install <path-to-wheel>`\n',
    'author': 'Fred Thomas',
    'author_email': 'fred.thomas@eci.ox.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
