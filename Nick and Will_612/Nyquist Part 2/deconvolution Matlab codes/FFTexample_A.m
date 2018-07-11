close all
clear all
clc

w = 10; %angular frequency in [Hz]
t_max = 3; %time in seconds
dt = 0.01;

t = [0:dt:t_max];

f = sin(2*pi*w*t);
n=length(f);

figure(1)
subplot(2,2,1)
plot(t,f,'b.-')
xlabel('time [sec]')
ylabel('magnitude')

FT = fft(f);
%FT(1) = [];
power = abs(FT(1:floor(n/2))).^2;

nyquist = 1/(2*dt);
freq = (1:n/2)/(n/2)*nyquist;

subplot(2,2,2)
plot(freq,power,'b.-')
xlabel('Hz')
ylabel('Power')

f_noise = normrnd(f,2);

subplot(2,2,3)
plot(t,f_noise,'b.-')
xlabel('time [sec]')
ylabel('magnitude')

FT_noise = fft(f_noise);
FT_noise(1) = [];
power_noise = abs(FT_noise(1:floor(n/2))).^2;

nyquist = 1/(2*dt);
freq = (1:n/2)/(n/2)*nyquist;

subplot(2,2,4)
plot(freq,power_noise,'b.-')
xlabel('Hz')
ylabel('Power')

