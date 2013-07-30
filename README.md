wicken
======
metadata companion library for paegan data model
COPYRIGHT 2013 David Stuebe

description
============

Wicken is built on a Object Relational Mapper. It assumes a mapping exists between a flat namespace which will be used as properties in the object classes for ease of access and the schema for a particular data encoding. For instance the schema might be ISO 19115-2 and the data encoding XML, or the schema might be CF and the encoding NetCDF.

Concrete classes implement the _get and _set methods for a particular encoding, while
the class for a particular mapping is generated at run time from a mapping. Most of the magic happens in a few lines of meta programming...


installation
=============
    $ git clone git@github.com:asascience-open/wicken.git
    $ cd wicken
    $ python setup.py install



demo
===========

Open the [CF Example](https://github.com/asascience-open/wicken/blob/master/example_cf_script.py) or [ISO Example](https://github.com/asascience-open/wicken/blob/master/example_iso_script.py) file. You can copy and paste the file to a python shell to test out the XmlDogma class and see how it works on a real ISO metadata object. I have only implemented three possible mappings to a metadata object, but that should be enough to see how it works. Developing the IOOS namespace for each metadata element and corresponding xpath expressions will be the hard part.

There is no need to make the namespace flat - you can pass in any xml etree element as a data object - it does not have to be the root element. As long as the xpath expressions are relative to the current object ('./gmd:role/...' rather than '/gmi:MI_Metadata/...') all will work just fine.

