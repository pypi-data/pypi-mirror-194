# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinat',
 'pyinaturalist',
 'pyinaturalist.controllers',
 'pyinaturalist.docs',
 'pyinaturalist.models',
 'pyinaturalist.v0',
 'pyinaturalist.v1',
 'pyinaturalist.v2']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2',
 'keyring>=22.3',
 'platformdirs>=2.5',
 'python-dateutil>=2.0',
 'python-forge>=18.6',
 'requests-cache>=1.0.0b0',
 'requests-ratelimiter>=0.3.2',
 'requests>=2.22',
 'rich>=10.9']

extras_require = \
{'all': ['ujson>=5.4.0,<6.0.0'],
 'docs': ['furo>=2022.9,<2023.0',
          'ipython>=7.25.0,<8.0.0',
          'linkify-it-py>=1.0.1,<2.0.0',
          'myst-parser>=0.18,<0.19',
          'nbsphinx>=0.8,<0.9',
          'sphinx>=5.2,<6.0',
          'sphinx-automodapi>=0.14,<0.15',
          'sphinx-autodoc-typehints>=1.17,<2.0',
          'sphinx-copybutton>=0.5',
          'sphinx-design>=0.2.0',
          'sphinxcontrib-apidoc>=0.3,<0.4']}

setup_kwargs = {
    'name': 'pyinaturalist',
    'version': '0.18.0',
    'description': 'iNaturalist API client for python',
    'long_description': "# pyinaturalist\n\n[![Build](https://github.com/pyinat/pyinaturalist/workflows/Build/badge.svg)](https://github.com/pyinat/pyinaturalist/actions)\n[![Codecov](https://codecov.io/gh/pyinat/pyinaturalist/branch/main/graph/badge.svg)](https://codecov.io/gh/pyinat/pyinaturalist)\n[![Documentation](https://img.shields.io/readthedocs/pyinaturalist/stable)](https://pyinaturalist.readthedocs.io)\n\n[![PyPI](https://img.shields.io/pypi/v/pyinaturalist?color=blue)](https://pypi.org/project/pyinaturalist)\n[![Conda](https://img.shields.io/conda/vn/conda-forge/pyinaturalist?color=blue)](https://anaconda.org/conda-forge/pyinaturalist)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pyinaturalist)](https://pypi.org/project/pyinaturalist)\n\n[![Run with Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pyinat/pyinaturalist/main?urlpath=lab/tree/examples)\n[![Open in VSCode](docs/images/open-in-vscode.svg)](https://open.vscode.dev/pyinat/pyinaturalist)\n\n<br/>\n\n[![](docs/images/pyinaturalist_logo_med.png)](https://pyinaturalist.readthedocs.io)\n\n# Introduction\n[**iNaturalist**](https://www.inaturalist.org) is a community science platform that helps people\nget involved in the natural world by observing and identifying the living things around them.\nCollectively, the community produces a rich source of global biodiversity data that can be valuable\nto anyone from hobbyists to scientists.\n\n**pyinaturalist** is a client for the [iNaturalist API](https://api.inaturalist.org/v1) that makes\nthese data easily accessible in the python programming language.\n\n- [Features](#features)\n- [Quickstart](#quickstart)\n- [Next Steps](#next-steps)\n- [Feedback](#feedback)\n- [Related Projects](#related-projects)\n\n## Features\n* ➡️ **Easier requests:** Simplified request formats, easy pagination, and complete request\n  parameter type annotations for better IDE integration\n* ⬅️ **Convenient responses:** Type conversions to the things you would expect in python, and an\n  optional object-oriented inteface for response data\n* 🔒 **Security:** Keyring integration for secure credential storage\n* 📗 **Docs:** Example requests, responses, scripts, and Jupyter notebooks to help get you started\n* 💚 **Responsible use:** Follows the\n  [API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices)\n  by default, so you can be nice to the iNaturalist servers and not worry about rate-limiting errors\n* 🧪 **Testing:** A dry-run testing mode to preview your requests before potentially modifying data\n\n### Supported Endpoints\nMany of the most relevant API endpoints are supported, including:\n* 📝 Annotations and observation fields\n* 🆔 Identifications\n* 💬 Messages\n* 👀 Observations (multiple formats)\n* 📷 Observation photos + sounds\n* 📊 Observation observers, identifiers, histograms, life lists, and species counts\n* 📍 Places\n* 👥 Projects\n* 🐦Species\n* 👤 Users\n\n## Quickstart\nHere are usage examples for some of the most commonly used features.\n\nFirst, install with pip:\n```bash\npip install pyinaturalist\n```\n\nThen, import the main API functions:\n```python\nfrom pyinaturalist import *\n```\n\n### Search observations\nLet's start by searching for all your own observations. There are\n[numerous fields you can search on](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.observations.html#pyinaturalist.v1.observations.create_observation), but we'll just use `user_id` for now:\n```python\n>>> observations = get_observations(user_id='my_username')\n```\n\nThe full response will be in JSON format, but we can use `pyinaturalist.pprint()` to print out a summary:\n```python\n>>> for obs in observations['results']:\n>>>    pprint(obs)\nID         Taxon                               Observed on   User     Location\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n117585709  Genus: Hyoscyamus (henbanes)        May 18, 2022  niconoe  Calvi, France\n117464920  Genus: Omophlus                     May 17, 2022  niconoe  Galéria, France\n117464393  Genus: Briza (Rattlesnake Grasses)  May 17, 2022  niconoe  Galéria, France\n...\n```\n\nYou can also get\n[observation counts by species](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.observations.html#pyinaturalist.v1.observations.get_observation_species_counts).\nOn iNaturalist.org, this information can be found on the 'Species' tab of search results.\nFor example, to get species counts of all your own research-grade observations:\n```python\n>>> counts = get_observation_species_counts(user_id='my_username', quality_grade='research')\n>>> pprint(counts)\n ID     Rank      Scientific name               Common name             Count\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n47934   species   🐛 Libellula luctuosa         Widow Skimmer           7\n48627   species   🌻 Echinacea purpurea         Purple Coneflower       6\n504060  species   🍄 Pleurotus citrinopileatus  Golden Oyster Mushroom  6\n...\n```\n\nAnother useful format is the\n[observation histogram](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.observations.html#pyinaturalist.v1.observations.get_observation_histogram),\nwhich shows the number of observations over a given interval. The default is `month_of_year`:\n```python\n>>> histogram = get_observation_histogram(user_id='my_username')\n>>> print(histogram)\n{\n    1: 8,  # January\n    2: 1,  # February\n    3: 19, # March\n    ...,   # etc.\n}\n```\n\n### Create and update observations\nTo create or modify observations, you will first need to log in.\nThis requires creating an [iNaturalist app](https://www.inaturalist.org/oauth/applications/new),\nwhich will be used to get an access token.\n```python\ntoken = get_access_token(\n    username='my_username',\n    password='my_password',\n    app_id='my_app_id',\n    app_secret='my_app_secret',\n)\n```\nSee [Authentication](https://pyinaturalist.readthedocs.io/en/latest/user_guide.html#authentication)\nfor more options including environment variables, keyrings, and password managers.\n\nNow we can [create a new observation](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.observations.html#pyinaturalist.v1.observations.create_observation):\n```python\nfrom datetime import datetime\n\nresponse = create_observation(\n    taxon_id=54327,  # Vespa Crabro\n    observed_on_string=datetime.now(),\n    time_zone='Brussels',\n    description='This is a free text comment for the observation',\n    tag_list='wasp, Belgium',\n    latitude=50.647143,\n    longitude=4.360216,\n    positional_accuracy=50,  # GPS accuracy in meters\n    access_token=token,\n    photos=['~/observations/wasp1.jpg', '~/observations/wasp2.jpg'],\n)\n\n# Save the new observation ID\nnew_observation_id = response[0]['id']\n```\n\nWe can then [update the observation](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.observations.html#pyinaturalist.v1.observations.update_observation) information, photos, or sounds:\n```python\nupdate_observation(\n    17932425,\n    access_token=token,\n    description='updated description !',\n    photos='~/observations/wasp_nest.jpg',\n    sounds='~/observations/wasp_nest.mp3',\n)\n```\n\n### Search species\nLet's say you partially remember either a genus or family name that started with **'vespi'**-something.\nThe [taxa endpoint](https://pyinaturalist.readthedocs.io/en/stable/modules/pyinaturalist.v1.taxa.html#pyinaturalist.v1.taxa.get_taxa)\ncan be used to search by name, rank, and several other criteria\n```python\n>>> response = get_taxa(q='vespi', rank=['genus', 'family'])\n```\n\nAs with observations, there is a lot of information in the response, but we'll print just a few basic details:\n```python\n>>> pprint(response)\n[52747] Family: Vespidae (Hornets, Paper Wasps, Potter Wasps, and Allies)\n[92786] Genus: Vespicula\n[84737] Genus: Vespina\n...\n```\n\n## Next Steps\nFor more information, see:\n\n* [User Guide](https://pyinaturalist.readthedocs.io/en/latest/user_guide.html):\n  introduction and general features that apply to most endpoints\n* [Endpoint Summary](https://pyinaturalist.readthedocs.io/en/latest/endpoints.html):\n  a complete list of endpoints wrapped by pyinaturalist\n* [Examples](https://pyinaturalist.readthedocs.io/en/stable/examples.html):\n  data visualizations and other examples of things to do with iNaturalist data\n* [Reference](https://pyinaturalist.readthedocs.io/en/latest/reference.html): Detailed API documentation\n* [Contributing Guide](https://pyinaturalist.readthedocs.io/en/stable/contributing.html):\n  development details for anyone interested in contributing to pyinaturalist\n* [History](https://github.com/pyinat/pyinaturalist/blob/dev/HISTORY.md):\n  details on past and current releases\n* [Issues](https://github.com/pyinat/pyinaturalist/issues): planned & proposed features\n\n## Feedback\nIf you have any problems, suggestions, or questions about pyinaturalist, please let us know!\nJust [create an issue](https://github.com/pyinat/pyinaturalist/issues/new/choose).\nAlso, **PRs are welcome!**\n\n**Note:** pyinaturalist is developed by members of the iNaturalist community, and is not endorsed by\niNaturalist.org or the California Academy of Sciences. If you have non-python-specific questions\nabout the iNaturalist API or iNaturalist in general, the\n[iNaturalist Community Forum](https://forum.inaturalist.org/) is the best place to start.\n\n## Related Projects\nOther python projects related to iNaturalist:\n\n* [naturtag](https://github.com/pyinat/naturtag): A desktop application for tagging image files with iNaturalist taxonomy & observation metadata\n* [pyinaturalist-convert](https://github.com/pyinat/pyinaturalist-convert): Tools to convert observation data to and from a variety of useful formats\n* [pyinaturalist-notebook](https://github.com/pyinat/pyinaturalist-notebook): Jupyter notebook Docker image for pyinaturalist\n* [dronefly](https://github.com/dronefly-garden/dronefly): A Discord bot with iNaturalist integration, used by the iNaturalist Discord server.\n",
    'author': 'Nicolas Noé',
    'author_email': 'nicolas@niconoe.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pyinat/pyinaturalist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
