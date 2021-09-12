from pathlib import Path
from setuptools import find_packages, setup


def read_requirements(path):
    return list(Path(path).read_text().splitlines())


setup(
    name='tars',
    packages=find_packages(
        where='src',
        exclude=['sample'],
    ),
    package_dir={'': 'src'},
    version='0.3.1',
    description='A cryptocurrency trading bot for research',
    author='Fred Montet',
    license='MIT',
    install_requires=[
          read_requirements("requirements.txt")
    ],
)
