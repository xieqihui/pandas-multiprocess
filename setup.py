import sys
from setuptools import setup

requirements = [
    'numpy',
    'pandas'
]
test_requirements = [
    'pytest'
]
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
setup_requires = ['pytest-runner'] if needs_pytest else []


setup(
    name='pandas_multiprocess',
    version='0.1.0',
    author='Qihui Xie',
    author_email='xieqihui@gmail.com',
    maintainer='Qihui Xie',
    maintainer_email='xieqihui@gmail.com',
    url='https://github.com/xieqihui/pandas-multiprocess',
    license="LICENSE.txt",
    description='Multiprocessing Support for Pandas DataFrame',
    long_description='Multiprocessing Support for Pandas DataFrame',
    packages=['pandas_multiprocess'],
    install_requires=requirements,
    tests_require=test_requirements,
    setup_requires=setup_requires
)
