# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shelved_cache']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.2,<6.0.0']

setup_kwargs = {
    'name': 'shelved-cache',
    'version': '0.3.1',
    'description': 'Persistent cache for Python cachetools.',
    'long_description': '# Shelved Cache\n\n[![Tests](https://github.com/mariushelf/shelved_cache/actions/workflows/cicd.yaml/badge.svg)](https://github.com/mariushelf/shelved_cache/actions/workflows/cicd.yaml)\n[![codecov](https://codecov.io/gh/mariushelf/shelved_cache/branch/master/graph/badge.svg)](https://codecov.io/gh/mariushelf/shelved_cache)\n[![PyPI version](https://badge.fury.io/py/shelved_cache.svg)](https://pypi.org/project/shelved_cache/)\n\nPersistent cache implementation for Python\n[cachetools](https://github.com/tkem/cachetools/).\n\nBehaves like any `Cache` implementation, but entries are persisted to disk.\n\nOriginal repository: [https://github.com/mariushelf/shelved_cache](https://github.com/mariushelf/shelved_cache)\n\n# Usage example\n\n```python\nfrom shelved_cache import PersistentCache\nfrom cachetools import LRUCache\n\nfilename = \'mycache\'\n\n# create persistency around an LRUCache\npc = PersistentCache(LRUCache, filename=filename, maxsize=2)\n\n# we can now use the cache like a normal LRUCache.\n# But: the cache is persisted to disk.\npc["a"] = 42\npc["b"] = 43\n\nassert pc["a"] == 42\nassert pc["b"] == 43\n\n# close the file\npc.close()\n\n# Now in the same script or in another script, we can re-load the cache:\npc2 = PersistentCache(LRUCache, filename=filename, maxsize=2)\nassert pc2["a"] == 42\nassert pc2["b"] == 43\n```\n\n## Use as a decorator\n\nJust like a regular `cachetools.Cache`, the `PersistentCache` can be used with\n`cachetools`\' `cached` decorator:\n\n```python\nimport cachetools\nfrom shelved_cache import PersistentCache\nfrom cachetools import LRUCache\n\nfilename = \'mycache\'\npc = PersistentCache(LRUCache, filename, maxsize=2)\n\n@cachetools.cached(pc)\ndef square(x):\n    print("called")\n    return x * x\n\nassert square(3) == 9\n# outputs "called"\nassert square(3) == 9\n# no output because the cache is used\n```\n\n\n# Features\n\n## persistent cache\n\nSee usage examples above.\n\n## Async decorators\n\nThe package contains equivalents for `cachetools`\' `cached` and `cachedmethod`\ndecorators which support wrapping async methods. You can find them in the `decorators`\nsubmodule.\n\nThey support both synchronous *and* asynchronous functions and methods.\n\nExamples:\n```python\nfrom shelved_cache import cachedasyncmethod\nfrom cachetools import LRUCache\n\nclass A:\n    # decorate an async method:\n    @cachedasyncmethod(lambda self: LRUCache(2))\n    async def asum(self, a, b):\n        return a + b\n\na = A()\nassert await a.asum(1, 2) == 3\n    \nclass S:\n    @cachedasyncmethod(lambda self: LRUCache(2))\n    def sum(self, a, b):\n        return a + b\n\ns = S()\nassert s.sum(1, 2) == 3\n```\n\n\n## Support for lists as function arguments\n\nUsing the `autotuple_hashkey` function, list arguments are automatically converted\nto tuples, so that they support hashing.\n\nExample:\n```python\nfrom cachetools import cached, LRUCache\nfrom shelved_cache.keys import autotuple_hashkey\n\n@cached(LRUCache(2), key=autotuple_hashkey)\ndef sum(values):\n    return values[0] + values[1]\n\n# fill cache\nassert sum([1, 2]) == 3\n\n# access cache\nassert sum([1, 2]) == 3\n```\n\n\n# Changelog\n\n## 0.3.0\n\n* add support for Python 3.10 and 3.11\n* better error message when trying to use the same file for multiple caches\n* CI/CD pipeline\n* fixes for documentation\n\n## 0.2.1\n* improved error handling\n\n# Acknowledgements\n\n* [cachetools](https://github.com/tkem/cachetools/) by Thomas Kemmer\n* [asyncache](https://github.com/hephex/asyncache) by hephex\n\n\n# License\n\nAuthor: Marius Helf ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))\n\nLicense: MIT -- see [LICENSE](LICENSE)\n',
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mariushelf/shelved_cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
