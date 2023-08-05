# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['therapi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'therapi',
    'version': '0.0.1',
    'description': 'Therapy to ease the pain of writing boilerplate code to consume JSON APIs.',
    'long_description': "# python-therapi\nTherapy to ease the pain of writing boilerplate code to consume JSON APIs.\n\n---\n\nJSON dominates the API space these days. Consuming such APIs can become a bit of a schlep.\n\nPython makes it quite easy, but you still have to deal with it on a low level by constructing each and every request. Can't we make it easier by abstracting some of that low-level boilerplate code? Let's look at an example.\n\n## \n",
    'author': 'Helmut Irle',
    'author_email': 'me@helmut.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
