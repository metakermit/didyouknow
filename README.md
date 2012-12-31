Welcome to Python's source of knowledge - DidYouKnow? (formerly Dracula)

Key features (to be added):

 - easy access to data APIs (for starters the World Bank API)
 - user-friendly data selection (through smart argument parsing)
 - data represented as Pandas DataFrames
 - caching

Deprecated stuf:

Installation
===========

Ubuntu Linux (or other Debian-based distro)
--------------------------------------
Open a terminal and change directory to the location of this file.

Run the install_dependencies script:

        $ sh install_dependencies.sh

Windows
-------
Best to install the python(x,y) bundle (http://code.google.com/p/pythonxy/).

Afterwards all the packages mentioned in the install_dependencies.sh file can be installed via pip. For example to install xlrd one would issue the following command inside Command Prompt:

        pip install xlrd


Installing Django
---------------
If you want to run the web application, you need to have Django installed.

To install from the Ubuntu repos:

        sudo apt-get install python-django

or to run a dev version:

        git clone git://github.com/django/django.git django-trunk
        sudo pip install -e django-trunk/

Running
=======

Console run
----------

Set the desired preferences in the configuration file:

        ./foc/forecaster/common/conf.py

Write down the crisis/normal years in the XLS file you defined in your conf file, e.g.:

        ./io/crises-imf-banking.xls

Position yourself inside the irb.foc.forecaster folder (pwd output just to show an example of the correct path):

        $ cd irb.foc.forecaster
        $ pwd
        /media/Data/Drazen/Dropbox/dev/eclipse/w2/irb.foc.forecaster

Run the Python interpreter with the entry script console_run.py as an argument:

        python console_run.py

Web app run
----------
Position yourself to the code root (the irb.foc.forecaster/ folder) and run the development server:

         python manage.py runserver

Point your web browser to [http://127.0.0.1:8000/foc](http://127.0.0.1:8000/foc) to see the site. If you want to open it from other computers you can also specify that your server listents to outside connections and a specific port (e.g. 8080):

         python manage.py runserver 0.0.0.0:8080

Local visualisation (matplotlib)
--------------------------------

The options are set in .foc/visualiser/data_presenter/vis_conf.py and the script is run by issuing:

         python console_run.py visualise

Lay of the code
================

console_run.py - the entry point for running the console application (useful for getting the data for example)

dracula - grabs data from various sources (so far only one) available online.
-------

*test* - tests which give nice insight into using the module
\-extractor

*cacher* - responsible to caching to a mongoDB data store.

*extractor* - the entry point to grab the data

*wb* - wrapper for the World Bank API and a parser to a simple model
|- api - communicates with the WB server to get data
|- model - data structures we want the data to be represented in
|    |- country - code and list of indicators
|    \- indicator - internal representation: list of dates, list of values
|
\- parser - called by the api module to form data into Country and Indicator instances


foc.forcaster - main machine learning module, contains all the logic
-----------------------

*common*
|- conf - configuration file with all the preferences that are used in a console run
\- exceptions - all the custom exceptions are defined here

*model* - contains the data structures - DEPRECATED, now part of dracula
|- country - code and list of indicators
\- indicator - internal representation: list of dates, list of values

*sources* - DEPRECATED, now part of dracula
\- wb - extracts data from the World Bank

*ai* - classes regarding pattern recognition, train and test building etc.
|- input - parses XLS files to get crisis and normal period years
|- output - writes the dataset into a text file in a subgroup-discovery-friendly format
|- samples_set - the representation of the train and test datasets that can build samples based on the crisis/normal years input and indicators and countries specified in the conf file; fetches the data live from the World Bank API
|- preprocessor - processes the samples to extract useful features (min, max, slope...)
\- metadata - column labels and data type marks used when writing the dataset

*tests* - unit tests for individual modules inside the module


foc.visualiser - organises data (and locally visualises it if matplotlib is used)
----------------------
*data_organiser* - prepares data so that it's ready for plotting
|- abstract_data_organiser - common functionality for all organisers
\- complete_multigroup_organiser - gets the complete time series and marks multiple groups of data points inside it

*data_presenter* - plots the data organised by the data_organiser using matplotlib
|- matplotlib
|   |- visualiser - entry point for local visualisation
|   |- complete_multigroup_visualisation - one of the implementations of the ivisualisation interface
|   | ...
| 
|- vis_conf - configuration used by the visualiser
\- ivisualisation - common interface any visualisation subclass must adher to by overriding the _create_figure(self, item) method


foc.extra
----------
Some scripts used here and there for some manual tasks.


focweb
------
The Django web application resides here.

io
--
Input and output files should live here not to make a mess elsewere (except for the conf.py files, which are part of the code for now and they have to be importable).

static, templates
----------------
Some parts of the web app. It would be nice if this could go somewhere else - like in focweb/

build, dist, foc_forecaster.egg-info
--------------------------------
Auto-generated files by the pip packaging command.
