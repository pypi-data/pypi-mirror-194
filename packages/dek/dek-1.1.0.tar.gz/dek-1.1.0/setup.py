# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dek']
install_requires = \
['xmod>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'dek',
    'version': '1.1.0',
    'description': '🎴 The decorator-decorator 🎴',
    'long_description': "🗃 `dek` - the decorator-decorator 🗃\n\n`dek` decorates your decorators to diminish defects and drudgery.\n\nWriting a Python decorator which takes no parameters isn't hard.\n\nBut writing a decorator with parameters is less easy - and more work\nif you want to decorate classes, like `unittest.mock.patch` does.\n\n`dek` is a decorator for decorators that does this deftly with a\nsingle tiny function.\n\n## Example 1: a simple decorator with dek\n\nTASK: write a decorator `before` that prints a function's name and its\narguments before it executes.\n\nWith `dek`, it's a few lines:\n\n    import dek\n\n    @dek\n    def before(pfunc):\n        print(pfunc)\n        return pfunc()\n\nDone! To use your new decorator:\n\n    @before\n    def phone(two, four=4):\n        print('Calling', two + two, four * four)\n\n    one(32, four=3)\n\n    # That prints something like:\n    #\n    # functools.partial(<function phone at 0x7fafa8072b00>, 32, four=3)\n    # Calling 64 9\n\n`pfunc` is a [`functools.partial`](\nhttps://docs.python.org/3/library/functools.html#functools.partial),\nwhich represents the function call that `dek` intercepted.  Your code\ncan call `pfunc` as often as you like, or add or change parameters.\n\n## Example 2: same, without `dek`\n\n    import functools\n\n    def before(func):\n        @functools.wraps(func)\n        def wrapped(*args, **kwargs):\n            print(func, args, kwargs)\n            return func(*args, **kwargs)\n\n        return wrapped\n\nWith `dek` it's a bit less work, but the real advantage comes when you have\na decorator with a parameter.\n\n## Example 3: a decorator with a single optional parameter\n\nWrite a decorator `before` that prints a function's name, arguments\n_and a label_ before it executes.\n\nWith `dek`, it's a trivial change from the previous solution.\n\n    import dek\n\n    @dek\n    def before(pfunc, label='dull'):\n        print(label, pfunc.func, *pfunc.args)\n        return pfunc()\n\n    @before\n    def add(x, y):\n        return x + y\n\n    @before(label='Exciting!')\n    def times(x, y):\n        return x * y\n\n    print('Result', add(2, times(2, 3)))\n\n    # Prints:\n    #   Exciting! times 2 3\n    #   dull add 2 6\n    #   Result 8\n\n\n## Example 4: same, without `dek`\n\nWithout `dek` it's actual work that's easy to get wrong.\n\n    import functools\n\n    def before(func=None, label='dull'):\n        if func is not None:\n            @functools.wraps(func)\n            def wrapped(*args, **kwargs):\n                print(label, func.__name, *args)\n                return func(*args, **kwargs)\n\n            return wrapped\n\n        return functools.partial(before, label=label)\n\n\n## Example 5: Deferred mode\n\nFor finer control over function signatures there is deferred mode, which\nlets you select what sort of signature you want to expose with a `wrapped`\nfunction that you create.\n\n    @dek(defer=True)\n    def before(func, label='debug'):\n        def wrapped(foo, bar):\n            print(label, foo, bar)\n            return func(foo, bar)\n\n        return wrapped\n\n## Example 6: Decorating a class\n\nIf you need to decorate methods on a class, there's a `methods` parameter to\nselect which methods get decorated.\n\n\n    import dek\n\n    @dek(methods='test')\n    def before(pfunc):\n        print('HERE', *pfunc.args)\n        return pfunc()\n\n    @before\n    class Class:\n        def test_one(self):\n            return 1\n\n        def test_two(self):\n            return 2\n\n        def three(self):  # This won't get decorated\n            return 1\n\n\n    # Test at the command line:\n    >>> cl = Class()\n    >>> cl.test_one(), cl.test_two(), cl.three()\n    HERE 1\n    HERE 2\n    (1, 2, 3)\n\nNOTES:\n\n[This article](https://medium.com/p/1277a9ed34dc/) talks more about\ndecorators that take parameters and about `dek` in general.\n\nFor your advanced decorator desires, the PyPi module\n[`decorator`](https://github.com/micheles/decorator/blob/master/docs/documentation.md) does not duplicate duties that `dek` does, but does\npretty anything else you could conceive of in a decorator library.\n\n\n### [API Documentation](https://rec.github.io/dek#dek--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
