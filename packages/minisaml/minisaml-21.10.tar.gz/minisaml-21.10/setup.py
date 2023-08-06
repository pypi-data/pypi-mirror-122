# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minisaml', 'minisaml.internal']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.4.1', 'minisignxml>=20.0', 'yarl>=1.4.2']

extras_require = \
{'docs': ['sphinx>=3.2.0,<4.0.0', 'sphinxcontrib-mermaid>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'minisaml',
    'version': '21.10',
    'description': 'Minimal SAML2 client',
    'long_description': "# MiniSAML\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![CircleCI](https://circleci.com/gh/HENNGE/minisaml.svg?style=svg)](https://circleci.com/gh/HENNGE/minisaml)\n[![Documentation Status](https://readthedocs.org/projects/minisaml/badge/?version=latest)](https://minisaml.readthedocs.io/en/latest/?badge=latest)\n\n\n\nAbsolutely minimalistic SAML 2 client. Does not support the full SAML 2 specification, on purpose.\nIt only supports requests via HTTP Redirect and responses via HTTP POST.\n\n\n## Usage\n\n\n### Create a SAML Request\n\n```python\nfrom minisaml.request import get_request_redirect_url\n\nurl = get_request_redirect_url(\n    saml_endpoint='https://your-idp.invalid/sso-endpoint/', \n    expected_audience='Your SAML Issuer', \n    acs_url='https://you.web-site.invalid/saml/acs/'\n)\n\n# This line depends on your web framework/server\nredirect_user_to_url(url)\n```\n\n### Validate and parse the SAML Response\n\n```python\nfrom minisaml.response import validate_response\n\n# This line depends on your web framework/server\nsaml_response = get_SAMLResponse_form_data_as_bytes() \n\n# Load the x509 certificate as a cryptography.x509.Certificate somehow\ncertificate = ...\n\ntry:\n    response = validate_response(data=saml_response, certificate=certificate, expected_audience='Your SAML Issuer')\nexcept:\n    handle_invalid_response_somehow()\n\n# response is a minisaml.response.Response object\n```\n",
    'author': 'Jonas Obrist',
    'author_email': 'jonas.obrist@hennge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HENNGE/minisaml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
