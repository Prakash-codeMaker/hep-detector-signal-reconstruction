# HEP Detector Signal Reconstruction: Simulation and Statistical Analysis

## Overview
This project presents a production-quality computational simulation for reconstructing noisy detector signals in high-energy physics (HEP). The focus is on statistical modeling, signal reconstruction algorithms, and quantitative validation, reflecting workflows used in experimental detector systems.

## Mathematical Formulation

### Signal Model
The ideal detector response is modeled as a Gaussian pulse:
$$S(t) = A \cdot \exp\left(-\frac{(t - t_0)^2}{2\sigma^2}\right)$$
where $A$ is peak amplitude, $t_0$ arrival time, and $\sigma$ pulse width.

### Noise Model
The observed signal $S_{noisy}(t)$ is a composite of:
1. **Gaussian Noise**: $\mathcal{N}(0, \sigma_n)$ (Electronics noise)
2. **Baseline Drift**: $D(t) = A_d \sin(2\pi f_d t)$ (Thermal/environmental effects)
3. **Random Spikes**: Sparse electronic disturbances.

### Reconstruction Algorithms
- **Moving Average (MA)**: Simple temporal smoothing.
- **Fourier Low-Pass Filter**: Frequency-domain suppression of high-frequency noise.
- **Kalman Filter**: Explicit recursive state-space estimator (Prediction & Update cycles).

## Experimental Design

### Quantitative Metrics
- **MSE**: Mean Squared Error of the reconstruction.
- **SNR**: Signal-to-Noise Ratio recovery in dB.
- **Peak Error**: Error in reconstructed pulse amplitude.
- **Bias**: Systematic reconstruction offset.

### Statistical Studies
- **Noise Sweep**: Evaluates robustness across $\sigma_n \in [0.05, 0.5]$.
- **Statistical Scaling**: Analyzes bias convergence across $10^2$ to $10^4$ events.

## Results and Interpretation
Results are generated programmatically:
- `signal_comparison.png`: Qualitative tracking behavior.
- `noise_sweep_metrics.png`: Quantitative performance trends.
- `scaling_convergence.png`: Statistical stability analysis.

All scientific conclusions are derived from the core simulation pipeline results stored in `/results`.

## Diagnostic Visualization Layer (Optional)
A lightweight visualization layer is provided for qualitative sanity checks and interactive parameter exploration. This component is non-essential and does not affect the quantitative analysis. It allows for:
- Real-time observation of noise-level impacts.
- Qualitative inspection of filter stability under varying $Q$ and $R$ parameters in the Kalman model.

## Usage
### Core Simulation
1. Install dependencies: `pip install -r requirements.txt`
2. Run full pipeline: `python simulation_runner.py`

### Diagnostic Visualization (Optional)
*Instructions for running the diagnostic layer will be added here upon implementation.*

## Future Work
- Real-time FPGA mapping of Kalman equations.
- ML-based denoising using Autoencoders.
- Multi-channel detector noise correlations.
