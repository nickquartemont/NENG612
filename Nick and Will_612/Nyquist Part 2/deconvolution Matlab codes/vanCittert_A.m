tmp=importdata('yourfilehere');
ix(:,1)=tmp(:,2);
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
fx(:,1)=ix;
figure;
hold;
plot(fx);
for i=2:10
fx(:,i)=fx(:,i-1)+(ix-(snm*fx(:,i-1)));
end
plot(fx);