import numpy as np
from scipy.fft import fft, ifft, fftfreq
from typing import Tuple

class SignalReconstructor:
    """
    Provides various filtering algorithms to reconstruct signals from noisy detector data.
    """
    
    @staticmethod
    def moving_average(signal: np.ndarray, window_size: int = 5) -> np.ndarray:
        """
        Applies a simple moving average filter.
        
        Args:
            signal: Noisy input signal.
            window_size: Size of the averaging window.
            
        Returns:
            np.ndarray: Filtered signal.
        """
        if window_size < 1:
            return signal
        
        # Pad signal to maintain length
        padding = window_size // 2
        padded_signal = np.pad(signal, (padding, padding), mode='edge')
        
        # Use convolution for efficiency
        kernel = np.ones(window_size) / window_size
        filtered = np.convolve(padded_signal, kernel, mode='valid')
        
        # Ensure output matches input length exactly (convolution 'valid' might differ slightly)
        return filtered[:len(signal)]

    @staticmethod
    def fourier_filter(signal: np.ndarray, dt: float, cutoff_freq: float) -> np.ndarray:
        """
        Applies a Fourier low-pass filter.
        
        Args:
            signal: Noisy input signal.
            dt: Time step size (sampling period).
            cutoff_freq: Frequency threshold for the low-pass filter.
            
        Returns:
            np.ndarray: Filtered signal.
        """
        n = len(signal)
        # 1. Transform to frequency domain
        yf = fft(signal)
        xf = fftfreq(n, dt)
        
        # 2. Apply low-pass threshold (zero out high frequencies)
        yf_filtered = yf.copy()
        yf_filtered[np.abs(xf) > cutoff_freq] = 0
        
        # 3. Inverse transform back to time domain
        filtered_signal = ifft(yf_filtered)
        return np.real(filtered_signal)

    @staticmethod
    def kalman_filter(signal: np.ndarray, process_noise: float = 1e-4, 
                      measurement_noise: float = 1e-2) -> np.ndarray:
        """
        Applies a 1D Kalman filter for signal reconstruction.
        
        Explicit implementation of Kalman updates:
        Prediction:
            x_hat_minus = x_hat
            P_minus = P + Q
        Update:
            K = P_minus / (P_minus + R)
            x_hat = x_hat_minus + K * (z - x_hat_minus)
            P = (1 - K) * P_minus
            
        Args:
            signal: Noisy input observations (z).
            process_noise (Q): Estimation of how much the signal changes between steps.
            measurement_noise (R): Estimation of the noise level in observations.
            
        Returns:
            np.ndarray: Reconstructed signal (estimates x_hat).
        """
        n = len(signal)
        reconstructed = np.zeros(n)
        
        # Initial guesses
        x_hat = signal[0]
        p = 1.0
        
        q = process_noise
        r = measurement_noise
        
        for i in range(n):
            # Prediction step (Time Update)
            # x_hat_minus = x_hat (Identity state transition)
            p_minus = p + q
            
            # Measurement Update step
            z = signal[i]
            k = p_minus / (p_minus + r)
            x_hat = x_hat + k * (z - x_hat)
            p = (1 - k) * p_minus
            
            reconstructed[i] = x_hat
            
        return reconstructed

if __name__ == "__main__":
    # Quick verification
    t = np.linspace(0, 10, 100)
    s = np.sin(t)
    noisy = s + np.random.normal(0, 0.5, 100)
    
    recon = SignalReconstructor()
    f_ma = recon.moving_average(noisy)
    f_ff = recon.fourier_filter(noisy, 0.1, 0.5)
    f_kf = recon.kalman_filter(noisy)
    
    print("Filters applied successfully.")
