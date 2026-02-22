from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .signal_generator import SignalGenerator
from .noise_model import NoiseModel
from .reconstruction import SignalReconstructor
import numpy as np

app = FastAPI(title="HEP Detector Signal Diagnostic API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/simulate")
async def simulate(
    amplitude: float = 1.0,
    t0: float = 50.0,
    sigma: float = 5.0,
    noise_sigma: float = 0.1,
    drift_amp: float = 0.1,
    cutoff: float = 0.5
):
    """
    Runs a single event simulation and returns signal data for visualization.
    """
    gen = SignalGenerator()
    noise = NoiseModel()
    recon = SignalReconstructor()
    
    t = gen.time
    clean = gen.generate_gaussian_pulse(amplitude=amplitude, t0=t0, sigma=sigma)
    noisy = noise.apply_full_noise_model(
        clean, t, 
        gaussian_sigma=noise_sigma, 
        drift_amplitude=drift_amp, 
        spike_prob=0.005
    )
    
    # Apply filters
    recon_kf = recon.kalman_filter(noisy)
    recon_ff = recon.fourier_filter(noisy, gen.dt, cutoff_freq=cutoff)
    
    return {
        "time": t.tolist(),
        "clean": clean.tolist(),
        "noisy": noisy.tolist(),
        "kalman": recon_kf.tolist(),
        "fourier": recon_ff.tolist(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
