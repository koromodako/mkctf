from pathlib import Path
from distutils.core import setup

bin_path = Path.home().joinpath('bin')
config_path = Path.home().joinpath('.config')

setup(
    # main information
    name='mkctf',
    version='0.1.0',
    description='',
    author='Paul Dautry',
    author_email='paul.dautry@gmail.com',
    url='https://github.com/pdautry/mkctf',
    # package files
    packages=[
        'mkctf',
        'mkctf.helper',
        'mkctf.object',
        'mkctf.command'
    ],
    # configuration files
    data_files=[
        (str(bin_path), ['script/mkctf-cli']),
        (str(config_path), ['config/mkctf.yml'])
    ]
)
