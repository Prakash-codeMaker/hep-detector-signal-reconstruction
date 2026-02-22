import numpy as np
from typing import Optional, Tuple

class SignalGenerator:
    """
    Simulates high-energy physics detector signals using a Gaussian pulse model.
    """
    
    def __init__(self, t_start: float = 0.0, t_end: float = 100.0, dt: float = 0.1, seed: int = 42):
        """
        Initializes the signal generator with time parameters.
        
        Args:
            t_start: Start time of the simulation.
            t_end: End time of the simulation.
            dt: Time step size.
            seed: Random seed for reproducibility.
        """
        self.t_start = t_start
        self.t_end = t_end
        self.dt = dt
        self.time = np.arange(t_start, t_end, dt)
        self.seed = seed
        np.random.seed(self.seed)

    def generate_gaussian_pulse(self, amplitude: float = 1.0, t0: float = 50.0, sigma: float = 5.0) -> np.ndarray:
        """
        Generates a single Gaussian pulse signal.
        
        S(t) = A * exp(-(t - t0)^2 / (2 * sigma^2))
        
        Args:
            amplitude: Peak height (A).
            t0: Peak position in time.
            sigma: Pulse width.
            
        Returns:
            np.ndarray: The generated pulse signal.
        """
        return amplitude * np.exp(-(self.time - t0)**2 / (2 * sigma**2))

    def generate_event_batch(self, n_events: int, amplitude_range: Tuple[float, float] = (0.8, 1.2),
                             t0_range: Tuple[float, float] = (40.0, 60.0),
                             sigma_range: Tuple[float, float] = (3.0, 7.0)) -> np.ndarray:
        """
        Generates a batch of detector events.
        
        Args:
            n_events: Number of pulses to generate.
            amplitude_range: Range for random amplitude selection.
            t0_range: Range for random peak position selection.
            sigma_range: Range for random pulse width selection.
            
        Returns:
            np.ndarray: A 2D array where each row is a pulse event.
        """
        events = np.zeros((n_events, len(self.time)))
        for i in range(n_events):
            a = np.random.uniform(*amplitude_range)
            t = np.random.uniform(*t0_range)
            s = np.random.uniform(*sigma_range)
            events[i] = self.generate_gaussian_pulse(amplitude=a, t0=t, sigma=s)
        return events

if __name__ == "__main__":
    # Quick verification
    gen = SignalGenerator()
    pulse = gen.generate_gaussian_pulse()
    print(f"Generated pulse with {len(pulse)} samples.")
    batch = gen.generate_event_batch(10)
    print(f"Generated batch with shape {batch.shape}.")
