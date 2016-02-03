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
@file dictionary_dogma_tests.py
@date 06/05/13
@description test cases for the DictionaryDogma class which is a reference implementation
'''

from __future__ import absolute_import, print_function, division

import unittest

from wicken.dictionary_dogma import DictionaryDogma

from wicken.dictionary_dogma import DictionaryDogmaException
from wicken.exceptions import DogmaMetaClassException
from wicken.exceptions import DogmaGetterSetterException
from wicken.exceptions import DogmaDeleteException

class DictionaryDogmaTest(unittest.TestCase):

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


        d = DictionaryDogma('CF',{},None)
        self.assertEqual(d._religion,'CF')
        self.assertEqual(d._beliefs,{})
        self.assertEqual(d._dataObject,{})
        self.assertEqual(d.__class__.__name__,'CFDictionaryDogma')

        d = DictionaryDogma('CF',{})
        self.assertEqual(d._dataObject,{})

        d = DictionaryDogma('CF',{},{'gi':'joe'})
        self.assertEqual(d._dataObject,{'gi':'joe'})




    def test_help(self):
        pass
        #Can't find a way to test the help?

    def test_dogma_set(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs)

        self.assertEqual(d._dataObject.get('bar'),None)
        d._set('bar','bizzar!')
        self.assertEqual(d._dataObject.get('bar'),'bizzar!')

        d = DictionaryDogma('CF',beliefs)
        self.assertEqual(d._dataObject.get('bar'),None)
        d.foo = 'how bizzar!'
        self.assertEqual(d._dataObject.get('bar'),'how bizzar!')

        with self.assertRaisesRegexp(AttributeError,"""Blasphemy! You can't create the new beliefs"""):
            d.not_an_att = 5

    def test_dogma_get(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,{'bar':'boo'})

        self.assertEqual(d._get('bar'),'boo')
        with self.assertRaises(KeyError):
            d._get('bzzz')

        self.assertEqual(d.foo, 'boo')

        with self.assertRaises(AttributeError):
            d.not_an_att

        with self.assertRaises(DogmaGetterSetterException):
            d.bat

    def test_dogma_del(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,{'bar':'boo'})

        self.assertEqual(d._dataObject.get('bar'),'boo')
        d._del('bar')
        self.assertEqual(d._dataObject.get('bar'),None)

        d._dataObject['bar'] = 'bamboo'
        self.assertEqual(d.foo, 'bamboo')
        del d.foo

        self.assertEqual(d._dataObject.get('bar'), None)

        with self.assertRaises(DogmaGetterSetterException):
            d.foo

        # Call it again!
        with self.assertRaises(DogmaDeleteException):
            del d.foo

        with self.assertRaises(AttributeError):
            del d.not_an_att

    def test_dogma_validate_teaching(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,None)

        ret = d._validate_teaching('foo','bar')
        self.assertIs(ret, 'bar')

        DictionaryDogma._validate_teaching('foo','bar')
        self.assertIs(ret, 'bar')

        with self.assertRaisesRegexp(DictionaryDogmaException,"""The belief """):
            ret = d._validate_teaching('foo',[])


        with self.assertRaisesRegexp(DictionaryDogmaException,"""The belief """):
            beliefs = {'foo':[],'bat':'baz'}
            d = DictionaryDogma('CF',beliefs,None)

