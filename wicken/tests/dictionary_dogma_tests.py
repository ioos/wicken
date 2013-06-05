from nose.tools import *
import unittest

from wicken.dictionary_dogma import DictionaryDogma

from wicken.dictionary_dogma import DictionaryDogmaException
from wicken.exceptions import DogmaMetaClassException
from wicken.exceptions import DogmaGetterSetterException

class DomgaTest(unittest.TestCase):

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
        assert_equal(d._get('bzzz'),None)
        
        assert_equal(d.foo, 'boo') 
       
        with assert_raises(AttributeError):
            d.not_an_att
       
    def test_dogma_del(self):
    
        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,{'bar':'boo'})
       
        assert_equal(d._dataObject.get('bar'),'boo')
        d._del('bar')
        assert_equal(d._dataObject.get('bar'),None)
    
        d._dataObject['bar'] = 'bamboo'
        assert_equal(d.foo, 'bamboo')
        del d.foo
        assert_equal(d._dataObject.get('bar'),None)
        assert_equal(d.foo, None)
       
       
       
       
            
    def test_dogma_validate_teaching(self):

        beliefs = {'foo':'bar','bat':'baz'}
        d = DictionaryDogma('CF',beliefs,None)
        
        ret = d._validate_teaching('foo','bar')
        assert_is(ret, None)
        
        DictionaryDogma._validate_teaching('foo','bar')
        assert_is(ret, None)
        
        with assert_raises_regexp(DictionaryDogmaException,"""The teaching """):
            ret = d._validate_teaching('foo',[])
        
        
        with assert_raises_regexp(DictionaryDogmaException,"""The teaching """):
            beliefs = {'foo':[],'bat':'baz'}
            d = DictionaryDogma('CF',beliefs,None)
        