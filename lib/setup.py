# -*- coding:utf8 -*-
import os
import sys
import codecs
import re
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))
package_requires = [
]
test_requires = [
    'pytest',
    'pytest-pep8',
    'pytest-flakes',
]

# Use README.rst for long description.
readme_path = os.path.join(here, 'README.rst')
long_description = ''
if os.path.exists(readme_path):
    with codecs.open(readme_path, encoding='utf-8') as fp:
        long_description = fp.read()


# Origin URL: http://tell-k.github.io/pyconjp2015/#28
def find_version(*file_paths):
    version_file_path = os.path.join(*file_paths)
    try:
        with codecs.open(version_file_path) as fp:
            version_file = fp.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1)
    except OSError:
        raise RuntimeError("Unable to find version string.")
    raise RuntimeError("Unable to find version string.")


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '--pep8',
            '--flakes',
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class LambdaArchiveCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import tempfile
        import subprocess
        import shutil
        import glob
        import zipfile
        package_dir = tempfile.mkdtemp()
        command = subprocess.Popen(['pip', 'install', '-t', package_dir, '.'])
        command.wait()
        # TODO: anantaの正式登録後は削除する処理
        command = subprocess.Popen(['pip', 'install', '-t', package_dir, './vendor/ananta'])
        command.wait()
        functions_dump_path = os.path.join(package_dir, 'functions.json')
        with open(functions_dump_path , 'w') as fp:
            command = subprocess.Popen('ananta dump -c ./ananta.ini -p sharequiz'.split(' '), stdout=fp)
            command.wait()
        # パッケージの作成
        package_file = './sharequiz.zip'
        with zipfile.ZipFile(package_file, 'w') as zfp:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    if file.endswith('.pyc'):
                        continue
                    fullpath = os.path.join(root, file)
                    itempath = fullpath.replace(package_dir+'/', '')
                    zfp.write(fullpath, itempath)
        shutil.rmtree(package_dir)

setup(
    name='sharequiz',
    version=find_version('sharequiz/__init__.py'),
    url='https://github.com/attakei/deck2pdf',
    description='ShareQuiz Lambda pack',
    long_description=long_description,
    author='attakei',
    author_email='attakei@gmail.com',
    license='MIT',
    classifiers=[
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=package_requires,
    tests_require=test_requires,
    cmdclass={
        'test': PyTest,
        'lambda': LambdaArchiveCommand,
    },
    entry_points={
        "console_scripts": [
        ]
    }
)