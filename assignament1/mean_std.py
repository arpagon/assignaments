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


__version__ = "0.0.2"
__license__ = """The GNU General Public License (GPL-2.0)"""
__author__ = "Sebastian Rojo <http://www.sapian.com.co> arpagon@gamil.com"
__contributors__ = []
_debug = 0

import os
import logging
from optparse import OptionParser
import csv
import collections
from weakref import proxy
from math import sqrt, fsum

logging.basicConfig(level=logging.DEBUG)
LOG_FILENAME = 'assignament1.log'
log = logging.getLogger('MEAN_STD')
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

def Mean(dataset):
    '''
    Calculate Mean from dataset
    '''
    Summatory=fsum(dataset)
    Length=len(dataset)
    Mean=Summatory/Length
    log.info("The Mean of dataset is %s" % Mean)
    return Mean

def Std(dataset):
    '''
    Calculate Standar deviation from dataset
    '''
    Summatory=fsum(dataset)
    LengthMinusOne=len(dataset)-1
    CurrentMean=Mean(dataset)
    Std=sqrt(sum([(data - CurrentMean)**2 for data in dataset]) / LengthMinusOne)
    log.info("The Std of dataset is %s" % Std)
    return Std

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
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        '''
        Method for de Equal comparation.
        '''
        if isinstance(other, LinkedList):
            return len(self) == len(other) and list(self) == list(other)
        return not self.isdisjoint(other)


def read_file(file):
    '''
    Read CSV File, Important Only Read column 1
    
    :param file: path for file to read 
    :returns dataset: LinkedLink dataset
    '''
    with open(file, 'rb') as csvfile:
        #dialect = csv.Sniffer().sniff(csvfile.read(1024))
        #csvfile.seek(0)
        reader = csv.reader(csvfile)
        dataset=LinkedList()
        for row in reader:
                if len(row) >= 1:
                    try:
                        dataset.add(float(row[0]))
                    except ValueError:
                        log.warning("%s Is not a float" % row[0])
                else:
                    log.warning("Empty Row")
        return dataset


def main():
    '''Unix parsing command-line options'''
    uso = "modo de uso: %prog [options] "
    parser = OptionParser(uso)
    parser.add_option("-F", "--file", dest="file",
                  help="process file [file]", metavar="file")
    parser.add_option("-s", "--standar-deviation", dest="std",
                  help="Calculate Standar deviation from dataset [file].csv", 
                  action="store_true", metavar="file")
    parser.add_option("-m", "--mean", dest="mean",
                  help="Calculate Mean from dataset [file]", 
                  action="store_true", 
		  metavar="file")
    (options, args) = parser.parse_args()
    log.info("START APP")
    if options.file:
        if options.std or options.mean:
            dataset=read_file(options.file)
            if options.std:
                Std(dataset)
            if options.mean:
                Mean(dataset)
        else:
             parser.error("please set calculation,\n Please use -h for help")
    else:
        parser.error("please define dataset,  %prog -F example.csv\n Please use -h for help")

if __name__=='__main__':
    main()
