# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logmixin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logmixin',
    'version': '0.1.2',
    'description': 'Defines a mixin class that adds a convenient get_logger method.',
    'long_description': '# logmixin\n\n## Description\n\nThis is an extremely small Python package (one module, ~40 lines) to enable quick and easy logging within class methods.\n\n## Usage\n\nIt defines a mixin class that adds a `get_logger` method to your class. This method returns a logger with the name of\nyour module, class, and method that called it. For example, suppose you have a module called `my_module.py` with these\ncontents:\n\n```python\nimport logging\nfrom logmixin import LogMixin\n\n\nclass MyClass(LogMixin):\n    """A class with logging enabled."""\n    def my_method(self):\n        self.get_logger().info("Hello, world!")\n\n\nif __name__ == "__main__":\n    logging.basicConfig(level=logging.INFO)\n    MyClass().my_method()\n```\n\nIf you run this file, you will see the following output:\n\n```\nINFO:my_module.MyClass.my_method:Hello, world!\n```\n\n## Installation\n\nYou can install this package from PyPI:\n\n```bash\npip install logmixin\n```\n\n## License\n\nMIT\n\n\n\n',
    'author': 'Sam Mathias',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sammosummo/logmixin',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
