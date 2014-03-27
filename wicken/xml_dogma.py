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
@file xml_dogma.py
@date 06/03/13
@description Implementation of the Dogma Metadata class for xml IO using etree
'''
import re
from lxml import etree
import dogma
from exceptions import WickenException

class XmlDogmaException(WickenException):
    """
    An exception class for catching problems in the XML Dogma class
    """
    pass

class XmlDogma(dogma.Dogma):
    
    def __init__(self, religion, beliefs, dataObject=None, namespaces=None):
        """
        Religion is a name or identifier for this metadata mapping which will become the 
        prefix for the class name
        Beliefs is a dictionary which maps a flat namespace to an xpath query
        DataObject is an etree element on which the xpath queries are applied
        Namespace is an optional set of namespaces which may be used in the xpath expressions.
        """            
        
        if dataObject is None:
            dataObject = etree.Element('root') # does this make sense? Should this argument be required?
        
        if not isinstance(dataObject, (etree._Element, etree._ElementTree)):
            raise TypeError('XmlDogma only allows XML Element dataObjects!')
            
        self._namespaces = namespaces
        super(XmlDogma, self).__init__(religion, beliefs, dataObject)   

    def _get(self, teaching, options=None): 
        result = self._eval(teaching)
        
        if isinstance(result, list):
            result_length = len(result)
            if result_length == 1:
                result = result[0]
            elif result_length == 0:
                raise XmlDogmaException('Teaching "%s" returns zero elements!' % teaching)
            else:
                raise XmlDogmaException('Teaching "%s" returns more than one element!' % teaching)

        if isinstance(result, etree._Element):
            #print type(result.text)
            result = result.text
        elif isinstance(result, etree._ElementStringResult) or isinstance(result, etree._XSLTResultTree):
            #print type(result)
            result = str(result)

        return result


    def _set(self,xpath,value, options=None):
        raise NotImplementedError()

        result = self._eval_xpath(xpath)
        
        if isinstance(result, list):
            result_length = len(result)
            if result_length == 1:
                result = result[0]
            elif result_length == 0:
                raise XmlDogmaException('The specified xpath "%s" does not exist. Create it before trying to set the value!' % xpath)
            else:
                raise XmlDogmaException('Invalid xpath expression "%s" returns more than one element!' % xpath)
              
        if isinstance(result, etree._Element):
            result.text = value
        elif isinstance(result, etree._ElementStringResult):
            parent = result.getparent()
            name = result.attrname
            parent.attrib[name] = value   
        
    def _del(self, xpath, options=None):
    
        raise NotImplementedError()

        result = self._eval_xpath(xpath)
        if isinstance(result, list):
            result_length = len(result)
            if result_length == 1:
                result = result[0]
            elif result_length == 0:
                raise XmlDogmaException('Can not delete a value that is not set!')
            else:
                raise XmlDogmaException('Invalid xpath expression "%s" returns more than one element!' % xpath)
        
        if isinstance(result, etree._Element):
            parent = result.getparent()
            parent.remove(result)
            
        elif isinstance(result, etree._ElementStringResult):
            parent = result.getparent()
            name = result.attrname
            del parent.attrib[name]
        
    def _create_path(self,xpath):
        """
        Started to write an xpath parser to create the specified path but there are many
        ways to specify a path in xpath - it is too expressive. This is not a sensible 
        thing to do from inside a property function. Let it return an error unless the 
        path exists and add helper functions to create the specific metadata block that is 
        required.
        """
        raise NotImplementedError()

        split_path = xpath.split('/')
        test_paths = ['/'.join(sp[:i+1]) for i in xrange(1,len(split_path))]
        
        for path in reversed(test_paths):
            result = self._eval_xpath(path)
            result_length = len(result)
            if  result_length == 0:
                # Still no elements found
                continue
            elif result_length == 1:
                result = result[0]
                break
            else:
                raise XmlDogmaException('Invalid xpath expression "%s" returns more than one element!' % xpath)
            
        else:
            raise XmlDogmaException('Root element "%s" of xpath expression "%s" not found while trying to create path.' % (path, xpath))
            
        existing_elemet = result
        existing_path = path
        existing_index = test_paths.index(existing_path)
        
        for new_element in split_path[existing_index+1:]:
            
            #Regex it!
            # 'employee[secretary][assistant]' => ['employee', 'secretary', 'assistant', '']
            # 'toy[attribute::color = "red"]' => ['toy', 'attribute::color = "red"', '']
            parts = re.split('\[(.*?)\]',new_element)
            #@TODO - find a better regex that does not include one empty string for each bracket
            try:
                while True:
                    parts.remove('')
            except ValueError:
                pass
                
            tag = parts[0]
            predicates = parts[1:]
            
            e = etree.Element(tag)
            
            
            ### Did not finish implementing... see comment above about why its a bad idea
            for predicate in predicates:
                if predicate.isdigit():
                    # it is specifying where to insert this child
                    pass
                elif predicate.startswith('@'):
                    #parse the attribute and set it...
                    pass
                else:
                    pass

            
            
        
        
        
    def _eval_xpath(self, xpath):
        """
        Evaluates xpath expressions.

        Either string or XPath object.
        """
        if isinstance(xpath, etree.XPath):
            result = xpath(self._dataObject)
        else:
            result = self._dataObject.xpath(xpath,namespaces=self._namespaces)
        
        #print 'Xpath expression:', xpath
        #print etree.tostring(self._dataObject)
        #print 'Got Result: \n%s\n   End Result' % result
        
        return result
        
        
    def _eval_xslt(self, xslt_doc):
        transform = etree.XSLT(xslt_doc)
        return str(transform(self._dataObject))

    def _eval(self, teaching):
        """
        Returns the evaluation.
        """
        # transform if someone called _get directly
        if isinstance(teaching, basestring):
            teaching = self._validate_teaching(None, teaching, namespaces=self._namespaces)

        return teaching(self._dataObject)

    @classmethod
    def _validate_teaching(cls, belief, teaching, *args, **kwargs):
        """
        Check to make sure the teaching object which will be used as a dictionary key is hashable
        """
        # attempt to transform
        namespaces = kwargs.get('namespaces', None)
        if not namespaces:
            for a in args:
                if isinstance(a, dict): # @TODO check types
                    namespaces = a
                    break

        try:
            return etree.XPath(teaching, namespaces=namespaces or {})
        except:
            pass

        try:
            xml_doc = etree.XML(teaching)
            return etree.XSLT(xml_doc)
        except:
            pass

        raise XmlDogmaException('The belief "%s" does not have a valid teaching. The Teaching must be an xpath string or xslt document. Received teaching: "%s" (type: %s)' % (belief, teaching, type(teaching)))

class MultipleXmlDogma(XmlDogma):
    """
    A mostly read-only Dogma that allows the returning of multiple values from a belief.

    Your beliefs that require multiple return values should have a key that ends with the
    '*' character.
    """
    def __init__(self, religion, beliefs, dataObject=None, namespaces=None):
        XmlDogma.__init__(self, religion, beliefs, dataObject=dataObject, namespaces=namespaces)

    def _get(self, xpath, options=None):
        if options and 'multiple' in options:
            result = self._eval_xpath(xpath)

            def get_text(el):
                if isinstance(el, etree._Element):
                    return el.text
                elif isinstance(el, etree._ElementStringResult):
                    return str(el)

            if not isinstance(result, list):
                result = [result]

            return map(get_text, result)

        return super(MultipleXmlDogma, self)._get(xpath, options=options)

    def _set(self, xpath, options=None):
        if options and 'multiple' in options:
            raise NotImplementedError("Cannot set a belief with the multiple option")

        return super(MultipleXmlDogma, self)._set(xpath, options=options)

    def _del(self, xpath, options=None):
        if options and 'multiple' in opitons:
            raise NotImplementedError("Cannot delete a belief with the multiple option")

        return super(MultipleXmlDogma, self)._set(xpath, options=options)

