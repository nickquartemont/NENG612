import sys
import os
sys.path.insert(0,os.path.abspath('C:/Users/nickq/Documents/AFIT_Masters/PyScripts/src'))
import pandas as pd
import matplotlib as plt 
from Histograms import Histogram
from DataAnalysis.DataManipulation import bin_integration, bin_differentiation
from DataAnalysis.Histograms import Histogram

data='ActivationData.xlsx'
outpath ='C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/Figs/'

#%% Pinhole results 

pinGuessData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1, 4,6])

pinGuessHisto=Histogram()
pinGuessHisto.build_histo(pinGuessData['Energy'].tolist(), pinGuessData['SrcCorr'].tolist(), 
                         uncert=pinGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Pinhole Guess Spectrum}')

# Get data from result without updating standard deviation until the end. 
path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/Pin_N120405_iter/Iteration1/stayslin.out'
df = pd.read_table(path, engine='python', sep='\s+', skiprows=95, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])

df.apply(pd.to_numeric)
df['adjFlux'] = bin_integration(df['lowE'].tolist(), df['adjFlux'].tolist(), 'low')
df['adjStd'] = df['adjStd'] * df['adjFlux'] / 100
df1=df

adjHisto = Histogram()
adjHisto.build_histo(df['lowE'].tolist(), df['adjFlux'].tolist(), uncert=df['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{NIF Guess $\chi^{2}$/v = 1.86}')

adjHisto.plot(pinGuessHisto,xMin=1E-6,logX=False, logY=False,
                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Pin.png',includeMarkers=False,
                  legendLoc=2)
adjHisto.plot(pinGuessHisto,xMin=1E-6, yMin=1, logX=False, logY=True,
                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Pin1.png',includeMarkers=False,
                  legendLoc=2)

#%% Basket Results 
baskGuessData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1,10,12])

baskGuessHisto=Histogram()
baskGuessHisto.build_histo(baskGuessData['Energy'].tolist(), baskGuessData['SrcCorr'].tolist(), 
                         uncert=baskGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Basket Guess Spectrum}')
#%% Kinematic Base Results

kbasGuessData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1, 16,18])

kbasGuessHisto=Histogram()
kbasGuessHisto.build_histo(kbasGuessData['Energy'].tolist(), kbasGuessData['SrcCorr'].tolist(), 
                         uncert=kbasGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Kinematic Base Guess Spectrum}')

# Get data from result without updating standard deviation until the end. 
path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/KBAS_N120405_iter/Iteration1/stayslin.out'
df = pd.read_table(path, engine='python', sep='\s+', skiprows=95, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])

df.apply(pd.to_numeric)
df['adjFlux'] = bin_integration(df['lowE'].tolist(), df['adjFlux'].tolist(), 'low')
df['adjStd'] = df['adjStd'] * df['adjFlux'] / 100

adjHisto = Histogram()
adjHisto.build_histo(df['lowE'].tolist(), df['adjFlux'].tolist(), uncert=df['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{NIF Guess $\chi^{2}$/v = 0.48}')

kbasGuessHisto.plot(adjHisto,xMin=1E-6,xMax=20,logX=False, logY=False,
                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'KBas.png',includeMarkers=False,
                  legendLoc=2)
adjHisto.plot(kbasGuessHisto,yMax=1E11,xMin=1E-6, yMin=10000, logX=False, logY=True, 
                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'KBAS1.png',includeMarkers=False,
                  legendLoc=4)
