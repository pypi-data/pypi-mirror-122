# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['datareadingrequests']
install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'datareadingrequests',
    'version': '2.0.1',
    'description': "A client for Energize Andover's Building Energy Gateway, with a focus on clarity and usability.",
    'long_description': '# Data Reading Requests\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datareadingrequests)](https://pypi.org/project/datareadingrequests/)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/tactlessfish/datareadingrequests/main)](https://github.com/tactlessfish/datareadingrequests/actions)\n[![Coveralls](https://img.shields.io/coveralls/github/tactlessfish/datareadingrequests)](https://coveralls.io/github/tactlessfish/datareadingrequests)\n\nA new client for Energize Andover\'s Building Energy Gateway, with a focus on clarity and usability.\n\n## Features\n- It\'s packaged, so you can install it with pip!\n- It\'s fully unit-tested.\n- It\'s open source,\nand contributions are welcome.\n\n## API Changes from building_data_requests\nFor compatibility, datareadingrequests\' function definitions are similar to those of building_data_requests.\nHowever, there are a few key differences between the two modules:\n- Instead of a tuple, datareadingrequests\' `get_value()` returns a DataReading namedtuple.\nThis allows you to use the original tuple notation or the cleaner dot notation.\nRead more about namedtuples [here](https://realpython.com/python-namedtuple/).\n- datareadingrequests has a predictable, single return type for `get_value()`.\nWith building_data_requests, `get_value()` could return a valid result or `None`.\nHere, it can only return a valid result; it raises an exception if the server returns no data.\nThe reasoning for this is well-explained by williballenthin:\n> I\'ve learned that *returning more than one type of data from a function is a recipe for trouble*.\n> For example, when a function can return a string *or* a list,\n> then every place that the function is called must check "is it a string or a list?".\n> If the programmer forgets this, then inevitably,\n> the program breaks at an inconvenient time.\n> By extension, if a function returns a string or `None`,\n> then every invocation must check "is the result `None`?".\n> This is easy to forget, and leads to latent bugs.\n> With the existing style, forgetting a `try/except` block is also a bug,\n> but when the exception is generated,\n> the programmer gets a very explicit stack trace with easy-to-find line number.\n- In the same way, datareadingrequests\' `get_bulk()` raises an exception\nif the server returns no data for any specific instance.\n- datareadingrequests has no way (currently) to change hostname or port.\n- datareadingrequests does not retry requests without SSL.\n  \n## Setup\nUse your favorite Python package manager, and do as you would with pandas, matplotlib, etc.\n\npip:\n```\npip install datareadingrequests\npip freeze > requirements.txt\n```\n\nPoetry:\n```\npoetry add datareadingrequests\n```\n',
    'author': 'fisher',
    'author_email': 'fisher521.fs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tactlessfish/datareadingrequests',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
