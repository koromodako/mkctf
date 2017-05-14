# PyChallFactory

## Why ?

This tool might help your team to create challenges following a predefined format.

##  Origins

This project was, initially, created for managing file for INS'hAck 2017 event.
You can find challenges and ctf framework [here](https://github.com/HugoDelval/inshack-2017)

## Getting started

```bash
# [only the first time]
$> python3 py_chall_factory.py configure 
# ... follow configuration process ...
# ------------------------------------------------------------------------------
# create a new challenge 'test' in bugbounty category
$> python3 py_chall_factory.py create
[?] > enter challenge name: test
[?] > enter challenge points: 100
Categories:
    0 - bugbounty
    1 - crypto
    2 - forensics
    3 - misc
    4 - programming
    5 - pwn
    6 - reverse
    7 - web
[?] > please select a category using its number: 0

See you soon! :)
# ------------------------------------------------------------------------------
# list challenges
$> python3 py_chall_factory.py list
Categories:
    0 - bugbounty
    1 - crypto
    2 - forensics
    3 - misc
    4 - programming
    5 - pwn
    6 - reverse
    7 - web
    8 - all (delete all challenges)
[?] > please select a category using its number: 0

Challenges:
    bugbounty:
        test-100

See you soon! :)
# ------------------------------------------------------------------------------
# check content of test-100 folder
$> tree ~/../bugbounty/test-100
~/../bugbounty/test-100
├── exploit
│   └── exploit
├── flag.txt
├── public-files
│   └── description.md
├── server-files
├── src
└── writeup.md

4 directories, 4 files
# ------------------------------------------------------------------------------
# finally delete the 'test' challenge
$> python3 py_chall_factory.py delete
[?] > first, select the category where the challenge you want to delete is.
Categories:
    0 - bugbounty
    1 - crypto
    2 - forensics
    3 - misc
    4 - programming
    5 - pwn
    6 - reverse
    7 - web
    8 - all (search in all categories)
[?] > please select a category using its number: 0

Challenges:
    bugbounty:
        test-100
[?] > now, what is the name of the challenge you want to delete? [<package_name>|all]: test-100
[?] > do you really want to remove </home/paul/documents/informatique/hacking/insecurity/orga/inshack-2017/challenges/bugbounty/test-100> ? [yes/*]
yes

See you soon! :)

```

## All you need to know

First, edit and rename `py_chall_factory.pref.dist` to `py_chall_factory.pref` 

The default configuration creates the following elements:

For each challenge a small file tree is created containing the following folders:

 + `src`: put all your challenge resources here. It's like your working folder.
 + `public-files`: every file you put here will be accessible from ctf website.
 + `server-files`: every file you put here will be run on the server like a service.
 + `exploit`: put a working exploit for your challenge for a future write-up publication.

The following files will be created:

 + `flag.txt`: write a unique file on a single line in this one.
 + `writeup.md`: write a WriteUp for your challenge.
 + `public-files/description.md`: write a description of your challenge in this one.
 + `exploit/exploit`: write a working exploit in this one.