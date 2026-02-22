import numpy as np
import json
import os
from .signal_generator import SignalGenerator
from .noise_model import NoiseModel
from .reconstruction import SignalReconstructor
from .metrics import PerformanceMetrics
from typing import List, Dict

class Experiments:
    """
    Orchestrates controlled studies to evaluate detector signal reconstruction.
    """
    
    def __init__(self, results_dir: str = "results"):
        self.gen = SignalGenerator()
        self.noise = NoiseModel()
        self.recon = SignalReconstructor()
        self.metrics = PerformanceMetrics()
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)

    def run_noise_sweep(self, sigma_levels: List[float]) -> Dict[str, Dict]:
        """
        Evaluates reconstruction performance across different Gaussian noise levels.
        """
        results = {}
        # Generate a standard pulse
        clean_signal = self.gen.generate_gaussian_pulse()
        dt = self.gen.dt
        
        for sigma in sigma_levels:
            # Add noise (Gaussian only for the sweep as per requirements)
            noisy_signal = self.noise.add_gaussian_noise(clean_signal, sigma=sigma)
            
            # Reconstruction
            f_ma = self.recon.moving_average(noisy_signal)
            f_ff = self.recon.fourier_filter(noisy_signal, dt, cutoff_freq=0.5)
            f_kf = self.recon.kalman_filter(noisy_signal)
            
            # Compute metrics
            results[str(sigma)] = {
                "MA": self.metrics.compute_all(clean_signal, f_ma),
                "Fourier": self.metrics.compute_all(clean_signal, f_ff),
                "Kalman": self.metrics.compute_all(clean_signal, f_kf),
                "Noisy": self.metrics.compute_all(clean_signal, noisy_signal)
            }
            
        with open(os.path.join(self.results_dir, "noise_sweep.json"), "w") as f:
            json.dump(results, f, indent=4)
            
        return results

    def run_event_scaling_study(self, event_counts: List[int]) -> Dict[str, Dict]:
        """
        Analyzes statistical convergence of reconstruction bias over multiple events.
        """
        results = {}
        dt = self.gen.dt
        
        for count in event_counts:
            # Generate batch
            clean_events = self.gen.generate_event_batch(count)
            
            bias_ma = []
            bias_kf = []
            
            for i in range(count):
                clean = clean_events[i]
                noisy = self.noise.add_gaussian_noise(clean, sigma=0.2)
                
                # Reconstruction
                f_ma = self.recon.moving_average(noisy)
                f_kf = self.recon.kalman_filter(noisy)
                
                # Metrics
                bias_ma.append(self.metrics.reconstruction_bias(clean, f_ma))
                bias_kf.append(self.metrics.reconstruction_bias(clean, f_kf))
            
            results[str(count)] = {
                "MA_bias_mean": float(np.mean(bias_ma)),
                "MA_bias_std": float(np.std(bias_ma)),
                "KF_bias_mean": float(np.mean(bias_kf)),
                "KF_bias_std": float(np.std(bias_kf)),
                "MA_biases": bias_ma[:100], # Store subset for histograms
                "KF_biases": bias_kf[:100]
            }
            
        with open(os.path.join(self.results_dir, "event_scaling.json"), "w") as f:
            json.dump(results, f, indent=4)
            
        return results
