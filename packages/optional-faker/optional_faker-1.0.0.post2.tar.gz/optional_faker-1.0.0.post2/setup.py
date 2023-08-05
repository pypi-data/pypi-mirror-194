# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['optional_faker']
install_requires = \
['Faker']

setup_kwargs = {
    'name': 'optional-faker',
    'version': '1.0.0.post2',
    'description': 'Small wrapper around faker, to make values optional!',
    'long_description': '# optional-faker\n\n[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)\n\n[![Build Status](https://github.com/PerchunPak/optional-faker/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/optional-faker/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/PerchunPak/optional-faker/branch/master/graph/badge.svg)](https://codecov.io/gh/PerchunPak/optional-faker)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Python support versions badge (from pypi)](https://img.shields.io/pypi/pyversions/optional-faker)](https://www.python.org/downloads/)\n\nSmall wrapper around faker, to make values optional!\n\n## Example\n\n```py\n>>> from faker import Faker\n>>> import optional_faker\n>>>\n>>> fake = Faker()\n>>> Faker.seed(444)\n>>>\n>>> # `fake.optional` can take any value, and return it, or None.\n>>> fake.optional(fake.pystr())\n\'qazSMGwqdElzLTggMaPM\'\n>>> fake.optional(fake.pystr())\nNone\n>>> # or it can take callable, and *args with **kwargs\n>>> # that will be passed to this callable.\n>>> fake.optional(fake.pystr, 1, max_chars=10)\n\'hmIEP\'\n>>> fake.optional(fake.pystr, 1, max_chars=10)\nNone\n>>> # there is no explicit check is callable a faker part,\n>>> # so you can pass anything.\n>>> fake.optional(lambda: "my callable!")\n\'my callable!\'\n>>> fake.optional(lambda: "my callable!")\nNone\n```\n\n## Installing\n\n```bash\npip install optional-faker\n```\n\nAnd then you need to import `optional_faker` anywhere but before creating `Faker` instance.\n\n## Installing for local developing\n\n```bash\ngit clone https://github.com/PerchunPak/optional-faker.git\ncd optional-faker\n```\n\n### Installing `poetry`\n\nNext we need install `poetry` with [recommended way](https://python-poetry.org/docs/master/#installation).\n\nIf you use Linux, use command:\n\n```bash\ncurl -sSL https://install.python-poetry.org | python -\n```\n\nIf you use Windows, open PowerShell with admin privileges and use:\n\n```powershell\n(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -\n```\n\n### Installing dependencies\n\n```bash\npoetry install\n```\n\n### If something is not clear\n\nYou can always write me!\n\n## Updating\n\n```bash\npip install -U optional-faker\n```\n\n### For local development\n\nFor updating, just re-download repository,\nif you used `git` for downloading, just run `git pull`.\n\n## Thanks\n\nThis project was inspired by [faker-optional](https://github.com/lyz-code/faker-optional).\n\nThis project was generated with [python-template](https://github.com/PerchunPak/python-template).\n',
    'author': 'PerchunPak',
    'author_email': 'pypi@perchun.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PerchunPak/optional-faker',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
