#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['yuyo']

package_data = \
{'': ['*']}

install_requires = \
['hikari~=2.0.0.dev102']

extras_require = \
{'docs': ['pdoc==8.0.0'],
 'flake8': ['flake8==3.9.2',
            'flake8-bandit~=2.1.2',
            'flake8-black==0.2.3',
            'flake8-broken-line==0.3.0',
            'flake8-builtins==1.5.3',
            'flake8-coding==1.3.2',
            'flake8-comprehensions==3.6.1',
            'flake8-deprecated==1.3',
            'flake8-docstrings==1.6.0',
            'flake8-executable==2.1.1',
            'flake8-fixme==1.1.1',
            'flake8-functions==0.0.6',
            'flake8-html==0.4.1',
            'flake8-if-statements==0.1.0',
            'flake8-isort==4.0.0',
            'flake8-mutable==1.2.0',
            'flake8-pep3101==1.3.0',
            'flake8-print==4.0.0',
            'flake8-printf-formatting==1.1.2',
            'flake8-pytest-style==1.5.0',
            'flake8-raise==0.0.5'],
 'lint': ['codespell==2.1.0'],
 'publish': ['flit~=3.3'],
 'reformat': ['black~=21.9b0', 'isort==5.9.3'],
 'tests': ['pytest==6.2.5', 'pytest-asyncio==0.15.1', 'pytest-cov==2.12.1'],
 'type_checking': ['pyright==0.0.10']}

setup(name='hikari-yuyo',
      version='1.0.2a1',
      description='A collection of utility classes and functions for use with Hikari',
      author=None,
      author_email='Faster Speeding <lucina@lmbyrne.dev>',
      url=None,
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.8.0,<3.12',
     )
