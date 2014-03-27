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