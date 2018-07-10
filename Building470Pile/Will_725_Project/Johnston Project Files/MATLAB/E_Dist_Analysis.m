
load('Project_Data.mat')

% Point Detector Plots
for j = 1:9
    Stringer = strcat('Tally.Point.Stringer_',num2str(j));
    Title = char(strcat({'Energy Distribution Stringer '},{num2str(j)}));
    figure('Name',Title,'NumberTitle','off')
    x = Tally.Energy;
    y1 = eval(strcat(Stringer,'.Left.Flux'))*1.006e7;
    y2 = eval(strcat(Stringer,'.Middle.Flux'))*1.006e7;
    y3 = eval(strcat(Stringer,'.Right.Flux'))*1.006e7;
    error1 = eval(strcat(Stringer,'.Left.Error')).*y1;
    error2 = eval(strcat(Stringer,'.Middle.Error')).*y2;
    error3 = eval(strcat(Stringer,'.Right.Error')).*y3;
    ax = axes();
    errorbar(ax,x,y1,error1,'k-'); hold on;
    errorbar(ax,x,y2,error2,'b--'); hold on;
    errorbar(ax,x,y3,error3,'r:'); hold off;
    set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
    legend('Left Point','Middle Point','Right Point')
    title(Title);
    xlabel('Neutron Energy [MeV]')
    ylabel('Counts')
    FileName = char(strcat({'Stringer '},{num2str(j)},{'.png'}));
    saveas(gcf,FileName);
end
for j = 10:12
    Stringer = strcat('Tally.Point.Stringer_',num2str(j));
    Title = char(strcat({'Energy Distribution Stringer '},{num2str(j)}));
    figure('Name',Title,'NumberTitle','off')
    x = Tally.Energy;
    y1 = eval(strcat(Stringer,'.Back.Flux'))*1.006e7;
    y2 = eval(strcat(Stringer,'.Middle.Flux'))*1.006e7;
    y3 = eval(strcat(Stringer,'.Front.Flux'))*1.006e7;
    error1 = eval(strcat(Stringer,'.Back.Error')).*y1;
    error2 = eval(strcat(Stringer,'.Middle.Error')).*y2;
    error3 = eval(strcat(Stringer,'.Front.Error')).*y3;
    ax = axes();
    errorbar(x,y1,error1,'k-'); hold on;
    errorbar(x,y2,error2,'b--'); hold on;
    errorbar(x,y3,error3,'r:'); hold off;
    set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
    legend('Back Point','Middle Point','Front Point')
    title(Title);
    xlabel('Neutron Energy [MeV]')
    ylabel('Counts')
    FileName = char(strcat({'Stringer '},{num2str(j)},{'.png'}));
    saveas(gcf,FileName);
end

% Volume Detector Plots
figure('Name','Energy Distribution Stringer 5 Partially Removed','NumberTitle','off')
x = Tally.Energy;
y = Tally.Volume.Partial.Flux*1.006e7;
error = Tally.Volume.Partial.Error.*y;
ax = axes();
errorbar(x,y,error,'g-');
set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
title('Energy Distribution of 4"x8"x4" Volume of Stringer 5 Partially Removed')
xlabel('Neutron Energy [MeV]')
ylabel('Counts')
saveas(gcf,'Volume Partial.png')

figure('Name','Energy Distribution Stringer 5 Fully Removed','NumberTitle','off')
x = Tally.Energy;
y = Tally.Volume.Full.Flux*1.006e7;
error = Tally.Volume.Full.Error.*y;
ax = axes();
errorbar(x,y,error,'g-');
set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
title('Energy Distribution of Centered 4"x8"x4" Volume of Stringer 5 Fully Removed')
xlabel('Neutron Energy [MeV]')
ylabel('Counts')
saveas(gcf,'Volume Full.png')

% Combined Plots
figure('Name','Stringer 5 Comparison with Partial Removal','NumberTitle','off')
x = Tally.Energy;
y1 = Tally.Point.Stringer_5.Left.Flux*1.006e7;
y2 = Tally.Point.Stringer_5.Middle.Flux*1.006e7;
y3 = Tally.Point.Stringer_5.Right.Flux*1.006e7;
y4 = Tally.Volume.Partial.Flux*1.006e7;
error1 = Tally.Point.Stringer_5.Left.Error.*y1;
error2 = Tally.Point.Stringer_5.Middle.Error.*y2;
error3 = Tally.Point.Stringer_5.Right.Error.*y3;
error4 = Tally.Volume.Partial.Error.*y4;
ax = axes();
errorbar(x,y1,error1,'k-'); hold on;
errorbar(x,y2,error2,'b--'); hold on;
errorbar(x,y3,error3,'r:'); hold on;
errorbar(x,y4,error4,'g-'); hold off;
set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
legend('Left Point','Middle Point','Right Point','Partially Removed')
title('Stringer 5 Comparison with Partial Removal');
xlabel('Neutron Energy [MeV]')
ylabel('Counts')
saveas(gcf,'Partial Comparison.png');

figure('Name','Stringer 5 Comparison with Full Removal','NumberTitle','off')
x = Tally.Energy;
y1 = Tally.Point.Stringer_5.Left.Flux*1.006e7;
y2 = Tally.Point.Stringer_5.Middle.Flux*1.006e7;
y3 = Tally.Point.Stringer_5.Right.Flux*1.006e7;
y4 = Tally.Volume.Full.Flux*1.006e7;
error1 = Tally.Point.Stringer_5.Left.Error.*y1;
error2 = Tally.Point.Stringer_5.Middle.Error.*y2;
error3 = Tally.Point.Stringer_5.Right.Error.*y3;
error4 = Tally.Volume.Full.Error.*y4;
ax = axes();
errorbar(x,y1,error1,'k-'); hold on;
errorbar(x,y2,error2,'b--'); hold on;
errorbar(x,y3,error3,'r:'); hold on;
errorbar(x,y4,error4,'g-'); hold off;
set(ax, 'YScale', 'log', 'XScale', 'log', 'XLim', [0,12], 'YLim', [10^-6,10^4]);
legend('Left Point','Middle Point','Right Point','Fully Removed')
title('Stringer 5 Comparison with Fully Removal');
xlabel('Neutron Energy [MeV]')
ylabel('Counts')
saveas(gcf,'Full Comparison.png');






