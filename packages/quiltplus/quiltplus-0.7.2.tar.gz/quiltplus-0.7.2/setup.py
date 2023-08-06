# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiltplus', 'quiltplus.cli']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'asyncclick>=8.1.3.4,<9.0.0.0',
 'isort>=5.12.0,<6.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'quilt3>=5.1.0,<6.0.0',
 'trio>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['qp = quiltplus.cli.qp:cli']}

setup_kwargs = {
    'name': 'quiltplus',
    'version': '0.7.2',
    'description': "Resource-oriented Python API/CLI for Quilt's decentralized social knowledge platform",
    'long_description': '# quiltplus\nResource-oriented API for Quilt\'s decentralized social knowledge platform\n\n## Command-Line QuickStart\n\n```bash\npip install quiltplus\nqp get "quilt+s3://quilt-example#package=examples/echarts"\nqp list\n```\n\n## Developmment\n\nUses the [trio](https://trio.readthedocs.io/en/stable/) version of Python\'s `async` I/O\n\n```bash\ngit clone https://github.com/quiltdata/quiltplus\ncd quiltplus\npoetry self update\npoetry install\nexport WRITE_BUCKET=writeable_s3_bucket\npoetry run ptw --now .\n```\n## Pushing Changes\nBe sure you to first set your [API token](https://pypi.org/manage/account/) using `poetry config pypi-token.pypi <pypi-api-token>`\n\n```bash\n# merge PR\npoetry version patch # minor major\npoetry build\npoetry publish\n# create new branch\npoetry version prepatch # preminor premajor\n```\n',
    'author': 'Ernest Prabhakar',
    'author_email': 'ernest@quiltdata.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
