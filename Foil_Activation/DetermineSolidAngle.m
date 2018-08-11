
d=4;
a=2;
Point=pi*a^2/d^2
s=0.25;
alpha=(s/d)^2;
Beta=(a/d)^2;
F1=(5/16)*(Beta/(1+Beta)^(7/2))-(35/64)*(Beta^2)/(1+Beta)^(9/2);
F2=(35/128)*(Beta/(1+Beta)^(9/2))-(315/256)*(Beta^2)/(1+Beta)^(11/2)+(1155/1024)*(Beta^3)/(1+Beta)^(13/2);
Omega=2*pi*(1-(1/(1+Beta)^(1/2))-(3/8)*(alpha*Beta/(1+Beta)^(5/2))+alpha^2*F1-alpha^3*F2)