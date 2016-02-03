from __future__ import absolute_import, print_function, division

from netCDF4 import Dataset
from wicken.netcdf_dogma import NetCDFDogma
from lxml import etree


cf_metadata_beliefs = {
    # A map of what you call the metadata property to an xpath expression for it in some convention/encoding
    # typically loaded from a file - a modified version of the IOOS Asset_SOS_MAP spread sheet for example
    'service_provider_institution':"""/ncml:netcdf/ncml:attribute[@name='institution']/@value""",
    'data_conventions':"""/ncml:netcdf/ncml:attribute[@name='institution']/@value""",
    'latitude_units':"""/ncml:netcdf/ncml:variable[@name='latitude']/ncml:attribute[@name='units']/@value""",
    'does_not_exist':"""/ncml:netcdf/ncml:attribute[@name='does_not_exist']/@value"""
    }



#read a file

ds = Dataset('test_ncs/result_surface.nc','a')

data_object = NetCDFDogma('NetcdfCF',cf_metadata_beliefs,ds)


data_object.__class__.__name__


data_object.service_provider_institution
data_object.data_conventions
data_object.latitude_units
# will return empty
data_object.does_not_exist


data_object.service_provider_institution = 'David Stuebe'
data_object.data_conventions = 'CF-3.14159'
data_object.latitude_units = 'degrees a little bit west of north'
# will fail - can't make a new attribute element (yet?)
data_object.does_not_exist = 'foobar'

data_object.service_provider_institution
data_object.data_conventions
data_object.latitude_units
data_object.does_not_exist

with open('out.xml','w') as f:
    f.write(etree.tostring(data_object._dataObject))
