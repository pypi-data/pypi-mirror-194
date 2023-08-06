from setuptools import setup
import upander

DESCRIPTION = ""
NAME = 'upander'
AUTHOR = 'Panda'
AUTHOR_EMAIL = 'aaa@example.com'
URL = 'https://example.com'
LICENSE = 'Apache License 2.0'
DOWNLOAD_URL = 'https://example.com'
VERSION = upander.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = None
with open("requirements.txt", "r") as f:
    INSTALL_REQUIRES = f.readlines()

EXTRAS_REQUIRE = {
}

PACKAGES = [
    'upander'
]

CLASSIFIERS = [
    'Programming Language :: Python :: 3 :: Only',
]

with open('README.md', 'r') as fp:
    readme = fp.read()
with open('CONTACT.txt', 'r') as fp:
    contacts = fp.read()
long_description = readme + '\n\n' + contacts

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )