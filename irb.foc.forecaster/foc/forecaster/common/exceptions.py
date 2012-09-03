'''
Created on 11. 1. 2012.

@author: kermit
'''

class UnexpectedDataError(Exception): pass

class NotInitializedError(Exception): pass

class MustOverrideError(Exception): pass

class ConfigurationFileError(Exception):
    def __str__(self):
        return "Check your conf.py file!"
