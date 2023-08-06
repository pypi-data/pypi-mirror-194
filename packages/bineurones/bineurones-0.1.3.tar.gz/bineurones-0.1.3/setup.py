from setuptools import find_packages, setup

VERSION = '0.1.3'
PACKAGE_NAME = 'bineurones'
AUTHOR = 'Guillermo Leira Temes'
AUTHOR_EMAIL = 'guilleleiratemes@gmail.com'
URL = 'https://github.com/Guille-ux'

LICENSE = 'GPL'
DESCRIPTION = 'a libary to create neurones with two inputs'

INSTALL_REQUIRES = [
      'numpy'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=None,
    long_description_content_type=None,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
