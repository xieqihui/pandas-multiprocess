import sys
from setuptools import setup

requirements = [
    'numpy',
    'pandas',
    'tqdm'
]
test_requirements = [
    'pytest'
]
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
setup_requires = ['pytest-runner>=2.0,<3.0'] if needs_pytest else []


setup(
    name='pandas_multiprocess',
    version='0.1.3',
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
    setup_requires=setup_requires,
    python_requires='>=2.7'
)
