#!/usr/bin/python3

import sys

from q import run, run_text

if len(sys.argv) == 1:
    while True:       
        text = input('> ')
        if text == 'exit': break
        print(run_text(text))
elif len(sys.argv) == 2:
    run(sys.argv[1])
else:
    print('Usage: q [file]')