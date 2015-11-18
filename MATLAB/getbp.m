function [blood_pressure] = getbp(k1, k2, AC, DC)
    blood_pressure = k1*AC + k2*DC;
end