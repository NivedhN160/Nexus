import React, { useState } from 'react';
import { TrendingUp, Activity, ChevronLeft, Search, BarChart3, ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function StockLab({ onBack }: { onBack: () => void }) {
  const [ticker, setTicker] = useState('NVDA');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!ticker) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/labs/stock/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test_key_123'
        },
        body: JSON.stringify({ ticker: ticker.toUpperCase() })
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
        <TrendingUp size={32} className="text-teal" />
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: 600 }}>Stock Analyser</h2>
          <p className="text-muted" style={{ fontSize: '14px' }}>Native Nexus Market Intelligence</p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', marginBottom: '16px', color: 'var(--text-secondary)' }}>Market Query</h3>
          
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px' }}>Ticker Symbol</label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input 
                type="text" 
                value={ticker} 
                onChange={(e) => setTicker(e.target.value)}
                placeholder="e.g. AAPL"
                className="chat-input mono"
                style={{ padding: '12px', flex: 1, textTransform: 'uppercase' }}
              />
              <button 
                onClick={handleAnalyze}
                disabled={loading || !ticker}
                className="btn-primary" 
                style={{ padding: '0 24px', display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                {loading ? <Activity size={18} className="spin" /> : <Search size={18} />}
                {loading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
          </div>
          
          <div style={{ padding: '16px', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <BarChart3 size={20} className="text-muted" />
              <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Analysis powered by local Nexus LLM and mock market data arrays to avoid API costs.</span>
            </div>
          </div>
        </div>

        {result && (
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <h3 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '4px', letterSpacing: '1px' }}>{ticker.toUpperCase()}</h3>
                  <div className="text-muted" style={{ fontSize: '14px' }}>Mock Market Data</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '28px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    ${result.market_data.price}
                  </div>
                  <div style={{ 
                    color: result.market_data.change >= 0 ? 'var(--accent-teal)' : 'var(--warning-amber)',
                    display: 'flex', alignItems: 'center', gap: '4px', justifyContent: 'flex-end',
                    fontSize: '14px', fontWeight: 500
                  }}>
                    {result.market_data.change >= 0 ? <ArrowUpRight size={16}/> : <ArrowDownRight size={16}/>}
                    {Math.abs(result.market_data.change)}%
                  </div>
                </div>
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
                <span className="text-muted" style={{ fontSize: '13px' }}>24h Volume</span>
                <span className="mono" style={{ fontSize: '13px' }}>{result.market_data.volume.toLocaleString()}</span>
              </div>
            </div>
            
            <div style={{ height: '1px', background: 'rgba(255,255,255,0.1)' }}></div>

            <div>
              <h3 style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '12px' }}>AI Technical Brief</h3>
              <p style={{ lineHeight: '1.6', fontSize: '15px' }}>{result.analysis}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
