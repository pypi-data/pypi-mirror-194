import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

TESTS_REQUIRE = [
    'pytest',
    'httpretty'
]


setup(
    name='xmlrpclib-to',
    version='0.1.2',
    packages=find_packages(),
    tests_require=TESTS_REQUIRE,
    cmdclass={'test': PyTest},
    url='http://github.com/gisce/xmlrpclib-to',
    license='MIT',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='XMLRPC Client with timeout'
)
