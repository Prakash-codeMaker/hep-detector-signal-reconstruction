import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from src.signal_generator import SignalGenerator
from src.noise_model import NoiseModel
from src.reconstruction import SignalReconstructor
from src.metrics import PerformanceMetrics
from src.experiments import Experiments

def set_style():
    """Sets publication-quality plot style."""
    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 12,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'grid.alpha': 0.3,
        'figure.figsize': (8, 5)
    })

class SimulationRunner:
    """
    Main entry point for the HEP Detector Signal Reconstruction project.
    """
    
    def __init__(self, plots_dir: str = "plots", results_dir: str = "results"):
        self.plots_dir = plots_dir
        self.results_dir = results_dir
        os.makedirs(plots_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
        
        self.gen = SignalGenerator()
        self.noise = NoiseModel()
        self.recon = SignalReconstructor()
        self.metrics = PerformanceMetrics()
        self.exp = Experiments(results_dir=results_dir)
        
        set_style()

    def plot_single_example(self):
        """Generates and saves a visualization of basic signal, noise, and reconstruction."""
        print("Generating single event visualization...")
        t = self.gen.time
        clean = self.gen.generate_gaussian_pulse()
        
        # Add full noise model
        noisy = self.noise.apply_full_noise_model(clean, t)
        
        # Reconstruction
        recon_kf = self.recon.kalman_filter(noisy)
        recon_ff = self.recon.fourier_filter(noisy, self.gen.dt, cutoff_freq=0.5)
        
        plt.figure()
        plt.plot(t, noisy, label="Noisy Signal", alpha=0.5, color='gray')
        plt.plot(t, clean, label="Ideal Pulse", color='black', linewidth=2)
        plt.plot(t, recon_kf, label="Kalman Filter", color='red', linestyle='--')
        plt.plot(t, recon_ff, label="Fourier Filter", color='blue', linestyle='-.')
        
        plt.title("Detector Signal Reconstruction Comparison")
        plt.xlabel("Time [ns]")
        plt.ylabel("Amplitude [a.u.]")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, "signal_comparison.png"), dpi=300)
        plt.close()

    def plot_noise_sweep_results(self, sweep_data: dict):
        """Visualizes MSE and SNR vs Noise Level."""
        print("Plotting noise sweep results...")
        sigmas = sorted([float(s) for s in sweep_data.keys()])
        
        plt.figure(figsize=(12, 5))
        
        # Plot MSE
        plt.subplot(1, 2, 1)
        for method in ["MA", "Fourier", "Kalman", "Noisy"]:
            mse = [sweep_data[str(s)][method]["MSE"] for s in sigmas]
            plt.plot(sigmas, mse, marker='o', label=method)
        plt.yscale('log')
        plt.title("Reconstruction MSE vs. Noise Level")
        plt.xlabel(r"Noise $\sigma_n$")
        plt.ylabel("Mean Squared Error")
        plt.legend()
        plt.grid(True)
        
        # Plot SNR
        plt.subplot(1, 2, 2)
        for method in ["MA", "Fourier", "Kalman", "Noisy"]:
            snr = [sweep_data[str(s)][method]["SNR"] for s in sigmas]
            plt.plot(sigmas, snr, marker='s', label=method)
        plt.title("SNR Recovery vs. Noise Level")
        plt.xlabel(r"Noise $\sigma_n$")
        plt.ylabel("SNR [dB]")
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, "noise_sweep_metrics.png"), dpi=300)
        plt.close()

    def plot_scaling_convergence(self, scaling_data: dict):
        """Visualizes statistical convergence of bias."""
        print("Plotting scaling convergence...")
        counts = sorted([int(c) for c in scaling_data.keys()])
        
        plt.figure()
        kf_bias = [scaling_data[str(c)]["KF_bias_mean"] for c in counts]
        kf_err = [scaling_data[str(c)]["KF_bias_std"] for c in counts]
        
        plt.errorbar(counts, kf_bias, yerr=kf_err, fmt='o-', label="Kalman Filter Bias", capsize=5)
        plt.xscale('log')
        plt.axhline(0, color='black', alpha=0.3, linestyle='--')
        plt.title("Statistical Convergence of Reconstruction Bias")
        plt.xlabel("Event Count")
        plt.ylabel("Mean Reconstruction Bias")
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, "scaling_convergence.png"), dpi=300)
        plt.close()
        
        # Bias Histogram for largest count
        last_count = str(counts[-1])
        plt.figure()
        biases = scaling_data[last_count]["KF_biases"]
        plt.hist(biases, bins=30, alpha=0.7, color='green', edgecolor='black')
        plt.axvline(np.mean(biases), color='red', linestyle='--', label=f"Mean: {np.mean(biases):.4f}")
        plt.title(f"Reconstruction Bias Distribution (N={last_count})")
        plt.xlabel("Bias [a.u.]")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.plots_dir, "bias_histogram.png"), dpi=300)
        plt.close()

    def run(self):
        """Executes the full simulation pipeline."""
        print("Starting HEP Detector Signal Reconstruction Pipeline...")
        
        # 1. Basic visualization
        self.plot_single_example()
        
        # 2. Run Noise Sweep Experiment
        print("Running Noise Sweep Study...")
        noise_levels = [0.05, 0.1, 0.2, 0.5]
        sweep_results = self.exp.run_noise_sweep(noise_levels)
        self.plot_noise_sweep_results(sweep_results)
        
        # 3. Run Event Scaling Study
        print("Running Event Scaling Study...")
        counts = [100, 1000, 10000]
        scaling_results = self.exp.run_event_scaling_study(counts)
        self.plot_scaling_convergence(scaling_results)
        
        print(f"Pipeline complete. All results saved to {self.results_dir} and plots to {self.plots_dir}.")

if __name__ == "__main__":
    runner = SimulationRunner()
    runner.run()
