# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonemptystr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nonemptystr',
    'version': '0.2.0',
    'description': 'Non-empty string',
    'long_description': '# nonemptystr\n\n[![PyPI](https://img.shields.io/pypi/v/nonemptystr)](https://pypi.org/project/nonemptystr/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonemptystr)](https://pypi.org/project/nonemptystr/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/nonemptystr)](https://github.com/nekonoshiri/nonemptystr/blob/main/LICENSE)\n\nNon-empty string.\n\n## Usage\n\n```Python\nfrom nonemptystr import EmptyString, nonemptystr\n\nname: nonemptystr = nonemptystr("John")\n\ntry:\n    name = nonemptystr("")\nexcept EmptyString:\n    print("The name is empty.")\n```\n\n### ... with [pydantic](https://github.com/samuelcolvin/pydantic)\n\n```Python\nfrom nonemptystr import nonemptystr\nfrom pydantic import BaseModel, ValidationError\n\nclass Request(BaseModel):\n    user_id: nonemptystr\n\ntry:\n    request = Request.parse_obj({"user_id": ""})\n    print(f"user_id: {request.user_id}")\nexcept ValidationError:\n    print("user_id is empty")\n```\n\n## API\n\n### Module `nonemptystr`\n\n#### *class* `nonemptystr(obj: object)`\n\nSubclass of `str`.\nRaise `EmptyString` exception if `str(obj)` is empty string.\n\n#### *class* `EmptyString`\n\nSubclass of `ValueError`.\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/nonemptystr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
