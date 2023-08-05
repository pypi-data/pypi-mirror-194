# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crontools']

package_data = \
{'': ['*']}

install_requires = \
['tzlocal>=2.0,<3.0']

setup_kwargs = {
    'name': 'crontools',
    'version': '0.1.6',
    'description': 'Python cron tools',
    'long_description': '=========\ncrontools\n=========\n\n.. image:: https://static.pepy.tech/personalized-badge/crontools?period=month&units=international_system&left_color=grey&right_color=orange&left_text=Downloads/month\n    :target: https://pepy.tech/project/crontools\n    :alt: Downloads/month\n.. image:: https://github.com/dapper91/crontools/actions/workflows/test.yml/badge.svg?branch=master\n    :target: https://github.com/dapper91/crontools/actions/workflows/test.yml\n    :alt: Build status\n.. image:: https://img.shields.io/pypi/l/crontools.svg\n    :target: https://pypi.org/project/crontools\n    :alt: License\n.. image:: https://img.shields.io/pypi/pyversions/crontools.svg\n    :target: https://pypi.org/project/crontools\n    :alt: Supported Python versions\n.. image:: https://codecov.io/gh/dapper91/crontools/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/dapper91/crontools\n    :alt: Code coverage\n\n\n``crontools`` is a library that allows you to parse crontab expression and iterate over scheduled fire times.\n\n\nFeatures:\n\n- crontab expression parser\n- optional seconds field support\n- optional year field support\n- crontab fire time sequential iteration support\n\nInstallation\n------------\n\nYou can install crontools with pip:\n\n.. code-block:: console\n\n    $ pip install crontools\n\n\nQuickstart\n----------\n\n\nGet next cron fire time:\n~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    >>> import datetime as dt\n    >>> import crontools as ct\n    >>>\n    >>> tz = dt.timezone.utc\n    >>> now = dt.datetime.fromisoformat(\'2020-02-29 23:59:59.999+00:00\')\n    >>> ct = ct.Crontab.parse(\n    ...     \'* * * * * * *\',\n    ...     seconds_ext=True,\n    ...     years_ext=True,\n    ...     tz=tz,\n    ... )\n    >>>\n    >>> print(f"Next fire time: {ct.next_fire_time(now=now)}")\n    Next fire time: 2020-03-01 00:00:00+00:00\n\n\nIteration over cron fire times starting from now:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    >>> import crontools as ct\n    >>>\n    >>> tz = dt.timezone.utc\n    >>> now = dt.datetime.fromisoformat(\'2021-02-01 00:00:00+00:00\')\n    >>> ct = ct.Crontab.parse(\n    ...     \'30 30 12-16/2 1,2 JAN SAT,SUN *\',\n    ...     seconds_ext=True,\n    ...     years_ext=True,\n    ...     tz=tz,\n    ... )\n    >>>\n    >>> cron_iter = ct.iter(start_from=now)\n    >>> for n, fire_datetime in zip(range(1, 31), cron_iter):\n    ...     print("{n:2}: {dt}".format(n=n, dt=fire_datetime))\n    ...\n    ...\n     1: 2022-01-01 12:30:30+00:00\n     2: 2022-01-01 14:30:30+00:00\n     3: 2022-01-01 16:30:30+00:00\n     4: 2022-01-02 12:30:30+00:00\n     5: 2022-01-02 14:30:30+00:00\n     6: 2022-01-02 16:30:30+00:00\n     7: 2022-01-08 12:30:30+00:00\n     8: 2022-01-08 14:30:30+00:00\n     9: 2022-01-08 16:30:30+00:00\n    10: 2022-01-09 12:30:30+00:00\n    11: 2022-01-09 14:30:30+00:00\n    12: 2022-01-09 16:30:30+00:00\n    13: 2022-01-15 12:30:30+00:00\n    14: 2022-01-15 14:30:30+00:00\n    15: 2022-01-15 16:30:30+00:00\n    16: 2022-01-16 12:30:30+00:00\n    17: 2022-01-16 14:30:30+00:00\n    18: 2022-01-16 16:30:30+00:00\n    19: 2022-01-22 12:30:30+00:00\n    20: 2022-01-22 14:30:30+00:00\n    21: 2022-01-22 16:30:30+00:00\n    22: 2022-01-23 12:30:30+00:00\n    23: 2022-01-23 14:30:30+00:00\n    24: 2022-01-23 16:30:30+00:00\n    25: 2023-01-01 12:30:30+00:00\n    26: 2023-01-01 14:30:30+00:00\n    27: 2023-01-01 16:30:30+00:00\n    28: 2023-01-02 12:30:30+00:00\n    29: 2023-01-02 14:30:30+00:00\n    30: 2023-01-02 16:30:30+00:00\n',
    'author': 'Dmitry Pershin',
    'author_email': 'dapper1291@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dapper91/crontools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
