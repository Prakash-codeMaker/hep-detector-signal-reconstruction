import numpy as np
from typing import Optional

class NoiseModel:
    """
    Simulates realistic noise in HEP detectors: Gaussian noise, baseline drift, and spikes.
    """
    
    def __init__(self, seed: int = 42):
        """
        Args:
            seed: Random seed for reproducibility.
        """
        self.seed = seed
        np.random.seed(self.seed)

    def add_gaussian_noise(self, signal: np.ndarray, sigma: float = 0.1) -> np.ndarray:
        """
        Adds additive white Gaussian noise (AWGN) to the signal.
        
        Args:
            signal: The clean input signal.
            sigma: Standard deviation of the Gaussian noise.
            
        Returns:
            np.ndarray: Noisy signal.
        """
        noise = np.random.normal(0, sigma, size=signal.shape)
        return signal + noise

    def add_baseline_drift(self, signal: np.ndarray, time: np.ndarray, 
                           amplitude: float = 0.2, frequency: float = 0.05) -> np.ndarray:
        """
        Adds a low-frequency sinusoidal baseline drift to the signal.
        
        Args:
            signal: The input signal.
            time: Time array corresponding to the signal.
            amplitude: Amplitude of the drift.
            frequency: Frequency of the sinusoidal drift.
            
        Returns:
            np.ndarray: Signal with drift.
        """
        drift = amplitude * np.sin(2 * np.pi * frequency * time)
        return signal + drift

    def add_spikes(self, signal: np.ndarray, prob: float = 0.01, amplitude: float = 2.0) -> np.ndarray:
        """
        Adds random spike outliers to the signal.
        
        Args:
            signal: The input signal.
            prob: Probability of a spike at any given time step.
            amplitude: Magnitude of the spikes.
            
        Returns:
            np.ndarray: Signal with spikes.
        """
        spikes = (np.random.random(size=signal.shape) < prob).astype(float)
        # Randomly choose positive or negative spikes
        spikes *= np.random.choice([-1, 1], size=signal.shape) * amplitude
        return signal + spikes

    def apply_full_noise_model(self, signal: np.ndarray, time: np.ndarray,
                               gaussian_sigma: float = 0.1,
                               drift_amplitude: float = 0.1, drift_frequency: float = 0.05,
                               spike_prob: float = 0.005, spike_amplitude: float = 1.5) -> np.ndarray:
        """
        Applies all noise components to the signal.
        """
        s = self.add_gaussian_noise(signal, sigma=gaussian_sigma)
        s = self.add_baseline_drift(s, time, amplitude=drift_amplitude, frequency=drift_frequency)
        s = self.add_spikes(s, prob=spike_prob, amplitude=spike_amplitude)
        return s

if __name__ == "__main__":
    # Quick verification
    nm = NoiseModel()
    t = np.linspace(0, 100, 1000)
    s = np.zeros_like(t)
    noisy = nm.apply_full_noise_model(s, t)
    print(f"Generated noisy signal with mean {np.mean(noisy):.4f} and std {np.std(noisy):.4f}")
