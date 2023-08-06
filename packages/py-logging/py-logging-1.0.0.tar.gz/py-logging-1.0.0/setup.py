from setuptools import setup
from pylogger import __version__

setup(
    name='py-logging',
    url='https://github.com/Szczurowsky/py-loggerr',
    author='Kamil Szczurowski',
    author_email='kamil@szczurowsky.pl',
    packages=['pylogger'],
    version=__version__,
    license='MPL-2.0',
    description='Configurable and easy extendable python logger.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown"
)
