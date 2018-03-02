# mkctf

## Why ?

This tool might help your team to create challenges following a predefined format.

##  Origins

This project was, initially, created for managing file for INS'hAck 2017 event.
You can find challenges and CTF framework [here](https://github.com/HugoDelval/inshack-2017).

This project was updated for INS'hAck 2018 event.

## Getting started

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/pdautry/mkctf/master/install.sh)"
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

## What you need to understand

`mkctf` helps you manipulate two CTF concepts described bellow. These objects
rely on YAML configuration files.

### Repository

Represents a collection of categories which contain instances of `Challenge`.

**How is it configured?**

```
categories: [bugbounty, crypto, for, misc, prog, pwn, re, web, quest]
directories:
  public: [public-files]
  private: [server-files, exploit, src]
files:
  build: build
  deploy: deploy
  status: exploit/exploit
  config:
    challenge: .mkctf.yml
  txt: [writeup.md, Dockerfile, public-files/description.md]
flag:
  prefix: 'INSA{'
  suffix: '}'
name: INS'hAck 2018
```

+ `categories`: categories to be used to classify CTF challenges
+ `directories`: folders to be created for each challenge
    + `public`: exportable folders
    + `private`: non-exportable folders
+ `files`: files to be created for each challenge
    + `build`: a _script_ used to build a challenge
    + `deploy`: a _script_ used to deploy a challenge
    + `status`: a _script_ used to test the availability of the
                challenge. It's usually an exploit
    + `config`: configuration-related files
        + `challenge`: challenge configuration file name usually `.mkctf.yml`
    + `txt`: list of non-executable mandatory files
+ `flag`: flag properties
    + `prefix`: flag's prefix usually ends with `{`
    + `suffix`: flag's suffix usually a single `}`
+ `name`: CTF's name

**Scripts**

Scripts like `build`, `deploy` and `status` are expected to behave according to
the following rules:

+ a _script_ **cannot take mandatory arguments**.
+ a _script_ must have a **return code of 0** when it succeeds, _other
  behavior will be considered as a failure_.
+ a _script_ **must complete its execution within 4 seconds**.

### Challenge

Represents a CTF challenge.

**How is it configured?**

```
category: for
enabled: false
flag: INSA{[redacted]}
name: Virtual Printer
parameters: {}
points: 100
slug: virtual-printer
standalone: false
```

+ `category`: challenge's category
+ `enabled`: is the challenge enabled?
+ `flag`: challenge's flag
+ `name`: challenge's name
+ `parameters`: _dict_ of challenge-specific parameters
+ `points`: challenge's value
+ `slug`: challenge's slug (should match challenge folder name)
+ `standalone`: is the challenge standalone? (meaning it does not rely on a server)
