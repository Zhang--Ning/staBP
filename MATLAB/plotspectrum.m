function plotspectrum(f, fs)
    T = 1/fs;
    L = length(f);
    t = (0:L-1)*T;
    spec = fft(f);
    P2 = abs(spec/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    freq = fs*(0:(L/2))/L;
    plot(freq, P1);
    title('Spectrum of F');
    xlabel('f (Hz)');
    ylabel('|F(f)|');
end