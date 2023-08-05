# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['horology']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'horology',
    'version': '1.2.0',
    'description': 'Conveniently measures the time of loops, contexts and functions.',
    'long_description': '# `Horology`\n\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mjmikulski/horology.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mjmikulski/horology/context:python)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/mjmikulski/horology.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mjmikulski/horology/alerts/)\n[![Downloads](https://pepy.tech/badge/horology/month)](https://pepy.tech/project/horology)\n[![PyPI version](https://badge.fury.io/py/horology.svg)](https://badge.fury.io/py/horology)\n\n[![CircleCI](https://circleci.com/gh/mjmikulski/horology/tree/master.svg?style=svg)](https://circleci.com/gh/mjmikulski/horology/tree/master)\n\nConveniently measures the time of your loops, contexts and functions.\n\n![](hourglass.jpg "Photo by Mike from Pexels")\n\n\n\n## Installation\nSimply:\n```\npip install horology\n```\n\nWorks with python versions 3.6, 3.7, 3.8 and 3.9. Tested on Linux, Windows and MacOS.\n\n## Usage\nThe following 3 tools will let you measure practically any part of your Python code.\n\n### Timing an iterable (list, tuple, generator, etc)\n#### Quick example\n```python\nfrom horology import Timed\n\nanimals = [\'cat\', \'dog\', \'crocodile\']\n\nfor x in Timed(animals):\n    feed(x)\n```\nResult:\n```\niteration    1: 12.0 s\niteration    2: 8.00 s\niteration    3: 100 s\n\ntotal 3 iterations in 120 s\nmin/median/max: 8.00/12.0/100 s\naverage (std): 40.0 (52.0) s\n\n```\n\n#### More cool stuff:\nYou can specify where (if at all) you want each iteration and summary to be printed, eg.:\n```python\nfor x in Timed(animals, unit=\'ms\', \n               iteration_print_fn=logger.debug, \n               summary_print_fn=logger.info):\n    feed(x)\n```\n\n\n### Timing a function with a `@timed` decorator\n#### Quick example\n```python\nfrom horology import timed\n\n@timed\ndef foo():\n    ...\n```\nResult:\n```\n>>> foo()\nfoo: 7.12 ms\n```\n\n#### More cool stuff:\nPersonalize time unit and name\n```python\n@timed(unit=\'s\', name=\'Processing took \')\ndef bar():\n    ...\n```\nResult:\n```\n>>> bar()\nProcessing took 0.185 s\n```\n\n\n### Timing part of code with a `Timing` context\n#### Quick example\nJust wrap your code using a `with` statement\n```python\nfrom horology import Timing\n\nwith Timing(name=\'Important calculations: \'):\n    ...\n```\nResult:\n```\nImportant calculations: 12.4 s\n```\n\n#### More cool stuff:\nYou can suppress default printing and directly use measured time (also within context)\n```python\nwith Timing(print_fn=None) as t:\n    ...\n    \nmake_use_of(t.interval)\n```\n\n\n## Time units\nTime units are by default automatically adjusted, for example you will see\n`foo: 7.12 ms` rather than `foo: 0.007 s`. If you don\'t like it, you can \noverride this by setting the `unit` argument with one of these names: \n`[\'ns\', \'us\', \'ms\', \'s\', \'min\', \'h\', \'d\']`.\n\n\n\n## Contributions \nContributions are welcomed, see [contribution guide](.github/contributing.md).\n\n\n\n## Internals\nHorology internally measures time with `perf_counter` which provides the *highest available resolution,*\n see [docs](https://docs.python.org/3/library/time.html#time.perf_counter).\n',
    'author': 'mjmikulski',
    'author_email': 'maciej.mikulski.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mjmikulski/horology',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
