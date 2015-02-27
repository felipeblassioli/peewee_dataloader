from setuptools import setup, find_packages

setup(
    name='PeeweeDataLoader',
    version='0.0.5',
    url='https://github.com/felipeblassioli/peewee_dataloader',
    author='Felipe Blassioli',
    author_email='felipeblassioli@gmail.com',
    description='Helpers to load that into a Peewee Database',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'peewee>=2.4.5',
        'xlrd>=0.9.3',
        'pymongo'
    ]
)
