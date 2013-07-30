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
@file netcdf_dogma.py
@date 06/03/13
@description Implementation of the Dogma Metadata class for NetCDF IO using NetCDF4-Python
'''

from petulantbear.netcdf_etree import *
import xml_dogma
from exceptions import WickenException

class NetCDFDogmaException(WickenException):
    """
    An exception class for catching problems in the NetCDF Dogma class
    """
    pass

class NetCDFDogma(xml_dogma.XmlDogma):


    def __init__(self, religion, beliefs, dataObject=None):
    
        if not isinstance(dataObject, Dataset):
            raise TypeError('NetCDFDogma only allows NetCDF4 Dataset data objects!')

        root = parse_nc_dataset_as_etree(dataObject)

        super(NetCDFDogma, self).__init__(religion, beliefs, root, namespaces=namespaces)   

        
    @classmethod
    def _validate_teaching(cls, belief, teaching):
        """
        Check to make sure the teaching object which will be used as a dictionary key is hashable
        """
        if not isinstance(teaching, str):
            raise NetCDFDogmaException('The belief "%s " does not have a valid teaching. The Teaching must be an xpath expression string. Received teaching: "%s"' % (belief, teaching))
        
        if teaching.startswith('//'):
            raise NetCDFDogmaException('The belief "%s " does not have a valid teaching. The Teaching must be a unique xpath expression which can not start with "//". Received teaching: "%s"' % (belief, teaching))
        
