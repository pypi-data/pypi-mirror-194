# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['abbrev']
install_requires = \
['xmod>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'abbrev',
    'version': '1.1.0',
    'description': '🐜 Tiny full-featured abbreviation expander 🐜',
    'long_description': "Expand a `Sequence` or `Mapping` of string abbreviations.\n\nHandy when the user has a choice of commands with long names.\n\n## Example 1: Use a list of choices\n\n    import abbrev\n\n    a = ['one', 'two', 'three']\n\n    assert abbrev(a, 'one') == 'one'\n    assert abbrev(a, 'o') == 'one'\n    assert abbrev(a, 'tw') == 'two'\n\n    abbrev(a, 'four')  # Raises a KeyError: no such key\n    abbrev(a, 't')  # Raises a KeyError: ambiguous key ('two' or 'three'?)\n\n\n## Example 2: Use a dictionary of choices\n\n    import abbrev\n\n    d = {'one': 100, 'two': 200, 'three': 300}\n\n    assert abbrev(d, 'one') == 100\n    assert abbrev(d, 'o') == 100\n    assert abbrev(d, 'tw') == 200\n\n## Example 3: Make an abbreviator to re-use\n\n    import abbrev\n\n    d = {'one': 100, 'two': 200, 'three': 300}\n\n    abbreviator = abbrev(d)\n\n    assert abbreviator('one') == my_abbrevs('o') == 100\n    assert abbreviator('tw') == 200\n\n## Example 4: Get all matches, when `multi=True`\n\n    import abbrev\n\n    a = ['one', 'two, 'three'}\n\n    multi = abbrev(a, multi=True)  # Make an abbreviator\n\n    assert multi('t') == abbrev(d, 't', multi=True) == ('two', three')\n    assert multi('o') == abbrev(d, 'o', multi=True) == ('one', )\n\n    multi('four')  # Still raises a key error\n\n## Example 5: Get only the first result, when `unique=False`\n\n    import abbrev\n\n    d = {'one': 100, 'two': 200, 'three': 300}\n\n    assert abbrev(d, 't', unique=False) == (200, 300)\n\n\n### [API Documentation](https://rec.github.io/abbrev#abbrev--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
