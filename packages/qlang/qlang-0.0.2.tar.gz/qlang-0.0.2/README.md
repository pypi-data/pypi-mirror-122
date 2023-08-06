# Q
A concise, procedural programming language.

# Installation
To install Q from pip, use the command:

```
$ pip install qlang
```

If you want to be able to use q from a shell script, navigate to the directory where `q` is installed and create a symbolic link:

```
ln -s ./cli.py q
```

# Usage
To use Q from a shell script:
```
$ q # run interactive shell
$ q <file> # run file
```

To use Q using the Python API:
```python
from qlang import run, run_text

run_text('<text>') # run text
run('<file>') # run file
```