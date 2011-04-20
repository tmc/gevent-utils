from setuptools import setup

__version__ = (0, 0, 2)

setup(
    name = 'gevent_utils',
    version = '.'.join([str(x) for x in __version__]),
    py_modules = ['gevent_utils'],
    author = 'Travis Cline',
    author_email = 'travis.cline@gmail.com',
    description = 'miscellaneous gevent utilities',
    url = 'http://traviscline.github.com/gevent-utils',
)
