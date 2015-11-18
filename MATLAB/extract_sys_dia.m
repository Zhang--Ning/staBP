function [sys, dia, systimes, diatimes] = extract_sys_dia(blood_pressure, threshold)
    %simplePeakDetector Return times and voltages of samples above threshold 9
    sys = [];
    dia = [];
    systimes = [];
    diatimes = [];
    train = [];
    find_sys = 1;
    for i = 1:length(blood_pressure)
        pressure = blood_pressure(i);
        if(find_sys)
            if pressure > threshold
                train = [train i];
            else
                [~, maxTrain] = max(blood_pressure(train));
                maxPressure = blood_pressure(train(maxTrain));
                maxTime = train(maxTrain);
                systimes = [systimes maxTime];
                sys = [sys maxPressure];
                train = [];
                find_sys = 0;
            end
        else
            if pressure <= threshold
                train = [train i];
            else
                [~, minTrain] = min(blood_pressure(train));
                minPressure = blood_pressure(train(minTrain));
                minTime = train(minTrain);
                diatimes = [diatimes minTime];
                dia = [dia minPressure];
                train = [];
                find_sys = 1;
            end
        end
    end
end