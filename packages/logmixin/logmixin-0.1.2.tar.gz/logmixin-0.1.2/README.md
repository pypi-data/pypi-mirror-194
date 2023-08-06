# logmixin

## Description

This is an extremely small Python package (one module, ~40 lines) to enable quick and easy logging within class methods.

## Usage

It defines a mixin class that adds a `get_logger` method to your class. This method returns a logger with the name of
your module, class, and method that called it. For example, suppose you have a module called `my_module.py` with these
contents:

```python
import logging
from logmixin import LogMixin


class MyClass(LogMixin):
    """A class with logging enabled."""
    def my_method(self):
        self.get_logger().info("Hello, world!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    MyClass().my_method()
```

If you run this file, you will see the following output:

```
INFO:my_module.MyClass.my_method:Hello, world!
```

## Installation

You can install this package from PyPI:

```bash
pip install logmixin
```

## License

MIT



