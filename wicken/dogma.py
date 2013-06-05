#!/usr/bin/env python
'''
@author David Stuebe <dstuebe@asasscience.com>
@file dogma.py
@date 06/03/13
@description The dogma module provides a metaclass based approach to mapping a flat name 
space for class properties to any storage format and metadata schema. Example classes are
implemented for a dictionary storage. A particular mapping from the flat namespace used for
the properties to the metadata schema must be provided at runtime. 
'''

from lxml import etree
from netCDF4 import Dataset


class Tenants(object):
    def __init__(self, belief, teaching, doc=None):
        '''
        belief is a string which will become a property of a particular dogma object
        teaching is the string, collection or object that is used by the _set and 
        _get method of this Dogma to map a belieft about what a metadata element should be 
        called by IOOS to a particular schema, say ISO XML or NetCDF CF.
        '''
        self.belief = belief
        self.teaching = teaching
        if doc: self.__doc__ = doc

    def __get__(self, dogma, objtype=None):
        print '__get__:', self.belief
        return dogma._get(self.teaching)
        
    def __set__(self, dogma, value):
        print '__set__:',self.belief
        dogma._set(self.teaching,value)
        
    def __delete__(self, dogma):
        raise NotImplementedError('Can not delete the %s property!' % self.belief)

class MetaReligion(type):

    def __call__(cls, religion, beliefs, *args, **kwargs):
        '''
        cls is the base class which new properties will be added to
        religion is the unique prefix for that class and its beliefs (properties)
        beliefs is a dictionary that maps property names (IOOS metadata) to a particular schema (ISO, CF, etc) 
        '''
        print 'call: religion: ', religion
        print 'call: beliefs: ', beliefs
        clsName = religion + cls.__name__
        clsDict={}
        clsDict['_religion'] = religion
        clsDict['_beliefs'] = beliefs
        
        
        for belief, teaching in beliefs.iteritems():
            clsDict[belief] = Tenants(belief, teaching)
        
        
        clsType = MetaReligion.__new__(MetaReligion, clsName, (cls,), clsDict)


        # Finally allow the instantiation to occur, but slip in our new class type
        obj = super(MetaReligion, clsType).__call__(religion, beliefs, *args, **kwargs)

        return obj



class Dogma(object):
    __metaclass__ = MetaReligion
    
    def __init__(self, religion, beliefs, dataObject):
        print 'init: religion: ', religion
        print 'init: beliefs: ', beliefs
        print 'init: dataObect', dataObject
        
        self._dataObject = dataObject
        
        
        
    def _get(self, key):
        raise NotImplementedError('_get Method is not implemented in the Dogma Base Class!')
        
    def _set(self, key, value):
        raise NotImplementedError('_set Method is not implemented in the Dogma Base Class!')


class DictionaryDogma(Dogma):
    
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


class XmlDogma(Dogma):
    
    def __init__(self, religion, beliefs, dataObject=None):
    
        if dataObject is None:
            dataObject = etree.Element('root') # ???
            
        if not isinstance(dataObject, etree._Element):
            raise TypeError('XmlDogma only allows XML Element data objects!')

        super(XmlDogma, self).__init__(religion, beliefs, dataObject)   

    def _get(self,xpath_args):        
        return self._dataObject.xpath(*xpath_args).text # Needs testing
        
    def _set(self,key,value):
        element = self._dataObject.xpath(*xpath_args)
        element.text = value


class NetCDFDogma(Dogma):


    def __init__(self, religion, beliefs, dataObject=None):
    
        if dataObject is None: # allow none - what is the title?
            dataObject = Dataset('junk_metadata.nc','w')
            
        if not isinstance(dataObject, Dataset):
            raise TypeError('NetCDFDogma only allows NetCDF4 Dataset data objects!')

        super(NetCDFDogma, self).__init__(religion, beliefs, dataObject)   

    def _get(self,key):        
        try:
            return getattr(self._dataObject,key)
        except AttributeError:
            return None
        
    def _set(self,key,value):
        setattr(self._dataObject,key,value)
        
    def _write(self):
    
        self._dataObject.close()
        
        


