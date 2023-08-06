# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mocksey', 'mocksey.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mocksey',
    'version': '0.4.0',
    'description': 'Stupidly-simple python mocking utility with moxie.',
    'long_description': "mocksey\n=======\n\nStupidly-simple python mocking utility with moxie.\n\n|BuildImage|_\n\n.. image:: https://pypip.in/v/mocksey/badge.png\n    :target: https://crate.io/packages/mocksey/\n    :alt: Latest PyPI version\n\n.. image:: https://pypip.in/d/mocksey/badge.png\n    :target: https://crate.io/packages/mocksey/\n    :alt: Number of PyPI downloads\n\n|Coverage Status|\n\n .. |Coverage Status| image:: https://coveralls.io/repos/mitgr81/mocksey/badge.png\n    :target: https://coveralls.io/r/mitgr81/mocksey\n\n\nMocksey Motivation\n==================\n\nI was teaching a class on unit testing to a group of co-workers who were familiar with `Simple Test for PHP <http://www.simpletest.org/>`_ so I hacked together what is becoming Mocksey.\n\nMocksey the TDD'd version of that TDD utilty. `It's so meta even this acronym <http://xkcd.com/917/>`_.\n\nInstallation\n============\n\nEither find mocksey on PyPI_ or install it with pip or easy_install\n::\n\n  pip install mocksey\n  #or\n  easy_install mocksey\n\nBasic Usage\n===========\n\nIt's pretty simple.  Create a mocked object with generate_mock, inject it (or monkey patch) and set up your assertions.  After your function call(s), simply call 'run_asserts' and win!\n\nThe unit tests are a pretty decent working example.\n\nTweaksey\n========\n\nTweaksey is a collection of beautification wrappers.  Currently there's only one around mock_, but there may be more in the future.  It'll look best if you also have nose_ installed, and may only be worth it in that case, actually.  Anyhow, to use it simply import tweaksey from mocksey and get your copy of the mock package from ``tweaksey.tweak_mock``.  Your mock assertions should now have a touch more friendliness.  If there are more you'd like to add, go for it!  Michael Foord, if you want to take the output and run, that cool too (conversely, if you don't like that I did this, I'll kill it square dead).\n\n\nChangelog\n=========\n\n0.3.1\n-----\nMocksey now sets nose to full diff mode.\n\n0.3.0\n-----\nTweaksey now requires you to pass in the 'mock' library that you're\ntweaking.  This allows one to apply mocks to python3's ``unittest.mock``.\n\n\nLicense\n=======\nThis software is hereby released under the MIT License, as seen in the LICENSE file\n\n.. |BuildImage| image:: https://secure.travis-ci.org/mitgr81/mocksey.png\n.. _BuildImage: https://travis-ci.org/mitgr81/mocksey\n.. _PyPI: http://pypi.python.org/pypi/mocksey\n.. _mock: http://www.voidspace.org.uk/python/mock/\n.. _nose: https://pypi.python.org/pypi/nose/\n",
    'author': 'Chris McGraw',
    'author_email': 'mitgr81+mocksey@mitgr81.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mitgr81/mocksey',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
