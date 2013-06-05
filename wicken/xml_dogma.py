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
@file xml_dogma.py
@date 06/03/13
@description Implementation of the Dogma Metadata class for xml IO using etree
'''

from lxml import etree
import dogma
from exceptions import WickenException

class XmlDogmaException(WickenException):
    """
    An exception class for catching problems in the XML Dogma class
    """
    pass

class XmlDogma(dogma.Dogma):
    
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