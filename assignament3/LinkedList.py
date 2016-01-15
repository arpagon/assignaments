#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#
#       mean_std.py
#       Copyright 2010 arpagon <arpagon@gmail.com.co>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


__version__ = "0.0.1"
__license__ = """The GNU General Public License (GPL-2.0)"""
__author__ = "Sebastian Rojo <http://www.sapian.com.co> arpagon@gamil.com"
__contributors__ = []
_debug = 0

import collections
from weakref import proxy

class Link(object):
    '''
    The proper use of __slots__ is to save space in objects.
    '''
    __slots__ = 'prev', 'next', 'key', '__weakref__'

class LinkedList(collections.MutableSet):
    '''
    LinkedLink
    Set the remembers the order elements were added
    '''

    def __init__(self, iterable=None):
        '''
        Init
        '''
        self.__root = root = Link()         
        root.prev = root.next = root
        self.__map = {}                     # key --> link
        if iterable is not None:
            self |= iterable

    def __len__(self):
        '''
        Length for the LinkedList
        '''
        return len(self.__map)

    def __contains__(self, key):
        '''
        Return Content of LinkedList
        '''
        return key in self.__map

    def add(self, key):
        '''
        Add Node
        Store new key in a new link at the end of the linked list
        '''
        if key not in self.__map:
            '''
            Not Element Eq in the list
            '''
            self.__map[key] = link = Link()            
            root = self.__root
            last = root.prev
            link.prev, link.next, link.key = last, root, key
            last.next = root.prev = proxy(link)
    
    def head(self):
        '''
        Return Head
        '''
        return list(self)[0],list(self)[-1] 
        

    def discard(self, key):
        '''
        Remove an existing item using self.__map to find the link which is
        then removed by updating the links in the predecessor and successors.
        '''
        if key in self.__map:
            link = self.__map.pop(key)
            link.prev.next = link.next
            link.next.prev = link.prev

    def __iter__(self):
        '''
        iteration for the Next Method
        '''
        root = self.__root
        curr = root.next
        while curr is not root:
            yield curr.key
            curr = curr.next

    def __reversed__(self):
        '''
        iteration in reverse mode Method
        '''
        root = self.__root
        curr = root.prev
        while curr is not root:
            yield curr.key
            curr = curr.prev

    def pop(self, last=True):
        '''
        pop key
        '''
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        '''
        String Conversion representation of object LinkeList repr()
        '''
        if not self:
            return '{0!s}()'.format(self.__class__.__name__)
        return '{0!s}({1!r})'.format(self.__class__.__name__, list(self))

    def __eq__(self, other):
        '''
        Method for de Equal comparation.
        '''
        if isinstance(other, LinkedList):
            return len(self) == len(other) and list(self) == list(other)
        return not self.isdisjoint(other)
