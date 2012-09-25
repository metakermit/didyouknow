Installation
============
For development purposes, cd to the parent of the directory where this package's setup.py script (irb.foc.forecaster) and do a:

    sudo pip install -e irb.foc.forecaster/


Basic usage
============
You can now try playing with dracula to make sure everything is working:

    from dracula.extractor import Extractor
    extractor = Extractor()
    this = extractor.arg()
    this["country_codes"] = ["hrv", "usa", "esp"]
    countries = extractor.fetch(this)
    print(countries)

To enable caching you first need to install [MongoDB][] locally
or on a remote server.


Getting metadata
=================
You can get e.g. a list of countries by doing a:

    extractor.grab_metadata("countries")

[MongoDB]: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-debian-or-ubuntu-linux/ 