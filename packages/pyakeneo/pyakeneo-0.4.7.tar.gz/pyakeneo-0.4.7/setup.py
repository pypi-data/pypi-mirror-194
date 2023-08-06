# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyakeneo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'pyakeneo',
    'version': '0.4.7',
    'description': 'Python client for the Akeneo API REST',
    'long_description': "|Build Status|\n|Documentation Status|\n\n\nPython client for Akeneo PIM API\n================================\n\nA simple Python client to use the `Akeneo PIM API`_.\n\nDependencies are managed with `poetry`_\n(list of dependencies available in `pyproject.toml`_).\n\nYou may install them with:\n\n.. code:: bashasda\n\n        poetry install --dev\n\nInstallation\n------------\n\n.. code:: bash\n\n        poetry install pyakeneo\n        \nUsage\n-----\n\nA simple example is provided in `docs/example_exporter.py`_.\n\nIf you experience issues when importing modules, run the examples as follow:\n\n.. code:: bash\n\n        cd docs\n        poetry run python example_exporter.py\n        \n\n.. _docs/example_exporter.py: https://raw.githubusercontent.com/kavetech/akeneo_api_client/master/docs/example.py\n\nTests\n-----\n\nRun tests as follow:\n\n.. code:: bash\n\n        poetry run nosetests\n        \nIf tests don't pass in your environment, please check that dependencies match those described in pyproject.toml. One way to do it is to ensure that poetry runs commands in a dedicated virtualenv by setting environment variable as follow:\n\n.. code:: bash\n\n        poetry install --dev\n\n\nTests are provided with mocks, recorded with `VCR.py`_. In case you need\nto (re)run tests, you should install the dataset in you PIM instance as\nfollow:\n\n.. _Akeneo PIM API: https://api.akeneo.com/\n.. _poetry: https://github.com/python-poetry/poetry\n.. _VCR.py: http://vcrpy.readthedocs.io/en/latest/index.html\n.. _pyproject.toml: https://python-poetry.org/docs/pyproject/\n\n.. |Build Status| image:: https://travis-ci.org/matthieudelaro/akeneo_api_client.svg?branch=master\n   :target: https://travis-ci.org/matthieudelaro/akeneo_api_client\n.. |Documentation Status| image:: https://readthedocs.org/projects/akeneo-api-client/badge/?version=latest\n   :target: http://akeneo-api-client.readthedocs.io/en/latest/\n",
    'author': 'Kave Tech',
    'author_email': 'kavetech@kavehome.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/KaveTech/akeneo_api_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
