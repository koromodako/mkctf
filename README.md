# PyChallFactory

## Get started

`python3 py_chall_factory.py [options]` 
or 
`chmod 700 py_chall_factory.py && ./py_chall_factory.py [options]`

Use option `-h` or `--help` to get started.

## All you need to know

First, edit and rename `py_chall_factory.ini.dist` to `py_chall_factory.ini` 

For each challenge a small file tree is created containing the following folders:

 + `src`: put all your challenge resources here. It's like your working folder.
 + `public-files`: every file you put here will be accessible from ctf website.
 + `server-files`: every file you put here will be run on the server like a service.
 + `exploit`: put a working exploit for your challenge for a future write-up publication.

The following files will be created:

 + `flag.txt`: write a unique file on a single line in this one.
 + `writeup.md`: write a WriteUp for your challenge.
 + `public-files/description.md`: write a description of your challenge in this one.
 + `exploit/exploit.py`: write a working exploit in this one.
