function [averages] = getavg(data, width)
    averages = [];
    for i = (width+1):length(data)
        averages = [averages mean(data(i-width:i))];
    end
end