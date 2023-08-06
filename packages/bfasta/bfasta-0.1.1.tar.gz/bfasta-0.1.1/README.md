[![check](https://github.com/retospect/bfasta/actions/workflows/check.yml/badge.svg)](https://github.com/retospect/bfasta/actions/workflows/check.yml)
[![PyPI version](https://badge.fury.io/py/bfasta.svg)](https://badge.fury.io/py/bfasta)

# FastA reader

Very simple fastA reader.

```python
from bfasta import FastAreader

reader = FastAreader("myFile.fa")

# If you want to just read the first entry:
header, seq = next(reader.readFasta())

# Read all the entries
# If you want to read all the entries
for header, seq in reader.readFasta():
    # header and seq are now strings here
    print(header)
```

Originally by Dr. B. 
