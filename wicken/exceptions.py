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
@file exceptions.py
@date 06/05/13
@description exception classes for the wicken project
'''

class WickenException(Exception):
    """
    Base class for all exceptions in Wicken
    """
    pass
    
class DogmaGetterSetterException(WickenException):
    """
    Exception class for errors during get or set of a dogmatic belief (a property)
    """
    pass  

class DogmaDeleteException(WickenException):
    """
    Exception class for errors while deleting of a dogmatic belief (a property)
    """
    pass  




class DogmaMetaClassException(WickenException):
    """
    Exception class for errors while creating the dogma class for a particular set of beliefs
    """
    pass  
    