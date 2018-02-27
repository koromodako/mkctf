# mkctf

## Why ?

This tool might help your team to create challenges following a predefined format.

##  Origins

This project was, initially, created for managing file for INS'hAck 2017 event.
You can find challenges and CTF framework [here](https://github.com/HugoDelval/inshack-2017).

This project was updated for INS'hAck 2018 event.

## Getting started

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/pdautry/mkctf/master/install.sh)"
```

You might need to add `~/bin` to your `$PATH` (most of the time you just reload `.profile`)

Then lets say you want to create a CTF for INS'hAck 2018:

```
mkdir inshack-2018
cd inshack-2018
mkctf init
```

Follow the instructions.

You need help: `mkctf -h`

## All you need to know

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
