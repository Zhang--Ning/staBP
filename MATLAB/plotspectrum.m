function plotspectrum(f, fs, t, color)
    NFFT = length(f);
    X = fftshift(fft(f, NFFT));
    fVals = fs*(-NFFT/2:NFFT/2-1)/NFFT;
    plot(fVals, abs(X), color);
    title(t);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
end