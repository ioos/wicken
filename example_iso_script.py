

from lxml import etree
from wicken.xml_dogma import XmlDogma



iso_metadata_beliefs = {
    # A map of what you call the metadata property to an xpath expression for it in some convention/encoding
    # typically loaded from a file - a modified version of the IOOS Asset_SOS_MAP spread sheet for example
    'service_provider_name':"""/gmi:MI_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode[@codeListValue='pointOfContact']/../../gmd:individualName/gco:CharacterString""",
    'service_provider_contact_info':"""/gmi:MI_Metadata/gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode[@codeListValue='pointOfContact']/../../gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString""",
    'west_bounding_longitude':"""/gmi:MI_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal"""
    }

# need to explicitely declare the name spaces
namespaces = {
"gmx":"http://www.isotc211.org/2005/gmx",
"gsr":"http://www.isotc211.org/2005/gsr",
"gss":"http://www.isotc211.org/2005/gss",
"gts":"http://www.isotc211.org/2005/gts",
"xs":"http://www.w3.org/2001/XMLSchema",
"gml":"http://www.opengis.net/gml/3.2",
"xlink":"http://www.w3.org/1999/xlink",
"xsi":"http://www.w3.org/2001/XMLSchema-instance",
"gco":"http://www.isotc211.org/2005/gco",
"gmd":"http://www.isotc211.org/2005/gmd",
"gmi":"http://www.isotc211.org/2005/gmi",
"srv":"http://www.isotc211.org/2005/srv",
}


#read a file

xml_etree = etree.parse('test_isos/slrfvm.xml')
#xml_etree = etree.parse('test_isos/45001.xml')

data_object = XmlDogma('Iso19115',iso_metadata_beliefs,xml_etree, namespaces=namespaces)


data_object.__class__.__name__


data_object.service_provider_name
data_object.service_provider_contact_info
data_object.west_bounding_longitude


data_object.service_provider_name = 'David Stuebe'
data_object.service_provider_contact_info = 'dstuebe@asascience.com'
data_object.west_bounding_longitude = '5.005'

data_object.service_provider_name
data_object.service_provider_contact_info
data_object.west_bounding_longitude

with open('out.xml','w') as f:

    f.write(etree.tostring(xml_etree))


    