

from wicken.dogma import NetCDFDogma
from netCDF4 import Dataset

rootGrp = Dataset('myfile.nc','w') # open a new file for read/write...


metadata_beliefs = {
    'service_provider_name':'publisher_name',
    'service_provider_contact_info':'publisher_email'}
# typically loaded from a file - a modified version of the IOOS Asset_SOS_MAP


# Make metadata object instance using the NetCDFDogma class to work with a NetCDF data objects metadata using CF conventions
metadata = NetCDFDogma('CF',metadata_beliefs, rootGrp)

print 'Class name: ', metadata.__class__.__name__


print metadata.service_provider_name

metadata.service_provider_name = 'ASA'

print metadata.service_provider_name

# Now use the netcdf method...

print metadata._dataObject.ncattrs()