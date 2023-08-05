# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xmod']
install_requires = \
['dek>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'xmod',
    'version': '1.4.0',
    'description': '🌱 Turn any object into a module 🌱',
    'long_description': 'Callable modules!  Indexable modules!?\n\nEver wanted to call a module directly, or index it?  Or just sick of seeing\n`from foo import foo` in your examples?\n\nGive your module the awesome power of an object, or maybe just save a\nlittle typing, with `xmod`.\n\n`xmod` is a tiny library that lets a module to do things that normally\nonly a class could do - handy for modules that "just do one thing".\n\n## Example: Make a module callable like a function!\n\n    # In your_module.py\n    import xmod\n\n    @xmod\n    def a_function():\n        return \'HERE!!\'\n\n\n    # Test at the command line\n    >>> import your_module\n    >>> your_module()\n    HERE!!\n\n## Example: Make a module look like a list!?!\n\n    # In your_module.py\n    import xmod\n\n    xmod(list(), __name__)\n\n    # Test at the command line\n    >>> import your_module\n    >>> assert your_module == []\n    >>> your_module.extend(range(3))\n    >>> print(your_module)\n    [0, 1, 2]\n\n\n### [API Documentation](https://rec.github.io/xmod#xmod--api-documentation)\n',
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
