DidYouKnow?
============

Welcome to Python's source of knowledge - DidYouKnow?

It is a Python library for accessing open data APIs in an easy-to-use, pythonic nature.

Key features (not all accessible a.t.m.):

 - easy access to data APIs (for starters the World Bank API)
 - user-friendly data selection (through smart argument parsing)
 - data represented as Pandas DataFrames
 - caching


Installation
------------
Requirements:
 - pymongo
 - pandas
 - matplotlib

Usage
-----
Run an ipython interpreter from within the cloned git repo:

    ipython --pylab=inline

(it can also be a notebook)

    ipython notebook --pylab=inline

Then enter this example code to see the basic functionality:

    from didyouknow.extractor import Extractor
    
    e = Extractor()
    print(e.arg())
    
    countries = e.grab(e.arg())
    for country in countries:
        for indicator in arg['indicator_codes']:
            country.get_indicator_pandas(indicator).plot()
    
You can change the `arg` object to select other indicators and countries.