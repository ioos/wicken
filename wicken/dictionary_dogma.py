#!/usr/bin/env python
'''
COPYRIGHT 2013 David Stuebe

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
@description The dogma module provides a metaclass based approach to mapping a flat name 
space for class properties to any storage format and metadata schema. Example classes are
implemented for a dictionary storage. A particular mapping from the flat namespace used for
the properties to the metadata schema must be provided at runtime. 
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

    def _get(self,key):        
        return self._dataObject.get(key)
        
    def _set(self,key,value):
        self._dataObject.__setitem__(key,value)

    def _del(self,key):
        del self._dataObject[key]


    @classmethod
    def _validate_teaching(cls, belief, teaching):
        """
        Check to make sure the teaching object which will be used as a dictionary key is hashable
        """
        if teaching.__hash__ is None:
            raise DictionaryDogmaException(''''The teaching '%s' is not hashable for the belief '%s' ''' % (teaching, belief))
        