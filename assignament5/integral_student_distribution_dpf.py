#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
#
#       integral_student_distribution_dpf.py
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
from scipy.stats import t
from numpy import abs

LOG_FILENAME = 'IntegrateSimpsonRule.log'
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('INTEGRATE')
handler = logging.FileHandler(LOG_FILENAME)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

#pdf
def pdf(x, dof):
	'''
    Parameters
    ----------
    x: float, calc funcion in x.
        calc funcion in x
    dof: int, degrees of freedom.
        which is constant within each integration test case
    Returns
    -------
    pdf: float, probability in x
    	probability in x
    '''
    #research in scipy incorporate stats and T distribution. pdf.
	return t.pdf(t, dof)

#IntegrateSimpsonRule
def IntegrateSimpsonRule(x, dof, 
						initial_steps=10, min_error=0.0000001, 
						max_steps=10000):
	'''
    Parameters
    ----------
    x: float, calc funcion in x.
        calc funcion in x
    dof: int, degrees of freedom.
        which is constant within each integration test case
    initial_steps: int, initial steps
        Number of steps for the integral
    min_error: float, minimal error
        minimal error defaul(0.0000001)
    max_steps: int, max number of interaction.
    	Max number of interaction for 
    	aboid infinite loops (defaul=10000)
    Returns
    -------
    integral_pdf: float, Area 
    	The total probability is the area of the pdf
	'''
	#min_error
	#max_steps
	#steps
	E=1
	steps=initial_steps
	#w = x / steps
	w = x / steps
	#last_result=none
	last_result=None
	#while:
	while:
		#result = pdf(0, dof)
		result = pdf(0, dof)
		#for step in range(1, (steps):
			for step in range(1, steps):
			#xi=w * step
			xi=w * step
			#if number % 2 == 0:
			if step % 2 == 0:
				#is even
				#result += 2 * pdf(xi, dof)
				result += 2 * pdf(xi, dof)
			#else:
			else:
				#is odd
				#result += 4 * pdf(xi, dof)
				result += 4 * pdf(xi, dof)
		#result += pdf(x, dof)
		result += pdf(x, dof)
		#result = ( float(w) / float(3)) * result )
		result = ( float(w) / float(3)) * result )
		#if not last_result:
		if not last_result:
			#steps = steps * 2
			steps = steps * 2
			w = x / steps
			#last_result=result:
			log.info("first result %s whit %s" % (result, steps))
			last_result=result:
		#else:
		else:
			#E=abs(result - last_result)
			log.info("result %s whit %s" % (result, steps))
			E=abs(result - last_result)
			log.info("Error %s" % (E))
			#if ( not E < min_error ) and ( step < max_steps ):
			if E > min_error:
				#last_result=result
				last_result=result
				log.debug("recalculatin steps for minimal error")
				#steps = steps * 2
				steps = steps * 2
				if steps > max_steps:
					log.debug("recalculatin steps for minimal error")
					break
				log.debug("recalculatin steps to %s" % steps)
				w = x / steps
			else:
				log.info("Great!!\n"
						"Integral:%s"
						"Error:%s"
						"Steps:%s" % (result, E, steps))
				break
	return result, E, steps


#main
    #give options.
    #t: pasar t (obligatorio)
    #d: pasar dof (obligatorio)
    #E: pasar error minimo
    #S: pasos iniciales
    #M: Maximo de pasos
    #if t and d option:
    	#if dof >= 1:
    		#IntegrateSimpsonRule
    		#print result
    	#else:
    		#mesnsaje: dof debe ser mayor a 1	
    #else 
        #mesnsaje: Print help
 def main():
    '''Unix parsing command-line options'''
    #give options.
    uso = "modo de uso: %prog [options] "
    parser = OptionParser(uso)
    parser.add_option("-t", dest="t",
                    help="t in distribution pdf")
    parser.add_option("-d", "--dof" dest="dof",
                    help="degrees of freedom (dof >=1)")
    parser.add_option("-E", "--min_error" dest="min_error", default=0.0000001,
                    help="minimal error defaul(0.0000001)")
    parser.add_option("-S", "--initial_steps" dest="initial_steps", default=10,
                    help="Number of initial steps for the integral")
    parser.add_option("-M", "--max_steps" dest="max_steps",  default=100000,
                    help="Max number of interaction (defaul=100000)")
    (options, args) = parser.parse_args()
    log.info("START APP")
    if options.t and options.dof:
        result, E, steps = IntegrateSimpsonRule( 
        					float(options.t), options.dof, 
        					initial_steps=options.initial_steps, 
        					min_error=options.min_error, 
							max_steps=options.max_steps
        				)
		print result
    else:
        parser.error("please define t and dof, %prog -t 1.1 -d 9\n" 
                                                       "Please use -h for help")

if __name__=='__main__':
    main()