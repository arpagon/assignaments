#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#
#       proxy_estimated_table.py
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
from math import sqrt, fsum, exp
from math import log as NaturalLogartim
from mean_std import Std, Mean
from LinkedList import LinkedList
import string

LOG_FILENAME = 'proxysize.log'
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('FIT')
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


#class parts
class Parts(object):
    '''
    Parameters
    ----------
    name: str, name
        name of the part
    loc: int, Lines of code.
        Lines of code of part
    n_of_items: int, Number of itemes.
        Number of items for this part.
    '''
    
    #init
    def __init__(self, name, loc, n_of_items):
        '''
        Init
        '''
        self.name = name
        self.loc = loc
        self.n_of_items = n_of_items
        self.CalcLocMethod()
        self.CalcNormSize()
        
    #CalcLocMethod
    def CalcLocMethod(self):
        '''
        divide number of parts for number of itemes.

        Parameters
        ----------
        Self: Parts
            Part

        Returns
        -------
        loc_methods: float, loc/methods value
        '''
        try:
            self.loc_methods = self.loc / self.n_of_items
        except ZeroDivisionError:
            log.warning("Number of for part %s items is Zero" % (self.name) )
            self.loc_methods = 0
        return self.loc_methods

    def CalcNormSize(self):
        '''
        Natural Log  fot de Loc/methods

        Parameters
        ----------
        Self: Parts
            Part

        Returns
        -------
        norm_size: float, loc/metho normalized.
        '''
        self.norm_size = NaturalLogartim(self.loc_methods)
        return self.norm_size

def CalcTableSizeNormalized(parts):
    '''
    Calculate Ln normalized est from dataset
    
    Parameters
    ----------
    parts : list of parts, 
        List of parts

    Returns
    -------
    ln_vs: float, 
        Normalized Proxy sixe for Very Small size.
    ln_s: float,
        Normalized Proxy sixe for Small size.
    ln_m: float,
        Normalized Proxy sixe for Medium size.
    ln_l: float,
        Normalized Proxy sixe for large size.
    ln_vl: float,
        Normalized Proxy sixe for large size.
    '''
    #for part in parts:
    dataset = []
    for part in parts:
        dataset.append(part.norm_size)
    std_ln_size = Std(dataset)
    mean_ln_size = Mean(dataset)
    ln_vs = mean_ln_size - 2 * std_ln_size
    ln_s = mean_ln_size - std_ln_size
    ln_m = mean_ln_size
    ln_l = mean_ln_size + std_ln_size
    ln_vl = mean_ln_size + 2 * std_ln_size
    return (ln_vs, ln_s, ln_m, ln_l, ln_vl)

#CalcTableSize
def CalcTableSize(ln_vs, ln_s, ln_m, ln_l, ln_vl):
    '''
    Calculate Table Size, des-normalized the table size.
    Parameters
    -------
    ln_vs: float, 
        Normalized Proxy sixe for Very Small size.
    ln_s: float,
        Normalized Proxy sixe for Small size.
    ln_m: float,
        Normalized Proxy sixe for Medium size.
    ln_l: float,
        Normalized Proxy sixe for large size.
    ln_vl: float,
        Normalized Proxy sixe for large size.
    
    Returns
    -------
    vs: float, 
        Proxy sixe for Very Small size.
    s: float,
        Proxy sixe for Small size.
    m: float,
        Proxy sixe for Medium size.
    l: float,
        Proxy sixe for large size.
    vl: float,
        Proxy sixe for large size.        
    '''
    #vs, s, m, l, vl = exp(ln_vs, ln_s, ln_m, ln_l, ln_vl )
    vs = exp(ln_vs)
    s = exp(ln_s)
    m = exp(ln_m)
    l = exp(ln_l)
    vl = exp(ln_vl)
    return (vs, s, m, l, vl)

#Read File
def read_file(file):
    '''
    Read CSV File, Important Only Read column 1 and column 2
    
    Parameters
    ----------
    file : str, path of file 
        path for file to read and fill dataset
    
    Returns
    -------
    parts: list of parts
    '''
    #Open File
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        parts = []
        #for row in file:
        for row in reader:
                #if length of row >= 3
                if len(row) >= 3:
                    #parts
                    try:
                        parts.append(Parts(name=row[0],
                            loc=float(row[1]), n_of_items=float(row[2])))
                    except ValueError:
                        log.warning("%s Problem whit row" % row)
                else:
                    #mesnsaje: row whit insuficient data.
                    log.warning("row whit insuficient data or Empty Row")
        return parts

#FormatOutput
def FormatOutput(vs, s, m, l, vl):
    '''
    OutPut whit the optimal Format.
    
    Parameters
    ----------
    vs: float, 
        Proxy sixe for Very Small size.
    s: float,
        Proxy sixe for Small size.
    m: float,
        Proxy sixe for Medium size.
    l: float,
        Proxy sixe for large size.
    vl: float,
        Proxy sixe for large size.  
    '''
    #Print Header
    print "===================================================================="
    print string.expandtabs("VS\tS\tM\tL\tVL", 16)
    print "===================================================================="
    #Print Values
    print string.expandtabs("%s\t%s\t%s\t%s\t%s" % (vs, s, m, l, vl), 16)
    print "===================================================================="

#main
def main():
    '''Unix parsing command-line options'''
    #give options.
    uso = "modo de uso: %prog [options] "
    parser = OptionParser(uso)
    parser.add_option("-F", "--file", dest="file",
                    help="File Whit Dataset file.csv [file]", metavar="file")
    (options, args) = parser.parse_args()
    log.info("START APP")
    if options.file:
        parts = read_file(options.file)
        if len(parts) >= 2:
            (ln_vs, ln_s, ln_m, ln_l, ln_vl) = CalcTableSizeNormalized(parts)
            (vs, s, m, l, vl) = CalcTableSize(ln_vs, ln_s, ln_m, ln_l, ln_vl)
            FormatOutput(vs, s, m, l, vl)
        else:
             parser.error("File must contaian 2 or more pairs of data")
    else:
        parser.error("please define dataset, %prog -F example.csv\n" 
                                                       "Please use -h for help")

if __name__=='__main__':
    main()