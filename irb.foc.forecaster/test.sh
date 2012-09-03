#!/bin/bash
python -m unittest discover -s './foc/forecaster/tests' -p '*.py'
python -m unittest discover -s './dracula/test' -p '*.py'
