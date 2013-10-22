#!/usr/bin/env python
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
import string

LOG_FILENAME = 'loc.log'
COMMENT_START_STRING = "#"
PY_EXTENSION = ("py","python")

logging.basicConfig(level=logging.WARNING)
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
        Item Constructor
        
        Parameters
        ----------
        line: str,
            line to analyze.
        start_line: int, 
            Start position
        
        '''
        self.line=line
        self.start_line=start_line
        self.end_line=False
        self.name=False
        self.ident_level=False
        self.length=0
        self.sub_items={}
        self.is_a_part=self.IdentifyPart()
        
    def IdentifyPart(self):
        '''
        Extract Item o Part Name. from line, Ident Level and If is a item
        
        Returns
        -------
            is_a_part: Bool, 
                Is a Item, Part, Function or Classs
        '''
        idents=self.line.rstrip().split("    ")
        self.ident_level=len(idents) - 1
        for level in idents:
            if level.startswith("def ") or level.startswith("class "):
                self.name=level.split(" ")[1].split("(")[0]
                return True
        return False

def LocateFiles(root, extensions=PY_EXTENSION):
    '''
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    
    Parameters
    ----------
    root : str, path of programs 
        search file for counting lines..
    extensions : list, List of extensions
        Extension to search programs
    '''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    if os.stat(os.path.join(path, filename)):
                        yield os.path.join(path, filename)

def LOCCountDir(root, extensions=PY_EXTENSION):
    '''
    Locate all files matching supplied filename pattern in and below
    supplied root directory.
    
    Parameters
    ----------
    root : str, path of programs 
        search file for counting lines..
    extensions : list, List of extensions
        Extension to search programs
    '''
    locate = LocateFiles(root, extensions)
    great_total = 0
    while True:
        try:
            file_to_count = locate.next()
            log.info("Counting File: %s" % file_to_count)
            (code_lines, parts, total_lines, blank_lines, comment_lines)=LOCCountFile(file_to_count)
            #print "===================================================================="
            print string.expandtabs("\t%s" % file_to_count.split("/")[-1],16)
            FormatOutput(code_lines, parts, total_lines, blank_lines, comment_lines)
            great_total+=code_lines
        except StopIteration:
            log.info("Fin De Archivado")
            break
    print "===================================================================="
    print string.expandtabs("TOTAL\t\t\t%s" % great_total,16)
    print "===================================================================="
            

    
    

def LOCCountFile(file):
    '''
    Count LOC in File. Follow Python Code Standar.
    
    Parameters
    ----------
    file : str, path of file 
        file for counting lines..

    Returns
    -------
    code_lines: int, 
        phisical code lines
    parts: dic
        Dictoinary of parts
    total_lines: int,
        Total fo lines.
    blank_lines: int,
        Blank Lines
    comment_lines: int,
        Comment lines.
    '''
    total_lines=0
    code_lines=0
    blank_lines=0
    comment_lines=0
    parts = {}
    in_part=False
    running_part=False
            
    with open(file, 'rb') as code_file:
        for line in code_file:
            log.debug("RUNINGPART:%s  INPART:%s" % (running_part, in_part))
            total_lines+=1
            if line.strip().startswith("#"):
                comment_lines+=1
                log.debug("COMENT LINE %s %s" % (comment_lines, line))
            elif not line.strip():
                blank_lines+=1
                log.debug("BLANK LINE %s %s" % (blank_lines, line))
            else:
                code_lines+=1
                log.debug("CODE LINE %s %s" % (code_lines, line))
                running_item=Item(line, total_lines)
                if running_item.is_a_part:
                    if running_item.ident_level==0:
                        '''Is a Part'''
                        parts[running_item.name]=running_item
                        running_part=running_item.name
                        parts[running_part].length+=1
                        in_part=True
                        logpart=logging.getLogger('LOC.%s' % running_part)
                        log.debug("ADDED PART %s %s" % (running_item.name, 
                                                                        line))
                    elif running_item.ident_level==1:
                        parts[running_part].sub_items[running_item.name]=running_item
                        parts[running_part].length+=1
                        logpart.debug("IN PART %s  ADD ITEM %s: %s" % (running_part, 
                                                    running_item.name, line))
                    else:
                        parts[running_part].length+=1
                        logpart.debug("PART LENGTH %s: %s %s" % (running_part, 
                                            parts[running_part].length, line))
                else:
                    if in_part:
                        logpart.debug("IDENT: %s" % running_item.ident_level)
                        if running_item.ident_level>0:
                            parts[running_part].length+=1
                            logpart.debug("PART LENGTH %s: %s" % (running_part, 
                                            parts[running_part].length))
                        else:
                            parts[running_part].end_line=total_lines
                            in_part=False
                            del running_item
    log.debug("===TOTAL===\n CODE LINES:%s\n PARTS:%s \n TOTAL LINES:%s \n "
              "BLANK LINE:%s \n COMMEN_LINES:%s" % 
              (code_lines, parts, total_lines, blank_lines, comment_lines))
    return (code_lines, parts, total_lines, blank_lines, comment_lines)

def FormatOutput(code_lines, parts, total_lines=0, blank_lines=0, comment_lines=0):
    '''
    OutPut whit the optimal Format.
    
    Parameters
    -------
    code_lines: int, 
        phisical code lines
    parts: dic
        Dictoinary of parts
    total_lines: int,
        Total fo lines.
    blank_lines: int,
        Blank Lines
    comment_lines: int,
        Comment lines.
    
    '''
    print "===================================================================="
    print string.expandtabs("Part Name\tN of Items\tPart Size\tTotal",16)
    print "===================================================================="
    for part in parts:
        if len(parts[part].sub_items.keys())==0:
            parts[part].sub_items[None]=None
        print string.expandtabs("%s\t%s\t%s" % (parts[part].name, 
                    len(parts[part].sub_items.keys()), parts[part].length),16)
    print string.expandtabs("\t\t\t%s" % code_lines,16)


def main():
    '''Unix parsing command-line options'''
    uso = "modo de uso: %prog [options]"
    parser = OptionParser(uso)
    parser.add_option("-F", "--file", dest="file",
                  help="process file [file]", metavar="file")
    parser.add_option("-D", "--dir", dest="dir",
                  help="process dir [DIR]", metavar="Directory")
    (options, args) = parser.parse_args()
    log.info("START COUNTING")              #Start Program
    if options.dir:
        LOCCountDir(options.dir)
    elif options.file:
        (code_lines, parts, total_lines, blank_lines, comment_lines)=LOCCountFile(options.file)
        FormatOutput(code_lines, parts, total_lines, blank_lines, comment_lines)
    else:
        parser.error("please define File,  %prog -F example.py\n Please use -h for help")

if __name__=='__main__':
    main()
