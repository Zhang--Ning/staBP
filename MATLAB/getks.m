function [k1, k2] = getks(AC, DC, real_systole, real_diastole, real_time_sec, width, fs)
    ac_window = AC(real_time_sec*fs: ((real_time_sec+width)*fs));
    dc_window = DC(real_time_sec*fs: ((real_time_sec+width)*fs));
    [ac_peaks, locs] = findpeaks(ac_window);
    systole_threshold = (max(ac_window)-min(ac_window))*.7+min(ac_window);
    [sys, dia, systimes, diatimes] = extract_sys_dia(ac_window, systole_threshold)

    average_systole = mean(sys);
    average_diastole = mean(dia);
    average_window = mean(dc_window);

    k1 = (real_systole-real_diastole)/(average_systole-average_diastole);
    k2 = (real_systole-(k1*average_systole))/average_window;
end