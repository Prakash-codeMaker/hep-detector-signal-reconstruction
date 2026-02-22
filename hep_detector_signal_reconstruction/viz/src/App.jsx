import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Settings, Play, Activity } from 'lucide-react';

const App = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [params, setParams] = useState({
    amplitude: 1.0,
    t0: 50.0,
    sigma: 5.0,
    noise_sigma: 0.1,
    drift_amp: 0.1,
    cutoff: 0.5
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const queryString = new URLSearchParams(params).toString();
      const response = await fetch(`http://localhost:8000/simulate?${queryString}`);
      const result = await response.json();

      // Transform data for Recharts
      const chartData = result.time.map((t, i) => ({
        time: t.toFixed(1),
        Ideal: result.clean[i],
        Noisy: result.noisy[i],
        Kalman: result.kalman[i],
        Fourier: result.fourier[i]
      }));
      setData(chartData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleParamChange = (e) => {
    const { name, value } = e.target;
    setParams(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <header className="mb-8 flex items-center justify-between border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-3xl font-bold text-blue-400">HEP Signal Diagnostic Layer</h1>
          <p className="text-slate-400">Qualitative Reconstruction Inspection Tool</p>
        </div>
        <div className="flex items-center gap-4 text-sm bg-slate-800 px-4 py-2 rounded-lg border border-slate-700">
          <Activity size={18} className="text-green-400" />
          <span>Scientific Simulation Engine: Active</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Controls Sidebar */}
        <div className="lg:col-span-1 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
          <div className="flex items-center gap-2 mb-6 font-semibold text-lg border-b border-slate-700 pb-2">
            <Settings size={20} />
            <h2>Control Panel</h2>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Pulse Amplitude (A)</label>
              <input
                type="range" name="amplitude" min="0.1" max="2.0" step="0.1"
                value={params.amplitude} onChange={handleParamChange}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
              <div className="text-right text-xs mt-1 text-slate-400">{params.amplitude}</div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Noise Level (σₙ)</label>
              <input
                type="range" name="noise_sigma" min="0.01" max="1.0" step="0.05"
                value={params.noise_sigma} onChange={handleParamChange}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-red-500"
              />
              <div className="text-right text-xs mt-1 text-slate-400">{params.noise_sigma}</div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Baseline Drift Amp</label>
              <input
                type="range" name="drift_amp" min="0" max="0.5" step="0.05"
                value={params.drift_amp} onChange={handleParamChange}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-yellow-500"
              />
              <div className="text-right text-xs mt-1 text-slate-400">{params.drift_amp}</div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Fourier Cutoff Freq</label>
              <input
                type="range" name="cutoff" min="0.1" max="2.0" step="0.1"
                value={params.cutoff} onChange={handleParamChange}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <div className="text-right text-xs mt-1 text-slate-400">{params.cutoff} Hz</div>
            </div>

            <button
              onClick={fetchData}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg font-bold flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              <Play size={18} fill="currentColor" />
              {loading ? "Simulating..." : "Execute Simulation"}
            </button>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-700">
            <p className="text-xs text-slate-500 leading-relaxed italic">
              *Note: This layer is for qualitative diagnostic exploration. Quantitative results are generated via the core simulation pipeline.
            </p>
          </div>
        </div>

        {/* Main Chart Area */}
        <div className="lg:col-span-3 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl min-h-[500px]">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold">Signal Reconstruction Response</h2>
            <div className="flex gap-4 text-xs">
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-slate-400"></div> Noisy</span>
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-white"></div> Ideal</span>
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-red-500"></div> Kalman</span>
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-blue-500"></div> Fourier</span>
            </div>
          </div>

          <div className="w-full h-[450px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" hide />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', color: '#f1f5f9' }}
                  itemStyle={{ fontSize: '12px' }}
                />
                <Legend />
                <Line type="monotone" dataKey="Noisy" stroke="#64748b" strokeWidth={1} dot={false} alpha={0.5} />
                <Line type="monotone" dataKey="Ideal" stroke="#ffffff" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Kalman" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                <Line type="monotone" dataKey="Fourier" stroke="#3b82f6" strokeWidth={2} dot={false} strokeDasharray="3 4" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
