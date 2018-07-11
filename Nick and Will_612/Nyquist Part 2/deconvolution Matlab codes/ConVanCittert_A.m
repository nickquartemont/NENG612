data=importdata('test1Ba133.txt');
ix(:,1)=data(:,1);
x=linspace(-511,512,1024);
s=yourvaluehere;
p(:,1)=1/sqrt(2*pi*s^2)*exp(-(x.^2./(2*s^2)));
for i=1:1024
    if p(i,1)==max(p)
        tshift=i+1;
    end
end
pp=circshift(p,tshift);
snm=toeplitz(pp);
snn=diag(diag(snm));
sm=snn-snm;
fx(:,1)=ix;

k0=.3;

for i=1:10000
k(:,i)=k0.*(1-(2/10^5).*abs(fx(:,i)-(10^5)/2));
fx(:,i+1)=fx(:,i)+k(:,i).*(snn\(ix+sm*fx(:,i)));
end
plot(fx(:,10000));