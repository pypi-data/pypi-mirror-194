# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devo_ml', 'devo_ml.modelmanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'devo-mlmodelmanager',
    'version': '1.2.0',
    'description': "A client for Devo's ML model manager",
    'long_description': '![License](https://img.shields.io/github/license/DevoInc/python-mlmodelmanager-client)\n![Release](https://img.shields.io/github/v/release/DevoInc/python-mlmodelmanager-client?display_name=tag&sort=semver)\n![Tests](https://github.com/DevoInc/python-mlmodelmanager-client/actions/workflows/test-tox.yml/badge.svg)\n![Python](https://img.shields.io/pypi/pyversions/devo-mlmodelmanager)\n\n# Devo Python ML Model Manager Client\n\nThe **ML Model Manager** is a service to register machine learning models on\n[Devo](https://www.devo.com) platform. These models can be used through the\nquery engine using the `mlevalmodel(...)`  operation or through the\n[FLOW](https://docs.devo.com/space/latest/95213164/Flow) correlation engine\nincluding in the context the\n[MlSingleModelEval](https://docs.devo.com/space/latest/95214962/ML+Single+Model+Evaluator)\nunit.\n\n**devo-mlmodelmanager** provides an easy-to-use client for Devo’s ML Model\nManager. Built on top of the widely used\n[Requests](https://requests.readthedocs.io/en/latest/) library exposes a\nsimplified interface for model management, allowing you to focus in the machine\nlearning workflows and not worry about the integration with Devo platform.\n\n## A simple example\n\n``` python\nfrom devo_ml.modelmanager import create_client_from_token\n\nurl = "<model-manager-server-url>"\ntoken = "<valid-access-token>"\n\nclient = create_client_from_token(url, token)\n\nclient.add_model(\n   "pokemon_onnx_regression",          # model name\n   "ONNX",                             # model engine\n   "~/models/pokemon.onnx",            # model file\n   description="A funny Pokemon prediction"\n)\n```\n\n## Requirements\n\n* Python 3.7+\n\n## Install\n\n``` console\n$ pip install devo-mlmodelmanager\n```\n\n## Documentation\n\nExplore the [documentation](https://devoinc.github.io/python-mlmodelmanager-client/) to learn more.\n',
    'author': 'Devo ML Team',
    'author_email': 'machine.learning@devo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DevoInc/python-mlmodelmanager-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
