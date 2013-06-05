#!/usr/bin/env python
'''
@author David Stuebe <dstuebe@asasscience.com>
@file util.py
@date 06/03/13
@description Utility module for functions and helpers
'''



from pprint import pprint
import StringIO



def pretty_print(obj):

    contents = "Pretty Print Failed :-("
    try:
        output = StringIO.StringIO()
        pprint(obj, output)
        contents = output.getvalue()
    finally:
        output.close()
    return contents