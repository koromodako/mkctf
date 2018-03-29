from distutils.core import setup

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
        'mkctf'
    ],
    package_dir={
        'mkctf': 'mkctf'
    },
    # configuration files
    data_files=[
        ('~/.config', ['config/mkctf.yml']),
        ('~/bin', ['script/mkctf-cli'])
    ]
)
