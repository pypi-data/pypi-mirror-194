# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['helium_positioning_api']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'fastapi>=0.87.0,<0.88.0',
 'haversine>=2.7.0,<3.0.0',
 'helium-api-wrapper>=0.0.1.dev1675239484,<0.0.2',
 'joblib>=1.2.0,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytest-mock>=3.10.0,<4.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'utm>=0.7.0,<0.8.0',
 'uvicorn>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'helium-positioning-api',
    'version': '0.0.2.dev1677516387',
    'description': 'Helium Positioning API',
    'long_description': '# Helium Positioning API\n\n[![PyPI](https://img.shields.io/pypi/v/helium-positioning-api.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/helium-positioning-api.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/helium-positioning-api)][python version]\n[![License](https://img.shields.io/pypi/l/helium-positioning-api)][license]\n\n[![Read the documentation at https://helium-positioning-api.readthedocs.io/](https://img.shields.io/readthedocs/helium-positioning-api-api-api-api-api-api/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/emergotechnologies/helium-positioning-api/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/emergotechnologies/helium-positioning-api/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/helium-positioning-api/\n[status]: https://pypi.org/project/helium-positioning-api/\n[python version]: https://pypi.org/project/helium-positioning-api\n[read the docs]: https://helium-positioning-api.readthedocs.io/\n[tests]: https://github.com/emergotechnologies/helium-positioning-api/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/emergotechnologies/helium-positioning-api\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\nPrediction of the location of devices belonging to an organization in the [Helium Console](https://console.helium.com/). \nSeveral different methods and models are available.\n\n## Installation\n\n### Developer install\n\nThe following allows a user to create a developer install of the positioning api.\n\n```console\npip install -r requirements.txt\npoetry install\npoetry shell\npip install git+https://github.com/emergotechnologies/helium-api-wrapper\n```\n\n## Prerequisites\n\nBefore use, ensure that there is an `.env` file in the root directory of the repository where the `API_KEY` variable is entered (see `.env.sample`). You can generate and copy the `API_KEY` at https://console.helium.com/profile.\n\n## Usage\n\nThe service allows usage via **command line interface** or locally hosted **REST interface**.\n\n### CLI\n\n**Get Device Position**\n\n```\npython -m helium_positioning_api predict --uuid 92f23793-6647-40aa-b255-fa1d4baec75d\n```\n\nCurrently defaults to the "nearest_neighbor" model.\n\n**Advanced Requests**\n\nThe location prediction command is\n\n```\npython -m helium_positioning_api predict --uuid \'your uuid\' --model \'your model selection\'\n```\n\nSee the table below for a list of currently available models.\n\n| **Model**                         | **Position estimation explanation**                                 | **Suggested use**                                                                                                                                                             |\n| --------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| nearest_neighbor                  | Location of hotspot with the best signal                            | Purchase of at most one packet from a device (see [Packet Configurations](https://docs.helium.com/use-the-network/console/multi-packets/) for more details)                   |\n| midpoint                          | Point of equal distance from the two hotspots with the best signals | Purchase of at least two packets from a device (see [Packet Configurations](https://docs.helium.com/use-the-network/console/multi-packets/) for more details)                 |\n| linear_regression (experimental)  | Trilateration with an linear regression distance estimator          | Experimental. Purchase of at least three packets from a device (see [Packet Configurations](https://docs.helium.com/use-the-network/console/multi-packets/) for more details) |\n| gradient_boosting (experimental)  | Trilateration with a gradient boosted regression distance estimator | Experimental. Purchase of at least three packets from a device (see [Packet Configurations](https://docs.helium.com/use-the-network/console/multi-packets/) for more details) |\n\n### REST-API\n\n1. Start local REST-API (default)\n   ```\n   python -m helium_positioning_api serve\n   ```\n2. Open Browser and navigate to `127.0.0.1:8000/docs`\n3. Click on `predict_tf` path to drop down the endpoint details\n4. Click on the `Try it out` button.\n5. Fill in the `uuid` of your device and click on the button `Execute` to get an estimation using the `nearest_neighbor` model\n6. You can see the location prediction response in the `Responses` section below.\n\nThe mapping of available models to paths can be seen in the table below.\n\n| **model**         | **path**                                                            |\n| ----------------- | ------------------------------------------------------------------- |\n| nearest_neighbor  | predict_tf                                                          |\n| midpoint          | predict_mp                                                          |\n| linear_regression | predict_tl_lin                                                      |\n| gradient_boosting | predict_tl_grad                                                     |\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Helium Positioning API_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/emergotechnologies/helium-positioning-api/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/emergotechnologies/helium-positioning-api/blob/main/LICENSE\n[contributor guide]: https://github.com/emergotechnologies/helium-positioning-api/blob/main/CONTRIBUTING.md\n[command-line reference]: https://helium-positioning-api.readthedocs.io/en/latest/usage.html\n',
    'author': 'Lukas Huber',
    'author_email': 'lukas.huber@fh-kufstein.ac.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/emergotechnologies/helium-positioning-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
