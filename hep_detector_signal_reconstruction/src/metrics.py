import numpy as np

class PerformanceMetrics:
    """
    Computes quantitative metrics for evaluating signal reconstruction quality.
    """
    
    @staticmethod
    def mean_squared_error(true_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Computes the Mean Squared Error (MSE).
        """
        return np.mean((true_signal - reconstructed_signal)**2)

    @staticmethod
    def signal_to_noise_ratio(true_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Computes the Signal-to-Noise Ratio (SNR) in decibels (dB).
        SNR_dB = 10 * log10(P_signal / P_noise)
        where P_noise is the power of the residual error.
        """
        signal_power = np.mean(true_signal**2)
        noise_power = np.mean((true_signal - reconstructed_signal)**2)
        
        if noise_power == 0:
            return float('inf')
            
        return 10 * np.log10(signal_power / noise_power)

    @staticmethod
    def peak_amplitude_error(true_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Computes the absolute error in the peak amplitude.
        """
        true_peak = np.max(true_signal)
        recon_peak = np.max(reconstructed_signal)
        return np.abs(true_peak - recon_peak)

    @staticmethod
    def reconstruction_bias(true_signal: np.ndarray, reconstructed_signal: np.ndarray) -> float:
        """
        Computes the mean bias (systematic offset) of the reconstruction.
        """
        return np.mean(reconstructed_signal - true_signal)

    @classmethod
    def compute_all(cls, true_signal: np.ndarray, reconstructed_signal: np.ndarray) -> dict:
        """
        Returns a dictionary containing all implemented metrics.
        """
        return {
            "MSE": cls.mean_squared_error(true_signal, reconstructed_signal),
            "SNR": cls.signal_to_noise_ratio(true_signal, reconstructed_signal),
            "Peak Error": cls.peak_amplitude_error(true_signal, reconstructed_signal),
            "Bias": cls.reconstruction_bias(true_signal, reconstructed_signal)
        }

if __name__ == "__main__":
    # Quick verification
    s_true = np.array([1.0, 2.0, 3.0, 2.0, 1.0])
    s_recon = np.array([1.1, 1.9, 2.8, 2.1, 1.2])
    print(PerformanceMetrics.compute_all(s_true, s_recon))
