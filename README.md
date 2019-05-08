# mkctf

## Why ?

This framework aims at helping your team create CTF challenges following format which will enable efficient integration
and deployment on the CTF infrastructure.

This project was, initially, created for managing challenges for INS'hAck 2017 event.
You can find challenges and writeups of the past editions of INS'hAck in [this repository](https://github.com/InsecurityAsso).

This project is constantly evolving to enable even more automation when deploying challenges on a VPS & Docker-based infrastructure.

## Requirements

This project has been design to run in a Linux environment having Python 3.7+ support.

It might work on Mac as well though I'm not testing it on this platform.

I won't invest time to make it work on Windows as WSL2 will enable having a Linux running on your Windows quite easily.

## Installing and Creating a new CTF

I advise you to setup mkctf using the following methodology:

```bash
# clone mkctf repository in tmp directory
$ git clone https://github.com/koromodako/mkctf /tmp/mkctf
# create ~/bin dir if required and enter ~/bin
$ mkdir -p ~/bin && cd ~/bin
# create a Python 3 virtual environment
$ python3 -m venv .mkctf-venv
# install mkctf in the venv
$ .mkctf-venv/bin/pip install /tmp/mkctf
# create symbolic links for mkctf scripts
$ ln -s ./mkctf-venv/bin/mkctf-* .
# leave ~/bin
cd ..
# ensure that config directory exists and copy configuration files in it
$ mkdir -p ~/.config && cp -r /tmp/mkctf/config ~/.config/mkctf
# ensure that ~/bin is part of your path and try invoking mkctf-cli
$ mkctf-cli -h
```

Then lets say you want to create a CTF for INS'hAck 2020:

```bash
# create and enter inshack-2020/
$ mkdir inshack-2020 && cd inshack-2020
# initialize a mkCTF repository
$ mkctf-cli init
# then simply follow the instructions
```

## Commandline tools

- `mkctf-cli` helps you manipulate two concepts described bellow. These concepts rely on YAML configuration files.
- `mkctf-serve` starts a web server exposing an API which will be documented here _soon_.

### Repository

A repository represents a collection of CTF challenges.

**How does it work?**

```

```

### Challenge

Represents a CTF challenge.

**How does it work?**

```
```

### Scripts

Scripts like `build`, `deploy` and `status` are expected to behave according to the following rules:

1. a _script_ **shall not take mandatory arguments**
2. a _script_ **shall execute before a timeout is triggered** which defaults to 60 seconds. `--timeout` option enable you to override this value
3. a _script_ **shall return a code** which will be interpreted according to the following table:

| **exit code** | **status** | **description** |
|:-------------:|:----------:|:----------------|
| `0` | `SUCCESS` | Script succeeded. |
| `2` | `N/A` | Script does not apply/have a meaning to this challenge. |
| `3` | `MANUAL` | Script cannot perform this task entirely, you will have to get your hands dirty. |
| `4` | `NOT IMPLEMENTED` | Script is not implemented. |
| _other values_ | `FAILURE` | Script failed. |

The special status `TIMED-OUT` may occur if your script took too long to execute as explained in `2.`

If the **exit code differs from 0** both _stdout_ and _stderr_ will be printed out.

You can use this behavior to print meaningful instructions/exceptions within these _scripts_ (particularly interesting if your script returns a code `3 (MANUAL)`)
