#!/usr/bin/env python
'''
COPYRIGHT 2013 RPS ASA

This file is part of Wicken.

    Wicken is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Wicken is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Wicken.  If not, see <http://www.gnu.org/licenses/>.

@author David Stuebe <dstuebe@asasscience.com>
@file dictionary_dogma.py
@date 06/03/13
@description DictionaryDogma is a reference implementation for the simplest possible 
application of the dogmatic mapping concept. 
'''

from exceptions import WickenException
import dogma

class DictionaryDogmaException(WickenException):
    """
    An exception class for catching problems in the Dictionary Dogma class
    """
    pass
    


class DictionaryDogma(dogma.Dogma):
    
    def __init__(self, religion, beliefs, dataObject=None):
    
        if dataObject is None:
            dataObject = {}
            
        if not isinstance(dataObject, dict):
            raise TypeError('DictionaryDogma only allows dictionary data objects!')

        super(DictionaryDogma, self).__init__(religion, beliefs, dataObject)   

    def _get(self, key, options=None):
        return self._dataObject[key]
        
    def _set(self,key,value, options=None):
        self._dataObject.__setitem__(key,value)

    def _del(self,key, options=None):
        del self._dataObject[key]


    @classmethod
    def _validate_teaching(cls, belief, teaching, *args, **kwargs):
        """
        Check to make sure the teaching object which will be used as a dictionary key is hashable
        """
        if teaching.__hash__ is None:
            raise DictionaryDogmaException(''''The belief '%s' does not have a hashable teaching '%s' ''' % (belief, teaching ))
        
        return teaching
