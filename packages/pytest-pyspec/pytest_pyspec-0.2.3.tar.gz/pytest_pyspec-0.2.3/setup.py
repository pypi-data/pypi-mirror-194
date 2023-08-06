# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_pyspec']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

entry_points = \
{'pytest11': ['pytest_pyspec = pytest_pyspec.plugin']}

setup_kwargs = {
    'name': 'pytest-pyspec',
    'version': '0.2.3',
    'description': 'A python test spec based on pytest',
    'long_description': '\nThe **pySpec** plugin transforms the pytest output into RSpec.\n\nJust nest your tests using classes and include _docstring_ for each class and test. You can create any nested levels.\n\nThe following test sample:\n\n```python\nimport pytest\n\nclass TestHouse:\n    "a House"\n    \n    def test_door(self):\n        "has a door"\n        assert 1 == 1\n        \n    class TestTwoFloors:\n        "with two floors"\n\n        def test_stairs(self):\n            "has stairs"\n            assert 1 == 1\n\n        def test_second_floor(self):\n            "has second floor"\n            assert 1 == 1\n```\n\nGenerates the following output:\n\n```\ntest/test_sample.py \n  A house\n    Has a door                                                       .\n  A house\n    With two floors\n      Has stairs                                                     .\n      Has second floor                                               .      [100%]\n```\n\n## Installing and running **pySpec**\n\n```bash\npip install pytest-pyspec\npytest --pyspec\n```',
    'author': 'Felipe Curty',
    'author_email': 'felipecrp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
