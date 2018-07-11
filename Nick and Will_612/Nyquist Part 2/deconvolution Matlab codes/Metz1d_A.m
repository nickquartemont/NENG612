tmp=importdata('yourfilehere');
fx(:,1)=tmp(:,2);
x=linspace(-511,512,1024);
s=yourvaluehere;
F=fft(fx);
tmp=1/sqrt(2*pi*s^2)*exp(-(x.^2./(2*s^2)));
for i=1:1024
    p(i,1)=tmp(i);
end
P=fft(p);
n=10;
Metz=(1-(1.-P.^2).^n)./P;
Metz(isnan(Metz))=0;
g=abs(ifft(Metz.*F));
gg=fftshift(g);
plot(gg);




