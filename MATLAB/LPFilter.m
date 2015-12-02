function filtered = LPFilter(f, fs, cutoff)
    NFFT = length(f);
    X = fftshift(fft(f));
    cutoffSamplePos = fix((cutoff*NFFT/fs) + (NFFT/2));
    cutoffSampleNeg = fix(-(cutoff*NFFT/fs) + (NFFT/2));
    X(cutoffSamplePos:end) = 0;
    X(1:cutoffSampleNeg) = 0;
    filtered = abs(ifft(ifftshift(X)));
end