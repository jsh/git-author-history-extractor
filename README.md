Simple git author data extractor.

Travels across multiple repositories of git logs to see who was working on the repositories and when.
 
# Requirements

Python 3.8+ required.

You need to install tabulate package first

```bash
    python -m pip install tabulate
```

Usage
-----

Check out all git repositories under a single folder.

Then run:

```bash
githistory.py path_to_repos/*
```

It will 

* Output info to stdout

* Write `authors.csv` as an overview of all authors

Example output
--------------

The script gives you something like this:

```
All authors

Name                         Name                                        First commit         Last commit            Commit count  Repos
---------------------------  ------------------------------------------  -------------------  -------------------  --------------  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
X Y                          x@xeample.com                               2010-12-03 20:49:34  2010-12-03 20:47:15               2  repo1, another repo
Z Z                          z@example.com                               2011-03-30 01:39:36  2011-02-03 20:55:27              42  repo1
```

License
-------

MIT
