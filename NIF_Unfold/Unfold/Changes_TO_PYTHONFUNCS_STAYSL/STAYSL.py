"""!
@file Unfolding/STAYSL.py
@package Unfolding

@defgroup STAYSL STAYSL

@brief Routines support data input and output for STAYSL.

@author James Bevins

@date 27Dec17
"""

import os
import os.path
import sys

import numpy as np
import pandas as pd
import numpy as np

from datetime import datetime
from math import ceil
from subprocess import Popen, PIPE, STDOUT

from Support.Utilities import check_path
from DataAnalysis.DataManipulation import bin_integration

#------------------------------------------------------------------------------#
def bcmToBCF(bcmPath, outPath='flux_history.dat', timeOut='cumulative',
             measOut='differential', measType='flux',
             title='PyScripts Generated BCF file'):
    """
    @ingroup STAYSL
    Converts from a bcm file with the following format 
    
    date time current
    4/26/2017 2:45:16 PM 0.000000014
    
    to a BCF input file format.
    
    Parameters
    ==========
    @param bcmPath: \e string \n
        Absolute path to the input BCM file. \n
    @param outPath: \e string \n
        Absolute path to the created BCF input file. \n
    @param timeOut: \e string \n
        Type of time data output for the BCF input file.  Either 'differential'
        or 'cumulative'. \n
    @param measOut: \e string \n
        Type of measurement output for the BCF input file.  Either 
        'differential' or 'cumulative'. \n
    @param measType: \e string \n
        Type of measurment output in the BCM file.  Either 'flux' or 
        'fluence'. \n
    @param title: \e string \n
        A STAYSL BCF input file title. \n

    """

    # Initialize variables and save header lines
    out = ''
    totTime = 0
    totMeas = 0

    if title.endswith('\n'):
        ntitl = title.count('\n')
    else:
        ntitl = title.count('\n')+1
        title += '\n'
        
    if timeOut.lower() == 'cumulative':
        if measOut.lower() == 'cumulative':
            ntype = 3
        elif measOut.lower() == 'differential':
            ntype = 2
        else:
            print 'ERROR: invalid entry for measOut parameter.'
            return
    elif timeOut.lower() == 'differential':
        if measOut.lower() == 'cumulative':
            ntype = 1
        elif measOut.lower() == 'differential':
            ntype = 0
        else:
            print 'ERROR: invalid entry for measOut parameter.'
            return
    else:
        print 'ERROR: invalid entry for timeOut parameter.'
        return

    if measType.lower() == 'flux':
        mfee = 0
    elif measType.lower() == 'fluence':
        mfee = 1
    else:
        print 'ERROR: Invalid entry for measType paramtere.'
        return
    
    out += '{} {} {} {} {} \n'.format(ntitl, ntype, 0, mfee, 'S')
    out += title
    
    # Open BCM file
    try:
        nrec = 0
        tmpOut = ''
        f = open(bcmPath, 'r')

        # Store first time slice
        line = f.next().rstrip().split('\t')
        nrec += 1
        prevTime = datetime.strptime(line[0]+line[1], '%m/%d/%Y%I:%M:%S %p')

        for line in f:
            line = line.rstrip().split('\t')
            nrec += 1
            curTime = datetime.strptime(line[0]+line[1],
                                        '%m/%d/%Y%I:%M:%S %p')
            curMeas = float(line[2])

            # Store in BCF format
            deltaT = (curTime-prevTime).total_seconds()
            totTime += deltaT
            totMeas += curMeas * deltaT
            if ntype == 0:
                tmpOut += '     {:.2f}          {:.9f}\n'.format(deltaT, curMeas)
            if ntype == 1:
                tmpOut += '     {:.2f}          {:.9f}\n'.format(deltaT, totMeas)
            if ntype == 2:
                tmpOut += '     {:.2f}          {:.9f}\n'.format(totTime, curMeas)
            if ntype == 3:
                tmpOut += '     {:.2f}          {:.9f}\n'.format(totTime,
                                                                 totMeas)

            prevTime = curTime

        # Close the file
        f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

    # Finalize the output file and save
    out += '{}\n'.format(nrec)
    out += tmpOut
    out += '     {:.2f}          {:.4f}\n'.format(0.0, -100)
    try:
        nrec = 0
        tmpOut = ''
        f = open(outPath, 'w')
        f.write(out)

        # Close the file
        f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    
    # Print output
    print 'The total measurement time was {} seconds with an integrated ' \
          'measurement of {}.'.format(totTime, totMeas)

#------------------------------------------------------------------------------#
def integralXSecEst(firPath, numRx, firName='stayslin.out',
                    xSecName='xsectlib_140.dat'):
    """
    @ingroup STAYSL
    Calculates the integral cross section values for the SigPhiCalculator. 
    The results are printed to the screen to be enetered into the
    SigPhiCalculator.
    
    Parameters
    ==========
    @param firPath: \e string \n
        Absolute path to the directory containing the FIR output and cross
        section file. \n
    @param numRx: \e integer \n
        The number of reactions used for the FIR calculation. \n
    @param firName: \e string \n
        Name of the FIR output file. \n
    @param xSecName: \e string \n
        Name of the cross section file. \n
    """

    # Open FIR output file
    try:
        f = open(firPath+firName, 'r')

        # Skip the header
        for i in range(0, 4):
            f.next()

        # Read in the RX names
        rxNames = []
        for i in range(0, numRx):
            splt = f.next().strip().split()
            rxNames.append(splt[0])
        
        # Read in flux
        start = []
        flux = []
        ebin = []
        for line in f:
            splt = line.strip().split()

            if len(splt) > 0:
                if splt[0] == 'GRP':
                    splt = f.next().strip().split()
                    while len(splt) > 3:
                        ebin.append(float(splt[1]))
                        flux.append(float(splt[2]))
                        if (float(splt[1]) >= 5.500E-07 and len(start) == 0) \
                           or (float(splt[1]) >= 0.1 and len(start) == 1) \
                           or (float(splt[1]) >= 1 and len(start) == 2):
                            start.append(int(splt[0])-1)
                        splt = f.next().strip().split()

        # Close the file
        f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

    # Integrate out per MeV and normalize
    flux = bin_integration(ebin, flux, 'low')
    print "The epithermal/thermal ratio is: {}\n".format(
                                           sum(flux[start[0]:start[1]])\
                                           /sum(flux[:start[0]]))
    flux = np.asarray(flux)/sum(flux)

    # Open XSec file
    try:
        f = open(firPath+xSecName, 'r')

        for line in f:
            splt = line.strip().split()

            # Store cross section
            if splt[0] in rxNames:
                print splt[0]
                xSec = []
                for i in range(0,20):
                    splt = f.next().strip().split()
                    for xs in splt:
                        xSec.append(float(xs))

                #Calculate integrals           
                print 'The > 0.1 flux weighted sigma is: {}'.format(
                                sum(np.asarray(xSec[start[1]:]) \
                                *np.asarray(flux[start[1]:])))
                print 'The > 1 flux weighted sigma is: {}'.format(
                                sum(np.asarray(xSec[start[2]:]) \
                                *np.asarray(flux[start[2]:])))

        # Close the file
        f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
#------------------------------------------------------------------------------#
def stayslFlux(df, fluxName='tally', uncertName='uncertainty',
               maxBinAdjust=0, adjFlux=0.0, adjUncert=0.0):
    """
    @ingroup STAYSL
    Converts a tally dataframe to the STAYSL input format to generate the flux
    and flux uncertainy inputs. The results are printed to the screen.

    There are optional parameters to allow for bin adjustments below a specified
    bin if the simulation records a tally of 0.  This is becuase STAYSL will
    not adjust the bin if a zero flux is recorded in the bin.  This can be
    necessary for difficult simulations or where the low-energy portion of the
    spectrum is not well known. This should be used with EXTREME CAUTION.

    Parameters
    ==========
    @param df: <em> pandas dataframe </em> \n
        Absolute path to the input BCM file. \n
    @param fluxName: \e string \n
        Column header for flux in the supplied dataframe. \n
    @param uncertName: \e string \n
        Column header for flux uncertainty in the supplied dataframe. \n
    @param maxBinAdjust: \e integer \n
        The highest bin number to adjust. \n
    @param adjFlux: \e float \n
        The flux to use for bins with zero flux if below maxBinAdjust. \n
    @param adjUncert: \e float \n
        The uncertainty to use for bins with zero flux if below
        maxBinAdjust. \n
    """

    # Output the flux
    out = ' '
    bin = 0
    print "The flux:"
    for f in df[fluxName]:
        if f == 0 and bin < maxBinAdjust:
            f = adjFlux
        out += '{:.4e} '.format(f)
        if len(out)%78==0:
            print out
            out = ' '
        bin += 1
    print out

    # Output the uncertainty
    out = ' '
    bin = 0
    print "The Uncertainty:"
    for f in df[uncertName]:
        if f == 0 and bin < maxBinAdjust:
            f = adjUncert
        out += '{:.4e} '.format(f)
        if len(out)%78==0:
            print out
            out = ' '
        bin += 1
    print out
    
#------------------------------------------------------------------------------#
class IterativeSTAYSL(object):
    """!
    @ingroup STAYSL
    This class creates an object used to perform an iterative STAYSL solution.
    The user can specify the convergence criteria, how to handle the solution
    uncertainty, and the convergence tolerance.

    The class assumes that all of the STAYSL input files follow the STAYSL
    default naming convention and that a complete set of input files has been
    created.
    """

    ##
    def __init__(self, path, chiConv=0.1, stdConv=0.1, updateStd=False,
                 nGrps = 140, **kwargs):
        """!
        Constructor to build the IterativeSTYASL class.

        @param self: <em> object pointer </em> \n
            The object pointer. \n
        @param path: \e string \n
            The path to the base directory containing all of the STAYSL_PNNL
            run files. \n
        @param chiConv: \e integer \n
            The convergence criteria for the $\chi^2$ value. \n
        @param stdConv: \e integer \n
            The convergence criteria for the flux uncertainty. These are
            calculated according to the 2-norm by default, but this can
            be changed using the kwargs. \n
        @param updateStd: \e boolean \n
            Optional specified to update the flux uncertainty with each
            iteration.  If False, the flux uncertainty will not update until
            after the $\chi^2$ convergence criteria has been met.  The
            iteration will then proceed until the flux is converged.  \n
        @param nGrps: \e integer \n
            The number of energy groups used in the unfold. \n
        @param kwargs: <em> optional inputs </em> \n
            An optional list of additional inputs to specify optional inputs
            used by np.linalg.norm(). \n
        """

        ## @var path: \e string
        # The path to the base directory containing all of the STAYSL_PNNL
        # run files.
        self.path = path
        os.chdir(self.path)
        ## @var chiConv: \e integer
        # The convergence criteria for the $\chi^2$ value.
        self.chiConv = chiConv
        ## @var stdConv: \e integer 
        # The convergence criteria for the flux uncertainty.
        self.stdConv = stdConv
        ## updateStd: \e boolean 
        # Optional specified to update the flux uncertainty with each
        # iteration.  
        self.updateStd = updateStd
        ## nGrps: \e integer 
        # The number of energy groups used in the unfold.  
        self.nGrps = nGrps
        
        self.norm = kwargs.pop('norm', 2)

        # Private attributes
        self._dataStart = 99
        self.FirstGroup=15
        self._df = None
        self._normFactor = 1.
        self._inpStr = ''
        self._chi2 = 1E12
        self._stdNorm = 1E12

    def __repr__(self):
        """!
        IterativeSTYASL print function.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """
        return "IterativeSTYASL({}, {}, {}, {}, {})".format(self.path,
                                                        self.chiConv,
                                                        self.stdConv,
                                                        self.updateStd,
                                                        self.nGrps)

    def __str__(self):
        """!
        Human readable IterativeSTYASL print function.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """

        header = ["IterativeSTYASL:"]
        header += ["STAYSL Path: {}".format(self.path)]
        header += ["$\chi^2$ Convergence: {}".format(self.chiConv)]
        header += ["Flux Std  Convergence: {}".format(self.stdConv)]
        header += ["Update Flux Std Each Iteration: {}".format(self.updateStd)]
        header += ["Number of Energy Groups: {}".format(self.nGrps)]
        header = "\n".join(header)+"\n"
        return header

    def find_data(self):
        """!
        Finds the start of the output data in a STAYSL file and the $\chi^2$
        and stores them as class atributes.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """

        nline = 0
        try:
            f = open(self.path+'stayslin.out', 'r')
            Flag=0
            for line in f:
                nline += 1
                spltLine = line.strip().split()
                if len(spltLine) == 7:
                    if spltLine[3] == 'NORM.':
                        self._chi2 = float(spltLine[6])
                if Flag==1:
                    self.FirstGroup = int(spltLine[0])
                    Flag=2
                if line[0:14] == ' GRP    ENERGY':
                    self._dataStart = nline
                    Flag==1


            # Close the file
            f.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            
    def read_output(self):
        """!
        Reads the STAYSL output and saves as a DataFrame. 

        Calculated the norm of the uncertainty.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """

        self._df = pd.read_table(self.path+'stayslin.out', engine='python',
                           sep='\s+', skiprows=self._dataStart, skipfooter=649,
                           header=None,
                           names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio',
                                  'adjStd', 'unadjStd', 'uncertRatio',
                                  'integralFlux', 'intFluxUncert'])
        self._df.apply(pd.to_numeric)
        self._df['adjFlux'] = bin_integration(self._df['lowE'].tolist(), 
                                             self._df['adjFlux'].tolist(), 'low')
        self._df['adjStd'] = self._df['adjStd'] / 100
        self._stdNorm = np.linalg.norm(self._df['adjStd'].tolist(), self.norm)
        # Add in data for groups if first group is not 1. 
        dfi=pd.DataFrame(columns=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio',
                                  'adjStd', 'unadjStd', 'uncertRatio',
                                  'integralFlux', 'intFluxUncert'])
#        print self.FirstGroup
        for a in range(self.FirstGroup-1):
#            print 'hi'
            dfi=dfi.append(pd.Series((1E-11*float(a+1),0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0),
                    index=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio',
                                  'adjStd', 'unadjStd', 'uncertRatio',
                                  'integralFlux', 'intFluxUncert']),ignore_index=True)
        self._df=pd.concat([dfi,self._df])
        #print self._df

    def create_input(self):
        """!
        Creates a STAYSL input string using the input and output from the
        previous run.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """
        self._inpStr = ''
        dfCol = 'adjStd'
        try:
            f = open(self.path+'stayslin.dat', 'r')

            # Skip the first two standard lines
            self._inpStr += f.next()
            self._inpStr += f.next()

            for line in f:
                self._inpStr += line

                # Find the start of the blocks for flux and uncertainty
                if line.strip().split()[0] == str(self.nGrps):
                    if dfCol == 'adjFlux':
                        self._normFactor = float(line.strip().split()[2])
                    inpData = f.next().strip().split()

                    # Add the new data to the input string
                    for d in self._df[dfCol]:
                        if dfCol == 'adjFlux':
                            self._inpStr += ' {:.4e}'.format(d/self._normFactor)
                        elif self.updateStd == False and dfCol == 'adjStd':
                            continue
                        else:
                            self._inpStr += ' {:.4e}'.format(d)
                        inpData.pop(0)
                        if len(inpData) == 0:
                            inpData = f.next().strip().split()
                            self._inpStr += '\n'

                    # Append any 0 flux energy bins to the input
                    if len(inpData) < 15:
                        for d in inpData:
                            self._inpStr += ' ' + d
                        self._inpStr += '\n'
                    dfCol = 'adjFlux'

            # Close the file
            f.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def write_input_file(self):
        """!
        Writes the input file using the created input string.

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """
        try:
            f = open(self.path+'stayslin.dat', 'w')

            f.write(self._inpStr)

            # Close the file
            f.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def run(self):
        """!
        Runs STAYSL iteratively to find a converged flux. 

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """
        prevChi2 = 1E6
        prevStd = 1E6
        prevStd = 1E6
        if check_path(self.path + 'stayslin.out'):
            self.find_data()
            self.read_output()
            print "Chi^2 = {}, Std Norm = {}".format(self._chi2, self._stdNorm)

        # Iterate until Chi2 is converged
        while abs(prevChi2-self._chi2) > self.chiConv:
            prevChi2 = self._chi2
            self._iteration()
            print "Chi^2 = {}".format(self._chi2)

        # Iterate until the uncertainty is converged
        self.updateStd = True
        while abs(prevStd-self._stdNorm) > self.stdConv:
            prevStd = self._stdNorm
            self._iteration()
            print "Std Norm = {}, {}".format(self._stdNorm, prevStd)
            
    def _iteration(self):
        """!
        Performs a STAYSL iteration. 

        @param self: <em> IterativeSTYASL pointer </em> \n
            The IterativeSTYASL pointer. \n
        """

        # Read output and create next input
        if check_path(self.path + 'stayslin.out', printOut=False):
            self.create_input()
            self.write_input_file()

        # Run STAYSL
        p = Popen(['STAYSL_PNNL.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT) 
        p_stdout = p.communicate(input='\n\n')[0]
        p.wait()
        if p.returncode != 0:
            print "ERROR:STAYSL did not execute correctly!"
            sys.exit()

        # Read ouput
        self.find_data()
        self.read_output()

