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
@file data_tests.py
@date 06/05/13
@description exception classes for the wicken project
'''

from __future__ import absolute_import, print_function, division

import unittest

from wicken.dogma import Dogma
from wicken.dogma import MetaReligion
from wicken.dogma import Tenets

from wicken.exceptions import DogmaMetaClassException
from wicken.exceptions import DogmaGetterSetterException
from wicken.exceptions import DogmaDeleteException

class DogmaTest(unittest.TestCase):

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


        d = Dogma('CF',{},None)
        self.assertEqual(d._religion,'CF')
        self.assertEqual(d._beliefs,{})
        self.assertIs(d._dataObject,None)
        self.assertEqual(d.__class__.__name__,'CFDogma')

        d = Dogma('CF',{},'foo')
        self.assertIs(d._dataObject,'foo')

        beliefs = {'foo':'bar','bat':'baz'}
        d = Dogma('CF',beliefs,None)
        self.assertIs(d._beliefs,beliefs)
        self.assertIs(d.__class__._beliefs, beliefs)
        self.assertIs(d.__class__._religion, 'CF')
        self.assertIsInstance(d.__class__.__dict__.get('foo'), Tenets)
        self.assertIsInstance(d.__class__.__dict__.get('bat'), Tenets)

        bat_tenet = d.__class__.__dict__.get('bat')
        self.assertEqual(bat_tenet.belief, 'bat')
        self.assertEqual(bat_tenet.teaching,'baz')


        with self.assertRaisesRegexp(DogmaMetaClassException,"Blasphemy! The name of your metadata religion"):
            d = Dogma('',{},None)

    def test_help(self):
        pass
        #Can't find a way to test the help?

    def test_dogma_set(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = Dogma('CF',beliefs,None)
        with self.assertRaisesRegexp(NotImplementedError,'_set Method is not implemented in the Dogma Base Class!'):
            d._set('foo','bar')

        with self.assertRaisesRegexp(DogmaGetterSetterException,"""Error setting the 'foo' property of the class 'CFDogma'"""):
            d.foo = 5

        with self.assertRaises(AttributeError):
            d.not_an_att = 5


    def test_dogma_delete(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = Dogma('CF',beliefs,None)
        with self.assertRaisesRegexp(NotImplementedError,'_del Method is not implemented in the Dogma Base Class!'):
            d._del('foo')

        with self.assertRaisesRegexp(DogmaDeleteException,"""Error deleting the 'foo' property of the class 'CFDogma'"""):
            del d.foo

        with self.assertRaises(AttributeError):
            del d.not_an_att


    def test_dogma_get(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = Dogma('CF',beliefs,None)
        with self.assertRaisesRegexp(NotImplementedError,'_get Method is not implemented in the Dogma Base Class!'):
            d._get('foo')

        with self.assertRaisesRegexp(DogmaGetterSetterException,"""Error getting the 'foo' property of the class 'CFDogma'"""):
            d.foo

        with self.assertRaises(AttributeError):
            d.not_an_att


    def test_dogma_validate_teaching(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = Dogma('CF',beliefs,None)

        ret = d._validate_teaching('foo','bar')
        self.assertIs(ret, 'bar')

        Dogma._validate_teaching('foo','bar')
        self.assertIs(ret, 'bar')



