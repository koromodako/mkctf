from pathlib import Path
from setuptools import setup, find_packages
from mkctf import __version__

HERE = Path(__file__).absolute().parent
CONF_DIR = Path.home().joinpath('.config')

def requirements():
    with HERE.joinpath('requirements.txt').open() as reqs:
        return list([req.strip() for req in reqs if req.strip()])

setup(
    # main information
    name='mkctf',
    version=__version__,
    description='',
    author='Paul Dautry',
    author_email='koromodako@gmail.com',
    url='https://github.com/koromodako/mkctf',
    # package files
    packages=find_packages(str(HERE)),
    install_requires=requirements(),
    # configuration files
    entry_points={
        'console_scripts': [
            'mkctf-cli = mkctf.main:app',
        ]
    },
    data_files=[(str(CONF_DIR), ['config/mkctf.yml'])]
)
