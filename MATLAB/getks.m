function [k1, k2] = getks(AC, DC, real_systole, real_diastole, real_time, width)
    ac_window = AC(real_time: (real_time+width));
    dc_window = DC(real_time: (real_time+width));
    threshold = (max(ac_window)-min(ac_window))*0.7+min(ac_window);
    [sys, dia, ~, ~] = extract_sys_dia(ac_window, threshold);

    average_systole = mean(sys);
    average_diastole = mean(dia);
    average_window = mean(dc_window);

    k1 = (real_systole-real_diastole)/(average_systole-average_diastole);
    k2 = (real_systole-(k1*average_systole))/average_window;
end