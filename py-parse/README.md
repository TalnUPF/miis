# Surface/Deep parser 

This repo contains a program for parsing text to surface syntax (and deep syntax, optionally). The program is composed by:
- A main script (parse.py)
- A client module for the surface parser (clients/transition_client.py)
- A client module for the deep parser (clients/mate_client.py)
- A utility module for dealing with conll structures (clients/conll.py)

You'll need Python 2.7 installed.

The usage, showed running 'python parse.py -h', is as follows:
```
usage: parse.py [-h] [-s SAVE_DIR] [-d] FILE [FILE ...]

Parses plain text files using TALN web service.

positional arguments:
  FILE                  the file[s] to process.

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE_DIR, --save_dir SAVE_DIR
                        Store the parsing result into the supplied directory
                        location.
  -d, --deep_parse      Do also the deep parsing of the text.
```

Also, within this repo, you'll find the samples directory, containing a set of sample text files.
For example, you can execute 'python parse.py -s output -d samples/test3.txt'. This execution should create an 'output' directory containing two files:

- test3.surface.conll, containing the surface parse result.
- test3.deep.conll, containing the deep parse result (as the -d flag was set).



