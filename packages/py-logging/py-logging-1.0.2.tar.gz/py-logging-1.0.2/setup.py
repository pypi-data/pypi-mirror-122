from setuptools import setup
from pylogging import __version__

setup(
    name='py-logging',
    url='https://github.com/Szczurowsky/py-logging',
    author='Kamil Szczurowski',
    author_email='kamil@szczurowsky.pl',
    packages=['pylogging'],
    version=__version__,
    license='MPL-2.0',
    description='Configurable and easy extendable python logger.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown"
)
