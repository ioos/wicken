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
@file dogma.py
@date 06/03/13
@description The dogma module provides a metaclass based approach to mapping a flat name 
space for class properties to any storage format and metadata schema. Example classes are
implemented for a dictionary storage. A particular mapping from the flat namespace used for
the properties to the metadata schema must be provided at runtime. 
'''

import re
from exceptions import DogmaGetterSetterException
from exceptions import DogmaMetaClassException
from exceptions import DogmaDeleteException

class Tenets(object):
    def __init__(self, belief, teaching, doc, options=None):
        '''
        belief is a string which will become a property of a particular dogma object
        teaching is the string, collection or object that is used by the _set and 
        _get method of this Dogma to map a belieft about what a metadata element should be 
        called by IOOS to a particular schema, say ISO XML or NetCDF CF.
        '''
        self.belief = belief
        self.teaching = teaching
        self.__doc__ = doc
        self.options = options or {}
        

    def __get__(self, dogma, objtype=None):
        try:
            return dogma._get(self.teaching, self.options)
        except Exception as ex:
            exception_string = ''
            exception_string += '''Error getting the '%s' property of the class '%s'\n''' % (self.belief, dogma.__class__.__name__)
            #exception_string += '''Instance data object status: '%s'\n''' % dogma._dataObject
            exception_string += '''Get operation raised exception: '%s' ''' % ex.__repr__()
            raise DogmaGetterSetterException(exception_string)
        
        
    def __set__(self, dogma, value):
        try:
            dogma._set(self.teaching, value, self.options)
        except Exception as ex:
            exception_string = ''
            exception_string += '''Error setting the '%s' property of the class '%s'\n''' % (self.belief, dogma.__class__.__name__)
            #exception_string += '''Instance data object status: '%s'\n''' % dogma._dataObject
            exception_string += '''Set operation raised exception: '%s' ''' % ex.__repr__()
            raise DogmaGetterSetterException(exception_string)
        
    def __delete__(self, dogma):
        try:
            dogma._del(self.teaching, self.options)
        except Exception as ex:
            exception_string = ''
            exception_string += '''Error deleting the '%s' property of the class '%s'\n''' % (self.belief, dogma.__class__.__name__)
            #exception_string += '''Instance data object status: '%s'\n''' % dogma._dataObject
            exception_string += '''Delete operation raised exception: '%s' ''' % ex.__repr__()
            raise DogmaDeleteException(exception_string)
            
            
class MetaReligion(type):
    """
    Designed for working with metadata and all of the strong personal convictions that go
    with it, 
    """

    def __call__(cls, religion, beliefs, *args, **kwargs):
        '''
        cls is the base class which new properties will be added to
        religion is the unique prefix for that class and its beliefs (properties)
        beliefs is a dictionary that maps property names (IOOS metadata) to a particular schema (ISO, CF, etc) 
        
        @TODO - store the clsTypes so that they are only generated once - but how are they identified?
        '''
        clsName = religion + cls.__name__
        clsDict={}
        
        if re.match('^[\w-]+$', religion) is None:
                raise DogmaMetaClassException('''Blasphemy! The name of your metadata religion (class name prefix: '%s') must be alpha numeric with no whitespace''' % religion)
        
        clsDict['_religion'] = religion
        clsDict['_beliefs'] = beliefs
        clsDict['_fixup_belief'] = cls._fixup_belief
        
        for origbelief, teaching in beliefs.iteritems():
        
            belief, opts = cls._fixup_belief(origbelief)

            if isinstance(teaching, dict):
                # store old name
                teaching['original_name'] = origbelief

                doc      = teaching.get('desc', '')
                teaching = teaching['query']
            else:
                doc      = cls._create_doc(belief, teaching)

            # use a class method from the Dogma class to validate/transform the teaching
            teaching = cls._validate_teaching(belief, teaching, *args, **kwargs)

            clsDict[belief] = Tenets(belief, teaching, doc=doc, options=opts)
        
        
        valid_propery_names = tuple(beliefs.keys())
        
        def obj_setter(self, k, v):
            if not k.startswith('_') and k not in valid_propery_names:
                raise AttributeError('''Blasphemy! You can't create the new beliefs (property %s) on an instance of %s - only god can create properties when the class is defined''' % (k, clsName))
            super(Dogma, self).__setattr__(k, v)

        clsDict['__setattr__'] = obj_setter
        
                
        clsType = MetaReligion.__new__(MetaReligion, clsName, (cls,), clsDict)

        # Finally allow the instantiation to occur, but slip in our new class type
        obj = super(MetaReligion, clsType).__call__(religion, beliefs, *args, **kwargs)

        return obj

    @classmethod
    def _fixup_belief(cls, belief):
        """
        Transforms beliefs into valid strings if possible and parses any options.

        Beliefs will always be lowercased.
        If it has spaces, they are converted to underscores ex: "Sensor Names" -> "sensor_names"

        Options:
            Multiple values: a belief with a suffix of "*" will allow multiple values returned from the get
                             when used with MultipleXmlDogma.
        """
        extra = {}
        belief = belief.lower()

        if ' ' in belief:
            belief = belief.replace(' ', '_')

        if belief.endswith("*"):
            belief = belief[:-1]
            extra['multiple'] = True

        # check for invalid characters in the belief which is used as a property name
        if re.match('^[\w-]+$', belief) is None:
            raise DogmaMetaClassException('''blasphemous belief! (property name: '%s') - even god can not make properties with non-alpha-numeric symbols or whitespace''' % belief)

        if belief.startswith('_'):
            raise DogmaMetaClassException('''Blasphemous belief! (property name: '%s') - even god can not make properties that start with an underscore''' % belief)

        return belief, extra

class Dogma(object):
    __metaclass__ = MetaReligion
    
    def __init__(self, religion, beliefs, dataObject):        
        self._dataObject = dataObject
                
        
    def _get(self, key):
        raise NotImplementedError('_get Method is not implemented in the Dogma Base Class!')
        
    def _set(self, key, value):
        raise NotImplementedError('_set Method is not implemented in the Dogma Base Class!')

    def _del(self, key):
        raise NotImplementedError('_del Method is not implemented in the Dogma Base Class!')
        

    @classmethod
    def _validate_teaching(cls, belief, teaching, *args, **kwargs):
        """
        Default implementation of the validation method for the teaching objects used as 
        keys in the _get and _set methods
        """
        return teaching
        

    @classmethod
    def _create_doc(cls, belief, teaching):
        """
        Default implementation to create a doc string for a tenet
        """
        return '''This is the belief that '%s' is the true name for '%s' as taught by the class %s''' % (belief, teaching, cls.__name__)







