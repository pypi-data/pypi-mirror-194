# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['datacls']
install_requires = \
['dtyper', 'xmod']

setup_kwargs = {
    'name': 'datacls',
    'version': '4.6.0',
    'description': '🗂 Take the edge off `dataclass` 🗂',
    'long_description': '`dataclasses` is almost perfect.\n\n`datacls` is a tiny, thin wrapper around `dataclass.dataclasses` making it\na bit more self-contained, reflective, and saving a bit of typing.\n\n`datacls` is exactly like `dataclass`, except:\n\n  * Adds three new instance methods: `asdict()`, `astuple()`, `replace()`,\n    and one new class method, `fields()`, all taken from the `dataclasses`\n    module\n\n  * `xmod`-ed for less cruft (so `datacls` is the same as `datacls.dataclass`)\n\n  * The default class is `datacls.immutable` where `frozen=True`.\n\n## Example\n\n    import datacls\n\n    @datacls\n    class One:\n        one: str = \'one\'\n        two: int = 2\n        three: dict = datacls.field(dict)\n\n    # `One` has three instance methods: asdict(), astuple(), replace()\n\n    o = One()\n    assert o.asdict() == {\'one\': \'one\', \'two\': 2, \'three\': {}}\n\n    import dataclasses\n    assert dataclasses.asdict(o) == o.asdict()\n\n    assert o.astuple() == (\'one\', 2, {})\n\n    o2 = o.replace(one=\'seven\', three={\'nine\': 9})\n    assert o2 == One(\'seven\', 2, {\'nine\': 9})\n\n    # `One` has one new class method: fields()\n\n    assert [f.name for f in One.fields()] == [\'one\', \'two\', \'three\']\n\n    # @datacls is immutable.\n\n    try:\n        o.one = \'three\'\n    except AttributeError:\n        pass\n    else:\n        raise AttributeError(\'Was mutable!\')\n\n    # Usec @datacls.mutable or @datacls(frozen=False)\n    # for mutable classes\n\n    @datacls.mutable\n    class OneMutable:\n        one: str = \'one\'\n        two: int = 2\n        three: Dict = datacls.field(dict)\n\n    om = OneMutable()\n    om.one = \'three\'\n    assert str(om) == "OneMutable(one=\'three\', two=2, three={})"\n\n    # These four new methods won\'t break your old dataclass by mistake:\n    @datacls\n    class Overloads:\n        one: str = \'one\'\n        asdict: int = 1\n        astuple: int = 1\n        fields: int = 1\n        replace: int = 1\n\n    o = Overloads()\n\n    assert ov.one == \'one\'\n    assert ov.asdict == 1\n    assert ov.astuple == 1\n    assert ov.fields == 1\n    assert ov.replace == 1\n\n    # You can still access the methods as functions on `datacls`:\n    assert (\n        datacls.asdict(ov) ==\n        {\'asdict\': 1, \'astuple\': 1, \'fields\': 1, \'one\': \'one\', \'replace\': 1}\n    )\n\n\n### [API Documentation](https://rec.github.io/datacls#datacls--api-documentation)\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rec/datacls',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
