#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#
#       fit.py
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
from math import sqrt, fsum
from LinkedList import LinkedList
import string

LOG_FILENAME = 'fit.log'

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('FIT')
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

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
    dataset: LinkedLink dataset
    '''
    #Open File
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        dataset=LinkedList()
        #for row in file:
        for row in reader:
                #if length of row >= 2:
                if len(row) >= 2:
                    #add to LinkedList Float Row[0] and Row[1]
                    try:
                        dataset.add(( float(row[0]) , float(row[1]) ))
                    except ValueError:
                        log.warning("{0!s} Problem whit row".format(row[0]))
                else:
                    #mesnsaje: row whit insuficient data.
                    log.warning("row whit insuficient data or Empty Row")
        return dataset

#Calc Sumarizes
def CalcSumatories(dataset):
    '''
    Calculate Sumatories for linear Regretaion from dataset
    
    Parameters
    ----------
    dataset : LinkedList, 
        Dataset to calc Sumatories..

    Returns
    -------
    sum_x: float, 
        Sumatories of data x in dataset
    sum_y: float,
        Sumatories of data x in dataset
    sum_square_x: float,
        Sumatories of squeres of data x in dataset
    sum_square_y: float,
        Sumatories of squeres of data xy in dataset
    sum_xy: float,
        Sumatories of product of data x  and data y in dataset
    mean_x:
        Mean of x data in dataset
    mean_y:
        Mean of y data in dataset
    length_list: int,
        N or Length of pair of data in dataset.
    '''
    sum_x = float(0)
    sum_y = float(0)
    sum_square_x = float(0)
    sum_square_y = float(0)
    sum_xy = float(0)
    mean_x = float(0)
    mean_y = float(0)
    length_list = len(dataset)
    #for data in LinkedList
    for data in dataset:
        sum_x += data[0]
        sum_y += data[1]
        sum_square_x += data[0] ** 2
        sum_square_y += data[1] ** 2
        sum_xy += data[0] * data[1]
    mean_x = sum_x / length_list
    mean_y = sum_y / length_list
    return (sum_x, sum_y, 
            sum_square_x, sum_square_y, 
            sum_xy, 
            mean_x, mean_y, 
            length_list)

#CalcBetaOne
def CalcBetaOne(sum_xy, length_list, mean_x, mean_y, sum_square_x):
    '''
    Calculate BetaOne.

    Parameters
    ----------
    sum_xy: float,
        Sumatories of product of data x  and data y in dataset
    length_list: int,
        N or Length of pair of data in dataset.
    mean_x:
        Mean of x data in dataset
    mean_y:
        Mean of y data in dataset
    sum_square_x: float,
        Sumatories of squeres of data x in dataset
    Returns
    -------
    beta_one: float,
        beta_one
    '''
    beta_numerator = sum_xy - (length_list * mean_x * mean_y)
    beta_denomintor = sum_square_x - (length_list * mean_x ** 2)
    beta_one = beta_numerator / beta_denomintor
    return beta_one

#CalcBetaZero
def CalcBetaZero(mean_y, beta_one, mean_x):
    '''
    Calculate BetaZero.

    Parameters
    ----------
    mean_x:
        Mean of x data in dataset
    beta_one: float,
        BetaOne
    mean_y:
        Mean of y data in dataset
    
    Returns
    -------
    beta_one: float,
        beta_zero
    '''
    beta_zero = mean_y - (beta_one * mean_x)
    return beta_zero

#CalcCorrelationR
def CalcCorrelationR(length_list, sum_xy, 
                     sum_x, sum_y, sum_square_x, sum_square_y):
    '''
    Calculate Correlation index R.

    Parameters
    ----------
    length_list: int,
        N or Length of pair of data in dataset.
    sum_xy: float,
        Sumatories of product of data x  and data y in dataset
    sum_x: float, 
        Sumatories of data x in dataset
    sum_y: float,
        Sumatories of data x in dataset
    sum_square_x: float,
        Sumatories of squeres of data x in dataset
    sum_square_y: float,
        Sumatories of squeres of data xy in dataset

    Returns
    -------
    correlation_r: float,
        Correlation Index R
    '''
    correlation_r_numerator = (length_list * sum_xy) - (sum_x * sum_y)
    correlation_r_denomintor_one = ((( length_list * sum_square_x ) - 
                                                               ( sum_x ) ** 2 ))
    correlation_r_denomintor_two = (((length_list * sum_square_y ) - 
                                                               ( sum_y ) ** 2 ))
    correlation_r_denomintor = sqrt( correlation_r_denomintor_one * 
                                                  correlation_r_denomintor_two )
    correlation_r = correlation_r_numerator / correlation_r_denomintor 
    return correlation_r

#CalcSquareCorrelation
def CalcSquareCorrelation(correlation_r):
    '''
    Calculate Correlation index R^2

    Parameters
    ----------
    correlation_r: float,
        Correlation Index R

    Returns
    -------
    correlation_square_r: float,
        Square Correlation Index R
    '''
    correlation_square_r = correlation_r ** 2
    return correlation_square_r

#CalcPrediction
def CalcPrediction(beta_zero, beta_one, estimated_proxy_size):
    '''
    Calculate prediction

    Parameters
    ----------
    beta_zero: float,
        Beta Zero
    beta_one: float,
        Beta One
    estimated_proxy_size: float,
        Estimated Proxy Size

    Returns
    -------
    prediction: float,
        Prediction for estimated_proxy_size    

    '''
    prediction = beta_zero + (beta_one * estimated_proxy_size)
    return prediction

#FormatOutput
def FormatOutput(beta_zero, beta_one, 
                correlation_r, correlation_square_r, 
                estimated_proxy_size=False, prediction=False):
    '''
    OutPut whit the optimal Format.
    
    Parameters
    -------
    beta_zero: float,
        Beta Zero
    beta_one: float,
        Beta One
    correlation_r: float,
        Correlation Index R
    correlation_square_r: float,
        Square Correlation Index R
    estimated_proxy_size: float,
        Estimated Proxy Size
       prediction: float,
        Prediction for estimated_proxy_size
    '''
    #Print Header
    print "===================================================================="
    print string.expandtabs("BetaZero\tBetaOne\tCorrelation R\tCorrelation R^2",
                                                                             16)
    print "===================================================================="
    #Print Values
    print string.expandtabs("{0!s}\t{1!s}\t{2!s}\t{3!s}".format(
                            beta_zero, beta_one,
                            correlation_r, correlation_square_r)
                            ,16)
    print "===================================================================="
    if estimated_proxy_size and prediction:
        print ("For E={0!s} The prediction is P={1!s}".format(estimated_proxy_size, prediction))

#main
def main():
    '''Unix parsing command-line options'''
    uso = "modo de uso: %prog [options] "
    parser = OptionParser(uso)
    parser.add_option("-F", "--file", dest="file",
                       help="File Whit Dataset file.csv [file]", metavar="file")
    parser.add_option("-e", "--estimated-proxy-size", 
                 dest="estimated_proxy_size", help="Calculate prediction for E")
    (options, args) = parser.parse_args()
    log.info("START APP")
    if options.file:
        dataset=read_file(options.file)
        if len(dataset) >= 2:
            #Calc sumarizes
            (sum_x,    sum_y, 
            sum_square_x, sum_square_y, 
            sum_xy, 
            mean_x, mean_y, 
            length_list) = CalcSumatories(dataset)
            #Calc BetaOne
            beta_one = CalcBetaOne(sum_xy, length_list, mean_x, 
                                                           mean_y, sum_square_x)
            #Calc BetaZero
            beta_zero = CalcBetaZero(mean_y, beta_one, mean_x)
            #Calc Corelation
            correlation_r = CalcCorrelationR(length_list, 
                               sum_xy, sum_x, sum_y, sum_square_x, sum_square_y)
            #Calc SquareCorelation
            correlation_square_r = CalcSquareCorrelation(correlation_r)
            if options.estimated_proxy_size:
                prediction=CalcPrediction(beta_zero, beta_one, 
                                                   float(options.estimated_proxy_size))
                FormatOutput(beta_zero, beta_one, 
                            correlation_r, correlation_square_r, 
                            options.estimated_proxy_size, prediction)
            else:
                FormatOutput(beta_zero, beta_one, 
                            correlation_r, correlation_square_r)
        else:
             parser.error("File must contaian 2 or more pairs of data")
    else:
        parser.error("please define dataset, %prog -F example.csv\n" 
                                                       "Please use -h for help")

if __name__=='__main__':
    main()