import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.4'
PACKAGE_NAME = 'bineurones'
AUTHOR = 'Guillermo Leira Temes'
AUTHOR_EMAIL = 'guilleleiratemes@gmail.com'
URL = 'https://github.com/Guille-ux'

LICENSE = 'GPL'
DESCRIPTION = 'a libary to create neurones with two inputs'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=None,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
