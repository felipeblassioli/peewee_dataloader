from setuptools import setup, find_packages

setup(
    name='PeeweeDataLoader',
    version='0.0.1',
    url='https://github.com/felipeblassioli/peewee_dataloader',
    author='Felipe Blassioli',
    author_email='felipeblassioli@gmail.com',
    description='Helpers to load that into a Peewee Database',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'peewee>=2.4.5',
        'xlrd>=0.9.3'
    ]
)
