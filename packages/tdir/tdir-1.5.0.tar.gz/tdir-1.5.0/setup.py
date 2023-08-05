# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tdir']
install_requires = \
['dek>=1.0.2,<2.0.0', 'xmod>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'tdir',
    'version': '1.5.0',
    'description': '🗃 Create and fill a temporary directory 🗃',
    'long_description': "# 🗃 tdir - create and fill a temporary directory 🗃\n\nRun code inside a temporary directory filled with zero or more files.\n\nVery convenient for writing tests: you can decorate individual tests or a whole\ntest suite.\n\n`tdir()` runs code in a temporary directory pre-filled with files: it can\neither be used as a context manager, or a decorator for functions or classes.\n\n`tdir.fill()` is a tiny function that recursively fills a directory.\n\n## Example: as a context manager\n\n    from pathlib import Path\n    import tdir\n\n    cwd = Path.cwd()\n\n    # Simplest invocation.\n\n    with tdir():\n       # Do a lot of things in a temporary directory\n\n    # Everything is gone!\n\n    # With a single file\n    with tdir('hello') as td:\n        # The file `hello` is there\n        assert Path('hello').read_text() = 'hello\\n'\n\n        # We're in a temporary directory\n        assert td == Path.cwd()\n        assert td != cwd\n\n        # Write some other file\n        Path('junk.txt').write_text('hello, world\\n')\n\n    # The temporary directory and the files are gone\n    assert not td.exists()\n    assert cwd == Path.cwd()\n\n    # A more complex example:\n    #\n    with tdir(\n        'one.txt',\n        three='some information',\n        four=Path('existing/file'),  # Copy a file into the tempdir\n        sub1={\n            'file.txt': 'blank lines\\n\\n\\n\\n',\n            'sub2': [\n                'a', 'b', 'c'\n            ]\n        },\n    ):\n        assert Path('one.txt').exists()\n        assert Path('four').read_text() == Path('/existing/file').read_text()\n        assert Path('sub1/sub2/a').exists()\n\n    # All files gone!\n\n## Example: as a decorator\n\n    from pathlib import Path\n    import tdir\n    import unittest\n\n    @tdir\n    def my_function():\n        pass  # my_function() always operates in a temporary directory\n\n\n    # Decorate a TestCase so each test runs in a new temporary directory\n    # with two files\n    @tdir('a', foo='bar')\n    class MyTest(unittest.TestCast):\n        def test_something(self):\n            assert Path('a').read_text() = 'a\\n'\n\n        def test_something_else(self):\n            assert Path('foo').read_text() = 'bar\\n'\n\n\n    class MyTest2(unittest.TestCast):\n        # Decorate just one test in a unitttest\n        @tdir(foo='bar', baz=bytes(range(4)))  # binary files are possible\n        def test_something(self):\n            assert Path('foo').read_text() = 'bar\\n'\n            assert Path('baz').read_bytes() = bytes(range(4)))\n\n        # Run test in an empty temporary directory\n        @tdir\n        def test_something_else(self):\n            assert not Path('a').exists()\n            assert Path().absolute() != self.ORIGINAL_PATH\n\n        ORIGINAL_PATH = Path().absolute()\n\n\n### [API Documentation](https://rec.github.io/tdir#tdir--api-documentation)\n",
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
