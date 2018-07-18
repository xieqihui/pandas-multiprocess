from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pandas_multiprocess',
    version='0.0.2',
    author='Qihui Xie',
    author_email='xieqihui@gmail.com',
    maintainer='Qihui Xie',
    maintainer_email='xieqihui@gmail.com',
    url='https://github.com/xieqihui/pandas-multiprocess',
    license="LICENSE.txt",
    description='Multiprocessing Support for Pandas DataFrame',
    long_description='Multiprocessing Support for Pandas DataFrame',
    packages=['pandas_multiprocess'],
    install_requires=required
)
