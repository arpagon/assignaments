#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#
#       pyloc.py
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

import os
import logging
from optparse import OptionParser
import csv
import collections
from weakref import proxy
from math import sqrt, fsum

LOG_FILENAME = 'loc.log'
COMMENT_START_STRING = "#"

#
# Logging
#

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('LOC')
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

class Item(object):
    '''
    Item of Code, PSP Defined Part
    '''
    def __init__(self, line, start_line):
        '''
        Init
        '''
        self.line=line
        self.position=start_line
        self.name=False
        self.ident_level=False
        self.sub_items={}
        if not self.IdentifyPart():
            del self
        
    def IdentifyPart(self.line):
        '''
        Extract Item o Part Name. from line
        '''
        idents=line.split("    ")
        ident_level=0
        for level in idents:
            if level.startswith("def ") or level.startswith("class "):
                self.name=level.split(" ")[1].split("(")[0]
                self.ident_level=ident_level
            ident_level+=1
        return False


def IdentLevel(line):
    '''
    Identify Ident Level
    '''
    line_space_removed_rigth=line.rstrip()
    idents=line_space_removed_rigth.split("    ")
    return len(idents) - 1

def LOCCount(file):
    '''
    Function for Counting.
        - LOC
        - Blank Spaces
        - ComentedLines
        - Name of Parts
    '''
    total_lines=0
    code_lines=0
    blank_lines=0
    comment_lines=0
    parts = {}
    
    with open(file, 'rb') as code_file:
        for line in code_file:
            in_part=False
            running_part=False
            total_lines+=1
            if line.startswith("#"):
                comment_lines+=1
            elif line.strip():
                blank_lines+=1
            else:
                code_lines+=1
                runining_item=Item(line)
                if runining_item.ident_level=0:
                    '''Is a Part'''
                    parts[runining_item.name]=runining_item
                    running_part=runining_item.name
                    
                    
                    
                            
                    
    


def main():
    '''Unix parsing command-line options'''
    uso = "modo de uso: %prog [options]"
    parser = OptionParser(uso)
    parser.add_option("-F", "--file", dest="file",
                  help="process file [file]", metavar="file")
    (options, args) = parser.parse_args()
    log.info("START COUNTING")
    if options.file:
        result=LOCCount(options.file)
    else:
        parser.error("please define File,  %prog -F example.csv\n Please use -h for help")

if __name__=='__main__':
    main()
