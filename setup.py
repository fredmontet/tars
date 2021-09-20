from pathlib import Path
from setuptools import find_packages, setup


def read_requirements(path):
    return list(Path(path).read_text().splitlines())


setup(
    name='tars',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    version='0.5.0',
    description='A crypto trading bot for research and developers',
    author='Fred Montet',
    license='MIT',
    install_requires=[
          read_requirements("requirements.txt")
    ],
    entry_points={
        'console_scripts': [
            'tars = tars.cli:cli',
        ],
    },
)
