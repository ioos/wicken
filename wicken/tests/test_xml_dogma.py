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
@file xml_dogma_tests.py
@date 06/05/13
@description test cases for the XmlDogma class

@TODO Ignore the fact that memory is leaked when we create each StringIO instance!
'''

from __future__ import absolute_import, print_function, division

import unittest
from io import BytesIO
from lxml import etree

from wicken.xml_dogma import XmlDogma

from wicken.xml_dogma import XmlDogmaException
from wicken.exceptions import DogmaMetaClassException
from wicken.exceptions import DogmaGetterSetterException
from wicken.exceptions import DogmaDeleteException

BOOKS = b'''<?xml version="1.0" encoding="ISO-8859-1"?>
<bookstore>

<book category="COOKING">
  <title lang="en">Everyday Italian</title>
  <author>Giada De Laurentiis</author>
  <year>2005</year>
  <price>30.00</price>
</book>

<book category="CHILDREN">
  <title lang="en">Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>

<book category="WEB">
  <title lang="en">XQuery Kick Start</title>
  <author>James McGovern</author>
  <author>Per Bothner</author>
  <author>Kurt Cagle</author>
  <author>James Linn</author>
  <author>Vaidyanathan Nagarajan</author>
  <year>2003</year>
  <price>49.99</price>
</book>

<book category="WEB">
  <title lang="en">Learning XML</title>
  <author>Erik T. Ray</author>
  <year>2003</year>
  <price>39.95</price>
</book>

</bookstore>
'''


class XmlDogmaTest(unittest.TestCase):

    def setUp(self):
        """
        Setup test
        """
        pass


    def tearDown(self):
        """
        Tear down test
        """
        pass


    def test_init(self):

        d = XmlDogma('Books',{},None)
        self.assertEqual(d._religion,'Books')
        self.assertEqual(d._beliefs,{})
        self.assertEqual(d._dataObject.tag,'root')
        self.assertEqual(d.__class__.__name__,'BooksXmlDogma')

        d = XmlDogma('Books', {})
        self.assertEqual(d._dataObject.tag, 'root')

        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books', {}, dataObject)
        self.assertEqual(d._dataObject, dataObject)


    def test_help(self):
        pass
        #Can't find a way to test the help?

    def dont_txxt_dogma_set_nonexistent(self):

        beliefs = {'book_title':'/bookstore/book[1]/title',
        'childrens_title':"""/bookstore/book[@category = 'CHILDREN']/title""",
        'foobar':'''/bookstore/foobar'''}

        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books',beliefs,dataObject)

        with self.assertRaisesRegexp(AttributeError,"""Blasphemy! You can't create the new beliefs"""):
            d.not_a_belief = 5

        with self.assertRaisesRegexp(DogmaGetterSetterException,"""Error setting the 'foobar' property of the class 'BooksXmlDogma'"""):
            d.foobar = 5


    def dont_txxt_dogma_set_element_text(self):

        beliefs = {'book_title':'/bookstore/book[1]/title',
        'childrens_title':"""/bookstore/book[@category = 'CHILDREN']/title"""}


        # Set the text using _set
        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books',beliefs,dataObject)
        self.assertEqual(d._get('/bookstore/book[1]/title'),'Everyday Italian')
        d._set('/bookstore/book[1]/title','Z french is better!')
        self.assertEqual(d._get('/bookstore/book[1]/title'),'Z french is better!')

        # Set using the attribute
        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books',beliefs,dataObject)
        self.assertEqual(d._get('/bookstore/book[1]/title'),'Everyday Italian')
        d.book_title = 'Z french is better!'
        self.assertEqual(d._get('/bookstore/book[1]/title'),'Z french is better!')

        self.assertEqual(d._get("""/bookstore/book[@category = 'CHILDREN']/title"""),'Harry Potter')
        d.childrens_title = 'potter harry'
        self.assertEqual(d._get("""/bookstore/book[@category = 'CHILDREN']/title"""),'potter harry')


    def dont_txxt_dogma_set_attribute_text(self):

        beliefs = {'book_category':'/bookstore/book[1]/@category'}

        # Set the text using _set
        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books',beliefs,dataObject)
        self.assertEqual(d._get('/bookstore/book[1]/@category'),'COOKING')
        d._set('/bookstore/book[1]/@category','FOOBAR')
        self.assertEqual(d._get('/bookstore/book[1]/@category'),'FOOBAR')

        # Set using the attribute
        dataObject = etree.parse(BytesIO(BOOKS))
        d = XmlDogma('Books',beliefs,dataObject)
        self.assertEqual(d._get('/bookstore/book[1]/@category'),'COOKING')
        d.book_category = 'CLEANING'
        self.assertEqual(d._get('/bookstore/book[1]/@category'),'CLEANING')




    def test_dogma_get_nonexisting(self):

        beliefs = {'book_title':'/bookstore/book[5]/title',
        'childrens_title':"""/bookstore/book[@category = 'CHILDREN']/title"""}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        with self.assertRaises(XmlDogmaException):
            d._get('bzzz')

        with self.assertRaises(DogmaGetterSetterException):
            d.book_title

        with self.assertRaises(AttributeError):
            d.not_an_att


    def test_dogma_get_element(self):

        beliefs = {'book_title':'/bookstore/book[1]/title',
        'no_title':'/bookstore/book[5]/title',
        'childrens_title':"""/bookstore/book[@category = 'CHILDREN']/title""",
        'childrens_year':"""/bookstore/book[@category = 'CHILDREN']/year"""}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        self.assertEqual(d._get('/bookstore/book[1]/title'),'Everyday Italian')

        self.assertEqual(d.book_title, 'Everyday Italian')

        self.assertEqual(d.childrens_title, 'Harry Potter')

        self.assertEqual(d.childrens_year, '2005')

        with self.assertRaises(DogmaGetterSetterException):
            d.no_title


    def test_dogma_get_existing_attribute(self):

        beliefs = {'book_category':'/bookstore/book[1]/@category'}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        self.assertEqual(d._get('/bookstore/book[1]/@category'),'COOKING')

        self.assertEqual(d.book_category, 'COOKING')



    def dont_txxt_dogma_del_nonexisting(self):
        beliefs = {'book_title':'/bookstore/book[5]/title',
                   'book_foo':'/bookstore/book[1]/@foo'}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        with self.assertRaises(DogmaDeleteException):
            del d.book_title

        with self.assertRaises(DogmaDeleteException):
            del d.book_foo

        with self.assertRaises(AttributeError):
            del d.non_existing



    def dont_txxt_dogma_del_attribute(self):

        beliefs = {'book_category':'/bookstore/book[1]/@category'}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        self.assertEqual(d._get('/bookstore/book[1]/@category'),'COOKING')

        del d.book_category

        with self.assertRaises(XmlDogmaException):
            d._get('/bookstore/book[1]/@category')

        with self.assertRaises(DogmaGetterSetterException):
            self.assertEqual(d.book_category, None)


    def dont_txxt_dogma_del_element(self):

        beliefs = {'book_title':'/bookstore/book[1]/title'}
        dataObject = etree.parse(BytesIO(BOOKS))

        d = XmlDogma('Books',beliefs,dataObject)

        self.assertEqual(d._get('/bookstore/book[1]/title'),'Everyday Italian')

        del d.book_title

        with self.assertRaises(XmlDogmaException):
            d._get('/bookstore/book[1]/title')
        with self.assertRaises(DogmaGetterSetterException):
            d.book_title



    def test_dogma_validate_teaching(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = XmlDogma('Books',beliefs,None)

        ret = d._validate_teaching('foo','bar')
        #self.assertIs(ret, None)

        ret = XmlDogma._validate_teaching('foo','bar')
        #self.assertIs(ret, None)

        #with self.assertRaisesRegexp(XmlDogmaException,"""The belief """):
        #    XmlDogma._validate_teaching('foo','//bar')

        with self.assertRaisesRegexp(XmlDogmaException,"""The belief """):
            ret = d._validate_teaching('foo',[])


        with self.assertRaisesRegexp(XmlDogmaException,"""The belief """):
            beliefs = {'foo':[],'bat':'baz'}
            d = XmlDogma('Books',beliefs,None)

