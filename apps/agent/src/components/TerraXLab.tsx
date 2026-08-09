import React, { useState } from 'react';
import { Globe, Wind, Droplets, Activity, ChevronLeft, Play } from 'lucide-react';

export default function TerraXLab({ onBack }: { onBack: () => void }) {
  const [location, setLocation] = useState('New York, USA');
  const [carbon, setCarbon] = useState(0);
  const [population, setPopulation] = useState(0);
  const [economy, setEconomy] = useState(0);
  const [resources, setResources] = useState(0);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/labs/terra-x/simulate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test_key_123'
        },
        body: JSON.stringify({
          location,
          carbon_change: carbon,
          pop_growth: population,
          econ_shift: economy,
          resource_use: resources
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
      <button onClick={onBack} className="btn-secondary" style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <ChevronLeft size={16} /> Back to Labs
      </button>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
        <Globe size={32} className="text-teal" />
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: 600 }}>Terra-X Climate Lab</h2>
          <p className="text-muted" style={{ fontSize: '14px' }}>Native Nexus Simulation Engine</p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', marginBottom: '16px', color: 'var(--text-secondary)' }}>Simulation Parameters</h3>
          
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px' }}>Target Location</label>
            <input 
              type="text" 
              value={location} 
              onChange={(e) => setLocation(e.target.value)}
              className="chat-input"
              style={{ padding: '12px', width: '100%' }}
            />
          </div>

          {[
            { label: 'Carbon Emissions Change (%)', value: carbon, setter: setCarbon },
            { label: 'Population Growth (%)', value: population, setter: setPopulation },
            { label: 'Economic Shift (%)', value: economy, setter: setEconomy },
            { label: 'Resource Utilization (%)', value: resources, setter: setResources }
          ].map(slider => (
            <div key={slider.label} style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '14px' }}>{slider.label}</span>
                <span className="mono text-teal">{slider.value}%</span>
              </div>
              <input 
                type="range" 
                min="-100" 
                max="100" 
                value={slider.value}
                onChange={(e) => slider.setter(parseInt(e.target.value))}
                style={{ width: '100%' }}
              />
            </div>
          ))}

          <button 
            onClick={handleSimulate}
            disabled={loading}
            className="btn-primary" 
            style={{ width: '100%', marginTop: '16px', display: 'flex', justifyContent: 'center', gap: '8px' }}
          >
            {loading ? <Activity size={18} className="spin" /> : <Play size={18} />}
            {loading ? 'Running Simulation...' : 'Run Simulation'}
          </button>
        </div>

        {result && (
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h3 style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '12px' }}>Current Baseline Weather (Mock)</h3>
              <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: '32px', fontWeight: 'bold' }}>{result.baseline.temp}°C</div>
                  <div className="text-muted" style={{ textTransform: 'capitalize' }}>{result.baseline.desc}</div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Droplets size={14} className="text-teal"/> Humidity: {result.baseline.humidity}%</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Wind size={14} className="text-teal"/> Wind: Normal</div>
                </div>
              </div>
            </div>
            
            <div style={{ height: '1px', background: 'rgba(255,255,255,0.1)' }}></div>

            <div>
              <h3 style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '12px' }}>AI Simulation Output</h3>
              <p style={{ lineHeight: '1.6', fontSize: '15px' }}>{result.analysis}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
