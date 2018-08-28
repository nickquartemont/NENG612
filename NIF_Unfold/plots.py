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
                        parse_cols=[1, 4,6,20,21])
pinGuessHisto=Histogram()
pinGuessHisto.build_histo(pinGuessData['Energy'].tolist(), pinGuessData['SrcCorr'].tolist(), 
                         uncert=pinGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Pinhole Guess Spectrum}')
diffpinGuessHisto=Histogram()
diffpinGuessHisto.build_histo(pinGuessData['Energy'].tolist(), pinGuessData['Dflux'].tolist(), 
                         uncert=pinGuessData['Derror'].tolist(), edgeLoc='up',
                         name='\\textbf{Pinhole Guess Spectrum}')
# Get data from result without updating standard deviation until the end. 
path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/Pin_N120405_iter/Iteration1/stayslin.out'
df = pd.read_table(path, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])

df.apply(pd.to_numeric)
df['adjFlux'] = bin_integration(df['lowE'].tolist(), df['adjFlux'].tolist(), 'low')
df['adjStd'] = df['adjStd'] * df['adjFlux'] / 100
df1=df


adjHisto = Histogram()
adjHisto.build_histo(df['lowE'].tolist(), df['adjFlux'].tolist(), uncert=df['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ updated $\chi^{2}$/v = 1.86}')



#adjHisto.plot(pinGuessHisto,xMin=1E-6,yMax=4e12,logX=False, logY=False,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Pin.png',includeMarkers=False,
#                  legendLoc=2)
#adjHisto.plot(pinGuessHisto,xMin=1E-6, yMin=1, logX=False, logY=True,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Pin1.png',includeMarkers=False,
#                  legendLoc=3)
#adjHisto.plot(pinGuessHisto,xMin=1E-6, yMin=100, logX=True, logY=True,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Pin2.png',includeMarkers=False,
#                  legendLoc=3)
# Differential 
ddf = pd.read_table(path, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf.apply(pd.to_numeric)

ddf['adjStd'] = ddf['adjStd'] * ddf['adjFlux'] / 100

diffadjHisto = Histogram()
diffadjHisto.build_histo(ddf['lowE'].tolist(), ddf['adjFlux'].tolist(), uncert=ddf['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ updated $\chi^{2}$/v = 1.86}')


# Get data from result with updating standard deviation until the end. 
path2 = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/Pin_N120405_iter/Iteration2/stayslin.out'
ddf2 = pd.read_table(path2, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf2.apply(pd.to_numeric)
ddf2['adjStd'] = ddf2['adjStd'] * ddf['adjFlux'] / 100
diff2adjHisto = Histogram()
diff2adjHisto.build_histo(ddf2['lowE'].tolist(), ddf2['adjFlux'].tolist(), uncert=ddf2['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ not updated $\chi^{2}$/v = 22.0}')


diff2adjHisto.plot(diffadjHisto,diffpinGuessHisto,xMin=1E-6, yMin=10**8,yMax=10**13, logX=True, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Pin3.png',includeMarkers=False,
                  legendLoc=3)
diff2adjHisto.plot(diffadjHisto,diffpinGuessHisto,xMin=1E-6, yMin=10**8,yMax=10**13, logX=False, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Pin4.png',includeMarkers=False,
                  legendLoc=3)
#%% Basket Results 
baskGuessData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1,10,12,22,23])

baskGuessHisto=Histogram()
baskGuessHisto.build_histo(baskGuessData['Energy'].tolist(), baskGuessData['SrcCorr'].tolist(), 
                         uncert=baskGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Basket Guess Spectrum}')
diffbaskGuessHisto=Histogram()
diffbaskGuessHisto.build_histo(baskGuessData['Energy'].tolist(), baskGuessData['Dflux'].tolist(), 
                         uncert=baskGuessData['Derror'].tolist(), edgeLoc='up',
                         name='\\textbf{Basket Guess Spectrum}')
# Get data from result without updating standard deviation until the end. 
path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/BASK_N120405_iter/Iteration2/stayslin.out'
df = pd.read_table(path, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])

df.apply(pd.to_numeric)
df['adjFlux'] = bin_integration(df['lowE'].tolist(), df['adjFlux'].tolist(), 'low')
df['adjStd'] = df['adjStd'] * df['adjFlux'] / 100
df2=df

adjHisto = Histogram()
adjHisto.build_histo(df['lowE'].tolist(), df['adjFlux'].tolist(), uncert=df['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{STAYSL $\chi^{2}$/v = 9.5}')

#adjHisto.plot(baskGuessHisto,xMin=1E-6,logX=False, logY=False,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Bask.png',includeMarkers=False,
#                  legendLoc=2)
#adjHisto.plot(baskGuessHisto,xMin=1E-6, yMin=1, logX=False, logY=True,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Bask1.png',includeMarkers=False,
#                  legendLoc=3)
#adjHisto.plot(baskGuessHisto,xMin=1E-6, yMin=1, logX=True, logY=True,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'Bask2.png',includeMarkers=False,
#                  legendLoc=3)

# Differential 

ddf = pd.read_table(path, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf.apply(pd.to_numeric)
ddf['adjStd'] = ddf['adjStd'] * ddf['adjFlux'] / 100

diffadjHisto = Histogram()
diffadjHisto.build_histo(ddf['lowE'].tolist(), ddf['adjFlux'].tolist(), uncert=ddf['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ updated $\chi^{2}$/v = 9.5}')

path3 = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/BASK_N120405_iter/Iteration3/stayslin.out'
ddf3 = pd.read_table(path3, engine='python', sep='\s+', skiprows=99, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf3.apply(pd.to_numeric)
ddf3['adjStd'] = ddf3['adjStd'] * ddf3['adjFlux'] / 100

diff3adjHisto = Histogram()
diff3adjHisto.build_histo(ddf3['lowE'].tolist(), ddf3['adjFlux'].tolist(), uncert=ddf3['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ not updated $\chi^{2}$/v = 89}')

diff3adjHisto.plot(diffadjHisto,diffbaskGuessHisto,xMin=1E-6, yMin=10**7, yMax=10**13,logX=True, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Bask3.png',includeMarkers=False,
                  legendLoc=2)
diff3adjHisto.plot(diffadjHisto,diffbaskGuessHisto,xMin=1E-6, yMin=10**7, yMax=10**13,logX=False, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'Bask4.png',includeMarkers=False,
                  legendLoc=2)
#%% Kinematic Base Results

kbasGuessData = pd.read_excel(data, "Guess_SpecMCNP_Results", skiprows=1, header=0,
                        parse_cols=[1, 16,18,24,25])

kbasGuessHisto=Histogram()
kbasGuessHisto.build_histo(kbasGuessData['Energy'].tolist(), kbasGuessData['SrcCorr'].tolist(), 
                         uncert=kbasGuessData['Error'].tolist(), edgeLoc='up',
                         name='\\textbf{Kinematic Base Guess Spectrum}')
diffkbasGuessHisto=Histogram()
diffkbasGuessHisto.build_histo(kbasGuessData['Energy'].tolist(), kbasGuessData['Dflux'].tolist(), 
                         uncert=kbasGuessData['Derror'].tolist(), edgeLoc='up',
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
                     edgeLoc='low',name='\\textbf{STAYSL $\chi^{2}$/v = 0.48}')

#kbasGuessHisto.plot(adjHisto,xMin=1E-6,xMax=17,yMax=2e10,logX=False, logY=False,
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'KBas.png',includeMarkers=False,
#                  legendLoc=2)
#adjHisto.plot(kbasGuessHisto,yMax=1E11,xMin=1E-6, yMin=10000, logX=False, logY=True, 
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'KBAS1.png',includeMarkers=False,
#                  legendLoc=4)
#adjHisto.plot(kbasGuessHisto,yMax=1E11,xMin=1E-6, yMin=10000, logX=True, logY=True, 
#                  xLabel='Energy [MeV]', yLabel='Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'KBAS2.png',includeMarkers=False,
#                  legendLoc=4)


# Differential 
path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/KBAS_N120405_iter/Iteration1/stayslin.out'

ddf = pd.read_table(path, engine='python', sep='\s+', skiprows=95, skipfooter=649, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf.apply(pd.to_numeric)
ddf['adjStd'] = ddf['adjStd'] * ddf['adjFlux'] / 100

diffadjHisto = Histogram()
diffadjHisto.build_histo(ddf['lowE'].tolist(), ddf['adjFlux'].tolist(), uncert=ddf['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ not updated $\chi^{2}$/v = 0.48}')



# With Updating Std Dev 

path = 'C:/Users/nickq/Documents/AFIT_Masters/NENG612/NIF_Unfold/Unfold/STAYSL/KBAS_N120405_iter/Iteration2/stayslin.out'

ddf22 = pd.read_table(path, engine='python', sep='\s+', skiprows=95, skipfooter=647, header=None,
                   names=['lowE', 'adjFlux', 'unadjFlux', 'fluxRatio', 'adjStd', 
                          'unadjStd', 'uncertRatio', 'integralFlux', 'intFluxUncert'])
ddf22.apply(pd.to_numeric)
ddf22['adjStd'] = ddf22['adjStd'] * ddf22['adjFlux'] / 100

diff22adjHisto = Histogram()
diff22adjHisto.build_histo(ddf['lowE'].tolist(), ddf['adjFlux'].tolist(), uncert=ddf['adjStd'].tolist(),
                     edgeLoc='low',name='\\textbf{$\sigma$ updated $\chi^{2}$/v = 0.71}')


diffadjHisto.plot(diff22adjHisto,diffkbasGuessHisto,xMin=1E-6, yMin=10**4, logX=True, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'KBAS3.png',includeMarkers=False,
                  legendLoc=3)
diffadjHisto.plot(diff22adjHisto,diffkbasGuessHisto,xMin=1E-6, yMin=10**4, logX=False, logY=True,
                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
                  savePath=outpath+'KBAS4.png',includeMarkers=False,
                  legendLoc=3)
#diff22adjHisto.plot(diffadjHisto,diffkbasGuessHisto,xMin=1E-6, yMin=100, logX=False, logY=True,
#                  xLabel='Energy [MeV]', yLabel='Differential Neutron Fluence [n/cm$^2$]',
#                  savePath=outpath+'KBAS4.png',includeMarkers=False,
#                  legendLoc=3)


