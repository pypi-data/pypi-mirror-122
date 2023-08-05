# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['power_cache']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'power-cache',
    'version': '0.1.0',
    'description': 'Simple (but powerful) Caching Tools',
    'long_description': '# Power Cache\n\n[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSimple (but powerful) Caching Tools.\n\n## Why another caching library\n\nThere are many libraries out there to deal with the same problem that this\nlibrary tries to solve, but most of them fall short on at least one of the\nfollowing points:\n\n- Minimalism.\n- Providing proper type hints to ease the user\'s life when using the library.\n- Providing out-of-the-box support for asynchronous functions.\n- Simplicity. One clear example is how cache\'s capacity is measured. In\n  `power_cache`, capacity is measured just counting items, and not using their\n  size, as other libraries do. There are legitimate reasons to avoid the "sizes\n  approach": it heavily affects performance, and it\'s highly error prone.\n- Correctness:\n  - Some popular implementations incorrectly implement `__eq__` by just\n    comparing object hashes.\n  - Some popular implementations implement `__hash__` in a way that collisions\n    will be more frequent than desirable.\n\n## Usage\n\n### LRU Cache\n\n```python\nfrom power_cache import LRUCache\n\ncache = LRUCache(capacity=3)\n\n# We can also specify key & value types if we are using `mypy` or `pytypes`\ncache = LRUCache[str, int](capacity=3)\n\ncache[\'the answer to everything\'] = 42\ncache[\'the answer to everything\']  # returns 42\n\ncache[\'a\'] = 1\ncache[\'b\'] = 2\ncache[\'c\'] = 3\n\n# Raises KeyError, because the key was the least recently used, and the capacity\n# is only 3, so the previous value was evicted.\ncache[\'the answer to everything\']\n```\n\n## TTL Cache\n\n`TTLCache` is very similar to `LRUCache`, with the distinction that it marks\nvalues as expired if they are too old.\n\n```python\nfrom time import sleep\nfrom power_cache import TTLCache\n\ncache = TTLCache(capacity=3, ttl=120)  # Values valid only for 2 minutes\n\n# We can also specify key & value types if we are using `mypy` or `pytypes`\ncache = TTLCache[str, int](capacity=3, ttl=120)\n\ncache[\'the answer to everything\'] = 42\ncache[\'the answer to everything\']  # returns 42\n\ncache[\'a\'] = 1\ncache[\'b\'] = 2\ncache[\'c\'] = 3\n\n# Raises KeyError, because the key was the least recently used, and the capacity\n# is only 3, so the previous value was evicted.\ncache[\'the answer to everything\']\n\nassert len(cache) == 3\n\ncache.evict_expired()  # We can manually evict all expired values\nassert len(cache) == 3  # Nothing was evicted because values are too recent\n\nsleep(121)\n\n# Now all values are marked as expired, but not evicted automatically, because\n# that would spend too much CPU time.\nassert len(cache) == 3\n\ncache.evict_expired()  # We can manually evict all expired values\nassert len(cache) == 0\n```\n\n## Memoize\n\n```python\nfrom power_cache import Memoize\n\n# Runtime annotations are preserved.\n# `capacity` must be always specified, while `cache_type` is "lru" by default.\n@Memoize(capacity=3, cache_type="lru")\ndef my_function(): ...\n\n@Memoize(capacity=3, cache_type="ttl", ttl=120)\ndef another_function(): ...\n```\n\n## AsyncMemoize\n\n```python\nfrom power_cache import AsyncMemoize\n\n# Runtime annotations are preserved.\n# `capacity` must be always specified, while `cache_type` is "lru" by default.\n@AsyncMemoize(capacity=3, cache_type="lru")\nasync def my_function(): ...\n\n@AsyncMemoize(capacity=3, cache_type="ttl", ttl=120)\nasync def another_function(): ...\n```\n',
    'author': 'Andres Correa Casablanca',
    'author_email': 'castarco@coderspirit.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Coder-Spirit/power_cache',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
