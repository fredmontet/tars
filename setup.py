from pathlib import Path
from setuptools import find_packages, setup


def read_requirements(path):
    return list(Path(path).read_text().splitlines())


setup(
    name='tars',
    packages=['src.tars'],
    version='0.2.0',
    description='A cryptocurrency trading bot for research',
    author='Fred Montet',
    license='MIT',
    install_requires=[
          read_requirements("requirements.txt")
    ],
)
