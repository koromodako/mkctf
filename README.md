# mkctf

## Why ?

This tool might help your team to create challenges following a predefined format.

##  Origins

This project was, initially, created for managing file for INS'hAck 2017 event.
You can find challenges and writeups of the past editions of INS'hAck [here](https://github.com/InsecurityAsso).

This project was updated for INS'hAck 2018 event.

Version [1](https://github.com/koromodako/mkctf/releases/tag/1.0.0) was used until INS'hAck 2019.

INS'hAck 2019 will be using version [2+](https://github.com/koromodako/mkctf/releases/tag/2.0.0) or above.

## Minimal requirements

 + Python v3.6.5+

## Getting started

```pdautry/mkctf/releases/tag/1.0.0
bash -c "$(curl -fsSL https://raw.githubusercontent.com/koromodako/mkctf/master/scripts/install.sh)"
```

You might need to add `~/bin` to your `$PATH` (most of the time you just reload `.profile`)

Then lets say you want to create a CTF for INS'hAck 2019:

```
mkdir inshack-2019
cd inshack-2019
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
tags: [bugbounty, crypto, for, misc, prog, pwn, re, web, quest]
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
name: INS'hAck 2019
```

+ `tags`: tags used to classify CTF challenges
+ `directories`: folders to be created for each challenge
    + `public`: exportable folders
    + `private`: non-exportable folders
+ `files`: files to be created for each challenge
    + `build`: a _script_ used to build a challenge (cf. Scripts)
    + `deploy`: a _script_ used to deploy a challenge (cf. Scripts)
    + `status`: a _script_ used to test the availability of the
                challenge. It's usually an exploit (cf. Scripts)
    + `config`: configuration-related files
        + `challenge`: challenge configuration file name usually `.mkctf.yml`
    + `txt`: list of non-executable mandatory files
+ `flag`: flag properties
    + `prefix`: flag's prefix, usually ends with `{`
    + `suffix`: flag's suffix, usually a single `}`
+ `name`: CTF's name

### Challenge

Represents a CTF challenge.

**How is it configured?**

```
tags: [for, crypto]
enabled: false
flag: INSA{[redacted]}
name: Virtual Printer
parameters: {}
points: 100
slug: virtual-printer
standalone: false
```

+ `tags`: challenge's tags
+ `enabled`: is the challenge enabled?
+ `flag`: challenge's flag
+ `name`: challenge's name
+ `parameters`: _dict_ of challenge-specific parameters
+ `points`: challenge's value
+ `slug`: challenge's slug (should match challenge folder name)
+ `standalone`: is the challenge standalone? (meaning it does not rely on a server)

### Scripts

Scripts like `build`, `deploy` and `status` are expected to behave according to the following rules:

1. a _script_ **shall not take mandatory arguments**.
2. a _script_ **shall execute before a timeout is triggered** which defaults to 60 seconds. `--timeout` option enable you to override this value.
3. a _script_ **shall return a code** which will be interpreted according to the following table:

| **exit code** | **status** | **description** |
|:-------------:|:----------:|:----------------|
| `0` | `SUCCESS` | Script succeeded. |
| `2` | `N/A` | Script does not apply/have a meaning to this challenge. |
| `3` | `MANUAL` | Script cannot perform this task entirely, you will have to get your hands dirty. |
| `4` | `NOT IMPLEMENTED` | Script is not implemented. |
| _other values_ | `FAILURE` | Script failed. |

The special status `TIMED-OUT` may occur if your script took too long to execute as explained in `2.`.

If the **exit code differs from 0** both _stdout_ and _stderr_ will be printed out. 

You can use this behavior to print meaningful instructions/exceptions within these _scripts_ (particularly interesting if your script returns a code `3 (MANUAL)`).
