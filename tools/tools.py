import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert, filtfilt, butter, lfilter


def fft_normalized(signal, count_samples, sampling_frequency):
    yf = fft(signal)
    yf_normalized = 2.0 / count_samples * np.abs(yf[0:count_samples // 2])
    xf = fftfreq(count_samples, 1 / sampling_frequency)[:count_samples // 2]
    return yf_normalized, xf


def butter_bandpass(lowcut, highcut, fs, order=20):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def envelope_signal(signal, band, sampling_frequency, count_samples):
    filtered = butter_bandpass_filter(signal, band[0], band[1], sampling_frequency)
    ev = np.abs(hilbert(filtered, count_samples))
    return ev



