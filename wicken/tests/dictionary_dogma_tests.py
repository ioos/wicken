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

from nose.tools import *
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
        assert_equal(d._religion,'CF')
        assert_equal(d._beliefs,{})
        assert_equal(d._dataObject,{})
        assert_equal(d.__class__.__name__,'CFDictionaryDogma')
        
        d = DictionaryDogma('CF',{})
        assert_equal(d._dataObject,{})
        
        d = DictionaryDogma('CF',{},{'gi':'joe'})
        assert_equal(d._dataObject,{'gi':'joe'})
        
        

            
    def test_help(self):    
        pass
        #Can't find a way to test the help?
        
    def test_dogma_set(self):
    
        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs)
        
        assert_equal(d._dataObject.get('bar'),None)
        d._set('bar','bizzar!')
        assert_equal(d._dataObject.get('bar'),'bizzar!')

        d = DictionaryDogma('CF',beliefs)
        assert_equal(d._dataObject.get('bar'),None)
        d.foo = 'how bizzar!'
        assert_equal(d._dataObject.get('bar'),'how bizzar!')

        with assert_raises_regexp(AttributeError,"""Blasphemy! You can't create the new beliefs"""):
            d.not_an_att = 5
            
    def test_dogma_get(self):
    
        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,{'bar':'boo'})
       
        assert_equal(d._get('bar'),'boo')
        with assert_raises(KeyError):
            d._get('bzzz')
        
        assert_equal(d.foo, 'boo') 
       
        with assert_raises(AttributeError):
            d.not_an_att
            
        with assert_raises(DogmaGetterSetterException):
            d.bat
       
    def test_dogma_del(self):
    
        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,{'bar':'boo'})
       
        assert_equal(d._dataObject.get('bar'),'boo')
        d._del('bar')
        assert_equal(d._dataObject.get('bar'),None)
    
        d._dataObject['bar'] = 'bamboo'
        assert_equal(d.foo, 'bamboo')
        del d.foo
        
        assert_equal(d._dataObject.get('bar'), None)
        
        with assert_raises(DogmaGetterSetterException):
            d.foo
        
        # Call it again!
        with assert_raises(DogmaDeleteException):
            del d.foo
        
        with assert_raises(AttributeError):
            del d.not_an_att
            
    def test_dogma_validate_teaching(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,None)
        
        ret = d._validate_teaching('foo','bar')
        assert_is(ret, 'bar')
        
        DictionaryDogma._validate_teaching('foo','bar')
        assert_is(ret, 'bar')
        
        with assert_raises_regexp(DictionaryDogmaException,"""The belief """):
            ret = d._validate_teaching('foo',[])
        
        
        with assert_raises_regexp(DictionaryDogmaException,"""The belief """):
            beliefs = {'foo':[],'bat':'baz'}
            d = DictionaryDogma('CF',beliefs,None)
        
