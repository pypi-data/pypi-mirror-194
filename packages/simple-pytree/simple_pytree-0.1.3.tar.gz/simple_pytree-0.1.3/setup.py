# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_pytree']

package_data = \
{'': ['*']}

install_requires = \
['jax', 'jaxlib']

setup_kwargs = {
    'name': 'simple-pytree',
    'version': '0.1.3',
    'description': '',
    'long_description': '\n<!-- codecov badge -->\n[![codecov](https://codecov.io/gh/cgarciae/simple-pytree/branch/main/graph/badge.svg?token=3IKEUAU3C8)](https://codecov.io/gh/cgarciae/simple-pytree)\n\n\n# Simple Pytree\n\nA _dead simple_ Python package for creating custom JAX pytree objects.\n\n* Strives to be minimal, the implementation is just ~100 lines of code\n* Has no dependencies other than JAX\n* Its compatible with both `dataclasses` and regular classes\n* It has no intention of supporting Neural Network use cases (e.g. partitioning)\n\n<details><summary>What about Equinox, Treeo, etc?</summary>\n\nMost pytree-based neural network libraries start simple but end up adding\na lot of features that are not needed for simple pytree objects. `flax.struct.PytreeNode`\nis the simplest one out there, but it has two downsides:\n\n1. Forces you to use `dataclasses`, which is not a bad thing but not always\nwhat you want.\n2. It requires you to install `flax` just to use it.\n\n</details>\n\n## Installation\n\n```bash\npip install simple-pytree\n```\n\n## Usage\n\n```python\nimport jax\nfrom simple_pytree import Pytree\n\nclass Foo(Pytree):\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\nfoo = Foo(1, 2)\nfoo = jax.tree_map(lambda x: -x, foo)\n\nassert foo.x == -1 and foo.y == -2\n```\n\n### Static fields\nYou can mark fields as static by assigning `static_field()` to a class attribute with the same name \nas the instance attribute:\n\n```python\nimport jax\nfrom simple_pytree import Pytree, static_field\n\nclass Foo(Pytree):\n    y = static_field()\n    \n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\nfoo = Foo(1, 2)\nfoo = jax.tree_map(lambda x: -x, foo) # y is not modified\n\nassert foo.x == -1 and foo.y == 2\n```\n\nStatic fields are not included in the pytree leaves, they\nare passed as pytree metadata instead.\n\n### Dataclasses\nYou can seamlessly use the `dataclasses.dataclass` decorator with `Pytree` classes.\nSince `static_field` returns instances of `dataclasses.Field` these it will work as expected:\n\n```python\nimport jax\nfrom dataclasses import dataclass\nfrom simple_pytree import Pytree, static_field\n\n@dataclass\nclass Foo(Pytree):\n    x: int\n    y: int = static_field(2) # with default value\n    \nfoo = Foo(1)\nfoo = jax.tree_map(lambda x: -x, foo) # y is not modified\n\nassert foo.x == -1 and foo.y == 2\n```\n\n### Mutability\n`Pytree` objects are immutable by default after `__init__`:\n\n```python\nfrom simple_pytree import Pytree, static_field\n\nclass Foo(Pytree):\n    y = static_field()\n    \n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\nfoo = Foo(1, 2)\nfoo.x = 3 # AttributeError\n```\nIf you want to make them mutable, you can use the `mutable` argument in class definition:\n\n```python\nfrom simple_pytree import Pytree, static_field\n\nclass Foo(Pytree, mutable=True):\n    y = static_field()\n    \n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\nfoo = Foo(1, 2)\nfoo.x = 3 # OK\n```\n\n### Replacing fields\n\nIf you want to make a copy of a `Pytree` object with some fields modified, you can use the `.replace()` method:\n\n```python\nfrom simple_pytree import Pytree, static_field\n\nclass Foo(Pytree):\n    y = static_field()\n    \n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\nfoo = Foo(1, 2)\nfoo = foo.replace(x=10)\n\nassert foo.x == 10 and foo.y == 2\n```\n\n`replace` works for both mutable and immutable `Pytree` objects. If the class\nis a `dataclass`, `replace` internally use `dataclasses.replace`.\n\n',
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
