Simple git author data extractor.

Travels across multiple repositories of git logs to see who was working on the repositories and when.
 
# Requirements

Python 3.8+ required.

You need to install GitHistory package first

```bash
    python -m pip install GitHistory tabulate
```

Usage
-----

Check out all git repositories under a single folder.

Then run:

```bash
python githistory.py path_to_repos/*
```

License
-------

MIT