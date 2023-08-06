# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hydev']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.7.8,<2.0.0',
 'black>=22.12.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'flake8-broken-line>=0.6.0,<0.7.0',
 'flake8-debugger>=4.1.2,<5.0.0',
 'flake8-mock-x2>=0.4.1,<0.5.0',
 'flake8-print>=5.0.0,<6.0.0',
 'flake8-pytest-style>=1.7.2,<2.0.0',
 'flake8-use-fstring>=1.4,<2.0',
 'flake8>=5.0.4,<6.0.0',
 'ipdb>=0.13.11,<0.14.0',
 'isort>=5.12.0,<6.0.0',
 'mypy>=0.991,<0.992',
 'poetry-plugin-up>=0.3.0,<0.4.0',
 'poetry>=1.3.2,<2.0.0',
 'pre-commit>=2.21.0,<3.0.0',
 'pytest-asyncio>=0.20.3,<0.21.0',
 'pytest-blockage>=0.2.4,<0.3.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest-deadfixtures>=2.2.1,<3.0.0',
 'pytest-env>=0.8.1,<0.9.0',
 'pytest-timeout>=2.1.0,<3.0.0',
 'pytest>=7.2.1,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'django': ['django-coverage-plugin>=2.0.4,<3.0.0',
            'django-debug-toolbar>=3.8.1,<4.0.0',
            'django-extra-checks>=0.13.3,<0.14.0',
            'django-migration-linter>=4.1.0,<5.0.0',
            'django-querycount>=0.7.0,<0.8.0',
            'django-split-settings>=1.2.0,<2.0.0',
            'django-stubs>=1.15.0,<2.0.0',
            'django-stubs-ext>=0.7.0,<0.8.0',
            'django-test-migrations>=1.2.0,<2.0.0',
            'flake8-django>=1.1.5,<2.0.0',
            'pytest-django>=4.5.2,<5.0.0']}

entry_points = \
{'console_scripts': ['hyd = hydev.main:Fulltest.run_cli',
                     'hydautoflake = hydev.main:Autoflake.run_cli',
                     'hydblack = hydev.main:Black.run_cli',
                     'hyddeploy = hydev.deploy:DeployManager.run_cli',
                     'hydflake8 = hydev.main:Flake8.run_cli',
                     'hydfmt = hydev.main:Format.run_cli',
                     'hydisort = hydev.main:ISort.run_cli',
                     'hydmypy = hydev.main:Mypy.run_cli',
                     'hydpytest = hydev.main:Pytest.run_cli',
                     'hydtest = hydev.main:Fulltest.run_cli']}

setup_kwargs = {
    'name': 'hydev',
    'version': '1.1.0',
    'description': 'Common tooling and configuration for pythonic development',
    'long_description': 'None',
    'author': 'hoverhell',
    'author_email': 'hoverhell@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
