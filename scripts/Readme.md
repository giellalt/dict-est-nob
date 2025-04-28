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

Run with `--analyse` to use analysers to try to find missing poses from analysis.

### Prerequisites

You must have a Norwegian and Estonian analyser installed on the system,
in the path where the `giella-nob` and `giella-est` apertium nightly packages
reside, which is in `/usr/share/giella/[nob,est]/...`.

To install them on an *apt* based system:

```
sudo apt-get install giella-nob giella-est
```

### Running

The script will try to use the `hfst` python package to run fst operations,
and fall back to try the `pyhfst` python package, if `hfst` is not found.

If you are using `uv`, you can specify dependencies to run the script with, using the `--with PACKAGE` argument to `uv run`, for example:

```
uv run --with hfst estnob2xml.py ../inc/est_nor_2005_utf8.txt --analyse
```

### Troubleshooting

_No solution found when resolving --with dependencies_: This can happen if your python version is not compatible with the python versions that the `hfst` package requires. Try using a specific python version that is known to work. With `uv`, you can specify which python version to use, with the `--python VERISON` argument to `uv run`, for example:

```
uv run --python 3.12 --with hfst estnob2xml.py ../inc/est_nor_2005_utf8.txt --analyse
```
