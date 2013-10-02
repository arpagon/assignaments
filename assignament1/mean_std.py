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
from math import sqrt, fsum
from LinkedList import LinkedList

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
