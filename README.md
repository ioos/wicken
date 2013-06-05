wicken
======
metadata companion library for paegan data model


description
============

Wicken is built on a Object Relational Mapper. It assumes a mapping exists between a flat namespace which will be used as properties in the object classes for ease of access and the schema for a particular data encoding. For instance the schema might be ISO 19115-2 and the data encoding XML, or the schema might be CF and the encoding NetCDF.

Concrete classes implement the _get and _set methods for a particular encoding, while
the class for a particular mapping is generated at run time from a mapping. Most of the magic happens in a few lines of meta programming...


