# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perspective']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'orjson>=3.8.6,<4.0.0']

setup_kwargs = {
    'name': 'perspectiveapi',
    'version': '0.1.0',
    'description': "a python wrapper for google's perspective api",
    'long_description': '# 💖 perspective\na strongly typed wrapper for google\'s perspective api\n\n## \U0001fab4 example\n```py\nfrom perspective import Perspective, Attribute\nfrom asyncio import get_event_loop\n\np = Perspective(key="...")\n\nasync def main():\n    s = await p.score(\n        "your message here", attributes=(Attribute.flirtation, Attribute.sexually_explicit)\n    )\n    print(s.flirtation) \n    print(s.sexually_explicit)\n```',
    'author': 'thrzl.',
    'author_email': 'thrizzle@skiff.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
