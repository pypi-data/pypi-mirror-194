# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['methodic_cache']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.0.0,<6.0.0']

extras_require = \
{':python_version < "3.10"': ['typing-extensions>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'methodic-cache',
    'version': '0.3.1',
    'description': 'functools.cache() for methods, done correctly',
    'long_description': '# methodic_cache\n\n[![codecov](https://codecov.io/gh/youtux/methodic_cache/branch/main/graph/badge.svg?token=7LSah9W8zt)](https://codecov.io/gh/youtux/methodic_cache)\n\n`functools.cache()` for methods, done correctly.\n\n`methodic_cache.cached_method` is a decorator that caches the return value of a method, based on the arguments passed to it.\n\nThe peculiarity of this library is that it does not store anything on objects themselves, but rather on a separate WeakKeyDictionary where the lifetime of the cache matches the lifetime of the object.\n\nAn advantage of this approach over storing the cache on the object itself when needed is that objects will keep their memory footprint smaller thanks to shared key dictionaries. See [PEP 412](https://peps.python.org/pep-0412/) and [The Dictionary Even Mightier - Brandon Rhodes at PyCon 2017, 00:21:02](https://www.youtube.com/watch?v=66P5FMkWoVU&t=1262s) for more details.\n\n\n# Features\n* Simple to use\n* Extendable with [custom cache backends](#custom-cache-backends) (e.g. LRUCache, LFUCache, etc.)\n* Works with non-hashable objects\n* Works with [frozen/slotted classes](#using-classes-with-__slots__)\n* Tested for memory leaks\n\n# Installation\n```bash\npip install methodic_cache\n```\n\n# Usage\n```python\nfrom methodic_cache import cached_method\n\n\nclass MyClass:\n    @cached_method\n    def my_method(self, arg1, arg2):\n        return arg1 + arg2\n\n\nmy_obj = MyClass()\nmy_obj.my_method(1, 2)  # returns 3\nmy_obj.my_method(1, 2)  # returns 3 from the cache\n```\n\n\n## Using classes with `__slots__`\nClasses that define `__slots__` need to have a `__weakref__` slot to be able to be weakly referenced:\n\n```python\nfrom methodic_cache import cached_method\n\n\nclass MyClass:\n    __slots__ = ("my_attr", "__weakref__")  # <-- __weakref__ is required\n\n    def __init__(self, my_attr):\n        self.my_attr = my_attr\n\n    @cached_method\n    def my_method(self, arg1, arg2):\n        print(f"Computing {self.my_attr} + {arg1} + {arg2}...")\n        return self.my_attr + arg1 + arg2\n\nmy_obj = MyClass(1)\nmy_obj.my_method(2, 3)\n# prints "Computing 1 + 2 + 3..."\n# returns 6\nmy_obj.my_method(2, 3)\n# returns 6\n```\n\n\n## Custom cache backends\nYou can use any cache backend that implements the `MutableMapping` interface (e.g. `dict`, `lru_cache`, `functools.lru_cache`, etc.).\nThe default cache backend is `cachetools.Cache(maxsize=math.inf)`, which will keep the cache bounded to the lifetime of the `self` object.\n\nYou can use a different cache backend by passing it as the `cache_factory` argument to `cached_method`:\n\n```python\nfrom methodic_cache import cached_method\nfrom cachetools import LRUCache\n\n\nclass MyClass:\n    @cached_method(cache_factory=lambda: LRUCache(maxsize=1))\n    def my_method(self, arg1, arg2):\n        print(f"Computing {arg1} + {arg2}...")\n        return arg1 + arg2\n\n\nmy_obj = MyClass()\nmy_obj.my_method(1, 1)\n# prints Computing 1 + 1...\n# returns 2\nmy_obj.my_method(1, 1)\n# returns 2\nmy_obj.my_method(2, 2)\n# prints Computing 2 + 2...\n# returns 4\nmy_obj.my_method(1, 1)  # <-- this will be recomputed because the cache is full\n# prints Computing 1 + 1...\n# returns 2\n```\n',
    'author': 'Alessio Bogon',
    'author_email': '778703+youtux@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/youtux/methodic_cache',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
