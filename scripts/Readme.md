# estnob2xml.py

The `estnob2xml.py` script will convert from the text format found in `../inc/est_nor_2005_utf8.txt` to giella-style xml dictionary.

Run it as follows:

```
python estnob2xml.py ../inc/est_nor_2005_utf8.txt
```

If `python` is not found, try `python3`.

If you have `uv` installed, you can also run the script as

```
uv run estnob2xml.py ../inc/est_nor_2005_utf8.txt
```

The output is by default send to standard output, but a file name
can be specified using the `-o` argument. Shell redirection is of course
also possible, e.g.:

```
python estnob2xml.py ../inc/est_nor_2005_utf8.txt -o output.xml
```

Or
```
python estnob2xml.py ../inc/est_nor_2005_utf8.txt > output.xml
```

## Running with pos-finding analyser

Run the script with the `--analyse` argument to use the Estoninan analyser to
look up pos of words. It requires an hfst library to run, and it looks
for the Estoninan analyser from apertium nightly, which is searched for in path
`/usr/share/giella/est/analyser-gt-desc.hfst".
