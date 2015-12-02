%% Setup
%%

%% Raw AC/DC Plots %%
figure(101);
clf;
subplot(2,1,1);
plot((1:length(AC))/200, 5*AC/1024);
title('Pressure Sensor (AC Component)');
xlabel('Time (s)');
ylabel('Sensor Value (V)');
ylim([-1 6]);

subplot(2,1,2);
plot((1:length(DC))/200, 5*DC/1024);
title('Pressure Sensor (DC Component)');
xlabel('Time (s)');
ylabel('Sensor Value (V)');
ylim([-1 6]);

%%

%% Spectrum Plots %%
figure(102);
clf;
subplot(2,1,1);
plotspectrum(AC, 200, 'AC Signal Spectrum', 'b');
subplot(2,1,2);
plotspectrum(DC, 200, 'DC Signal Spectrum', 'b');
%%

%% Filtered Plots %%
filteredAC = LPFilter(AC, 200, 4);
filteredDC = LPFilter(DC, 200, 0.5);

figure(103);
clf;
subplot(2,1,1);
plot((1:length(filteredAC))/200, 5*filteredAC/1024);
title('Headband Pressure Sensor (AC Software 5.0Hz LPF)');
xlabel('Time (s)');
ylabel('Sensor Value (V)');
ylim([-1 6]);

subplot(2,1,2);
plot((1:length(filteredDC))/200, 5*filteredDC/1024);
title('Headband Pressure Sensor (DC Software 0.5Hz LPF)');
xlabel('Time (s)');
ylabel('Sensor Value (V)');
ylim([-1 6]);

figure(104);
clf;
subplot(2,1,1);
plotspectrum(filteredAC, 200, 'AC Signal Spectrum (Software 0.01Hz LPF)', 'b');
subplot(2,1,2);
plotspectrum(filteredDC, 200, 'DC Signal Spectrum (Software 0.5Hz LPF)', 'b');
%%

%% Blood pressure plots %%
t_calib = 1;
[k1, k2] = getks(AC, DC, calib_systoles(t_calib), calib_diastoles(t_calib), calib_times(t_calib), 20*60);
blood_pressure = getbp(k1, k2, AC, DC);

[k1f, k2f] = getks(filteredAC, filteredDC, calib_systoles(t_calib), calib_diastoles(t_calib), calib_times(t_calib), 20*60);
blood_pressure_filtered = getbp(k1f, k2f, filteredAC, filteredDC);

figure(105);
clf;
subplot(2, 1, 1);
plot((1:length(blood_pressure))/200, blood_pressure);
title(sprintf('Calibrated Blood Pressure (k1=%f, k2=%f)', k1, k2));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
ylim([0 200]);

subplot(2, 1, 2);
plot((1:length(blood_pressure_filtered))/200, blood_pressure_filtered);
title(sprintf('Calibrated Filtered Blood Pressure (k1=%f, k2=%f)', k1f, k2f));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
ylim([0 200]);
%

%% Systole, diastole, mean plots %%

% Calculate unfiltered
[sys, dia, systimes, diatimes] = extract_sys_dia(blood_pressure, 100);
if(length(systimes) > length(diatimes))
    meantimes = diatimes;
else
    meantimes = systimes;
end
means = sys(1:length(meantimes))./3+2*dia(1:length(meantimes))./3;

% Plot unfiltered
figure(106)
clf;
subplot(3,1,1);
hold on;
plot(systimes/200, sys, 'r');
plot(diatimes/200, dia, 'b');
plot(meantimes/200, means, 'k');
plot(calib_times/200, calib_systoles, 'or')
plot(calib_times/200, calib_diastoles, 'ob')
plot(calib_times/200, (calib_systoles/3 + 2*calib_diastoles/3), 'ok');
title(sprintf('SDM', k1f, k2f));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
legend('Systoles', 'Diastoles', 'Means', 'Blood Pressure Cuff');
ylim([40 180]);

% Calculate filtered
[sys, dia, systimes, diatimes] = extract_sys_dia(blood_pressure_filtered, 100);
if(length(systimes) > length(diatimes))
    meantimes = diatimes;
else
    meantimes = systimes;
end
means = sys(1:length(meantimes))./3+2*dia(1:length(meantimes))./3;

% Plot filtered
subplot(3,1,2);
hold on;
plot(systimes/200, sys, 'r');
plot(diatimes/200, dia, 'b');
plot(meantimes/200, means, 'k');
plot(calib_times/200, calib_systoles, 'or')
plot(calib_times/200, calib_diastoles, 'ob')
plot(calib_times/200, (calib_systoles/3 + 2*calib_diastoles/3), 'ok');
title(sprintf('SDM (Signal LPF)', k1f, k2f));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
legend('Systoles', 'Diastoles', 'Means', 'Blood Pressure Cuff');
ylim([40 180]);

% Plot averaged
subplot(3,1,3);
width = 30;
hold on;
systimesa = systimes(1:length(systimes)-width);
diatimesa = diatimes(1:length(diatimes)-width);
meantimesa = meantimes(1:length(meantimes)-width);
sysa = getavg(sys, width);
diaa = getavg(dia, width);
meansa = getavg(means, width);
plot(systimesa/200, sysa, 'r');
plot(diatimesa/200, diaa, 'b');
plot(meantimesa/200, meansa, 'k');
plot(calib_times/200, calib_systoles, 'or')
plot(calib_times/200, calib_diastoles, 'ob')
plot(calib_times/200, (calib_systoles/3 + 2*calib_diastoles/3), 'ok');
title(sprintf('SDM (Moving Average w=30)', k1f, k2f));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
legend('Systoles', 'Diastoles', 'Means', 'Blood Pressure Cuff');
ylim([40 180]);
%

%% Calculate drift and accuracy
figure(107)
clf
p = polyfit(systimes/200, sys, 1);
plot(systimes/200, sys);
hold on;
t = min(systimes/200):max(systimes/200);
plot(t, polyval(p, t), 'r');
plot(t, ones(1,length(t))*mean(calib_systoles), 'k');
title(sprintf('Systole regression', k1f, k2f));
xlabel('Time (s)');
ylabel('Blood Pressure (mmHg)');
legend('Systoles', sprintf('P=%ft+%f', p(1), p(2)), 'Mean Systolic Cuff Pressure');
ylim([0, 200]);
drift = abs(p(1))
precision = sqrt(sum((mean(calib_systoles)-sys).^2)/length(sys))
%%