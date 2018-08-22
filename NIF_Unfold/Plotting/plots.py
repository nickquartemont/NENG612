import sys
import os
sys.path.insert(0,os.path.abspath('C:/Users/nickq/Documents/AFIT_Masters/PyScripts/src'))
import pandas as pd
import matplotlib as plt 

datapath='C:\Users\nickq\Documents\AFIT_Masters\NENG612\NIF_Unfold'
data=datapath+'\\ActivationData.xlsx'

#%% Pinhole results 

pinData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1, 4,5])
#objData.columns = ['eBins', 'flux', 'sigma']
#print "The objective spectrum data:\n", objData.head(10)
#
#objHisto=Histogram()
#objHisto.build_histo(objData['eBins'].tolist(), objData['flux'].tolist(), 
#                         uncert=objData['sigma'].tolist(), edgeLoc='up',
#                         name='\\textbf{Objective TN+PFNS}')