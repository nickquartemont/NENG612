import os
import sys
import pandas as pd
import matplotlib
import numpy as np

# Support Functions path. Adopted from https://github.com/jamesbevins/PyScripts
sys.path.insert(0,os.path.abspath('C:/Users/nickq/Documents/AFIT_Masters/PyScripts/src'))
from Support.Plotting import plot
from Histograms import Histogram

dataPath='Spectra.xlsx'

Data = pd.read_excel(dataPath, "Sheet1", skiprows=0, header=0,
                        parse_cols=[1,4,5])
Data.columns = ['eBins', 'flux', 'sigma']
Histo=Histogram()
Histo.build_histo(Data['eBins'].tolist(), Data['sigma'].tolist(), 
                         uncert= Data['flux'].tolist(), edgeLoc='up')
plt=Histo.plot(xMin=1E-9,xMax=13, logX=True, logY=True, legendLoc=1, includeMarkers=False,
              xLabel='\\textbf{Energy [MeV]}', yLabel='\\textbf{ Flux [n cm$^{-2}$  s$^{-1}$]}',savePath='Pile.png')

