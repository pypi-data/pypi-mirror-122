import setuptools

with open('README.md', 'r', encoding='utf-8') as fl:
    long_description = fl.read()

setuptools.setup(
    name = 'zhang_hello',
    version = '1.0.5',
    author = 'Zhang',
    license = 'MIT',
    packages = ['zhang_hello'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    description = 'My first setup files',
    )