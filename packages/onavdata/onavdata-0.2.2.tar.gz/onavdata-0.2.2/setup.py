import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="onavdata",
    version="0.2.2",
    author="Organic Navigation",
    author_email="team@organicnavigation.com",
    description=(("Easily import both reference and user-specified datasets "
                  "for navigation system design and testing projects.")),
    packages=['onavdata', 'onavdata.utils'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/onavdata-print-shortnames'],
    install_requires=[
          'toml',
          'pandas',
          'numpy',
          'idelib==3.1.0'
      ],
)
