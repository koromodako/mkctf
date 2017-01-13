# PyChallFactory

## Get started

`python3 py_chall_factory.py [options]` 
or 
`chmod 700 py_chall_factory.py && ./py_chall_factory.py [options]`

Use option `-h` or `--help` to get started.

## All you need to know

For each challenge a small file tree is created containing the following folders:

 + `src` : Put all your challenge resources here. It's like your working folder.
 + `chall` : Every file you put here will be integrated to the challenge archive.
 + `exploit` : Put a working exploit for your challenge for a future write-up publication.
 + `flags` : Put files containing flags here. It allows you to quickly change the flags and rebuild the challenge.

The `Makefile` created in the challenge folder can have its `build` rule modified to include specific processing required by your challenge.

Finally, after packaging running `python3 py_chall_factory.py -p`, for each challenge in `challenges/` folder you will have a corresponding ZIP archive and MD5 signature file in `packages/` folder.

## Example

```bash
~/py_chall_factory$> python3 py_chall_factory.py -n
[?] > enter challenge name: challenge-test

See you soon! :)

~/py_chall_factory$> ll challenges/challenge-test/
total 36K
drwxrwxr-x 6 paul paul 4,0K janv. 13 18:44 ./
drwxrwxr-x 3 paul paul 4,0K janv. 13 18:44 ../
drwxrwxr-x 2 paul paul 4,0K janv. 13 18:44 chall/
drwxrwxr-x 2 paul paul 4,0K janv. 13 18:44 exploit/
drwxrwxr-x 2 paul paul 4,0K janv. 13 18:44 flags/
-rw-rw-r-- 1 paul paul 1,1K janv. 13 18:44 Makefile
drwxrwxr-x 2 paul paul 4,0K janv. 13 18:44 src/

~/py_chall_factory$> touch challenges/challenge-test/chall/readme

~/py_chall_factory$> python3 py_chall_factory.py -p
[?] > which challenge do you want to package ? [<package_name>|all]
challenge-test
mkdir challenge-test
cp -r chall/* challenge-test/
zip -r challenge-test.zip challenge-test/
  adding: challenge-test/ (stored 0%)
  adding: challenge-test/readme (stored 0%)
md5sum challenge-test.zip > challenge-test.md5
rm -rf challenge-test

See you soon! :)

~/py_chall_factory$> ll packages/
total 32K
drwxrwxr-x 2 paul paul 4,0K janv. 13 18:45 ./
drwxrwxr-x 6 paul paul 4,0K janv. 13 18:37 ../
-rw-rw-r-- 1 paul paul   53 janv. 13 18:45 challenge-test.md5
-rw-rw-r-- 1 paul paul  350 janv. 13 18:45 challenge-test.zip
```
