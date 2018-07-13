close all; 
Energy=Test1Calibrated(:,3); 
Channel=Test1Calibrated(:,1);
DataTest1=Test1Calibrated(:,2); 
DataTest2=test2(:,2); 
DataTest3=test3(:,2);
%% Original Data for Ba-133
figure(1)
hold on 
semilogy(Energy,DataTest1,'k-'); 
semilogy(Energy,DataTest2,'k--'); 
semilogy(Energy,DataTest3,'k.-'); 
xlabel('Energy [keV]')
ylabel('Counts')
legend('Test1 Ba-133','Test2','Test3')
set(gca, 'YScale', 'log')
hold off

%% Do FFT on all data 
% Folding frequency based on source in folder - Penn State 
f=1*(0:(1024/2))/1024; 
FFT1=fft(DataTest1);
FFT2=fft(DataTest2);
FFT3=fft(DataTest3);
C1=abs(FFT1/1024); 
C2=abs(FFT1/1024); 
C3=abs(FFT1/1024); 

figure(2)
hold on 
plot(f,C(1:1024/2+1),'k-')
plot(f,C(1:1024/2+1),'k--')
plot(f,C(1:1024/2+1),'k.-')
xlabel('A*Counts^-1')
ylabel('|C(f)|')
legend('Test1 Ba-133','Test2','Test3')
hold off 




%% Apply METZ Filter to all Data. Just to see.
x=linspace(-511,512,1024);
s=7.404;
F1=fft(DataTest1);
F2=fft(DataTest2);
F3=fft(DataTest3);
tmp=1/sqrt(2*pi*s^2)*exp(-(x.^2./(2*s^2)));
for i=1:1024
    p(i,1)=tmp(i);
end
P=fft(p);
n=20;
Metz=(1-(1.-P.^2).^n)./P;
Metz(isnan(Metz))=0;
g1=abs(ifft(Metz.*F1));
g2=abs(ifft(Metz.*F2));
g3=abs(ifft(Metz.*F3));
Data1=fftshift(g1);
Data2=fftshift(g2);
Data3=fftshift(g3);
% Check that the data looks similar 
figure(3)
subplot(2,2,1)
hold on 
plot(Channel,DataTest1,'k-')
plot(Channel,Data1,'k--')
xlim([0 120])
title('Data1')
hold off 
subplot(2,2,2)
hold on 
plot(Channel,DataTest2,'k-')
plot(Channel,Data2,'k--')
title('Data2')
xlim([0 120])
hold off
subplot(2,2,3)
hold on 
plot(Channel,DataTest3,'k-')
plot(Channel,Data3,'k--')
title('Data3')
xlim([0 120])
hold off 

% The Metz filter, as expected messes up the plot. There is 
% not enough high frequency noise in the system. Data does not converge for
% any value of n. Tried bi-section method. 

%% VanCittert 
