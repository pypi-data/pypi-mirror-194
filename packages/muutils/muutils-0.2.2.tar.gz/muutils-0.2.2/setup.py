# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['muutils',
 'muutils._wip',
 'muutils.json_serialize',
 'muutils.logger',
 'muutils.zanj']

package_data = \
{'': ['*']}

install_requires = \
['jaxtyping>=0.2.12,<0.3.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'torch>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'muutils',
    'version': '0.2.2',
    'description': 'A collection of miscellaneous python utilities',
    'long_description': '\n\n`muutils`, stylized as "$\\mu$utils" or "μutils", is a collection of miscellaneous python utilities, meant to be small and with ~~no~~ minimal dependencies outside of standard python.\n\n\n- [`json_serialize`](https://github.com/mivanit/muutils/tree/main/muutils/json_serialize.py) is a tool for serializing and loading arbitrary python objects into json\n- [`statcounter`](https://github.com/mivanit/muutils/tree/main/muutils/statcounter.py) is an extension of `collections.Counter` that provides "smart" computation of stats (mean, variance, median, other percentiles) from the counter object without using `Counter.elements()`\n- [`group_equiv`](https://github.com/mivanit/muutils/tree/main/muutils/group_equiv.py) groups elements from a sequence according to a given equivalence relation, without assuming that the equivalence relation obeys the transitive property\n- [`logger`](https://github.com/mivanit/muutils/tree/main/muutils/logger.py) implements a logger with "streams" and a timer context manager\n- [`jsonlines`](https://github.com/mivanit/muutils/tree/main/muutils/jsonlines.py) extremely simple utility for reading/writing `jsonl` files\n- [`ZANJ`](https://github.com/mivanit/muutils/tree/main/muutils/zanj/zanj.py) is a WIP hdf5 alternative. This will probably be spun off into its own repo\n\nThere are a couple work-in-progress utilities in [`_wip`](https://github.com/mivanit/muutils/tree/main/muutils/_wip/) that aren\'t ready for anything, but nothing in this repo is suitable for production. Use at your own risk!\n\n\n# installation\n\n```\npip install muutils\n```\n',
    'author': 'mivanit',
    'author_email': 'mivanits@umich.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mivanit/muutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
