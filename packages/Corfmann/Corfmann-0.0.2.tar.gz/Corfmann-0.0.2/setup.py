import setuptools

VERSION = '0.0.2'
DESCRIPTION = 'Corfmann package'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Corfmann',
    version=VERSION,
    author='Edgar Navasardyan',
    author_email='rips.arutyunyan@mail.com',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/navasardyan.edgar/corfmann',
    packages=['corfmann'],
    install_requires=[],
    keywords=[]
)