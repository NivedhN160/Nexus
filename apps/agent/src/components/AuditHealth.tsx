import React, { useState, useEffect } from 'react';
import { ShieldAlert, Database, Server, Brain, Activity, RefreshCw } from 'lucide-react';

interface LogEntry {
  time: string;
  level: string;
  message: string;
}

export default function AuditHealth() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/audit/logs`, {
        headers: {
          'X-API-Key': import.meta.env.VITE_API_KEY || 'nexus_dev_key'
        }
      });
      if (res.ok) {
        const data = await res.json();
        setLogs(data);
      }
    } catch (e) {
      console.error('Failed to fetch logs', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert className="text-teal" size={20} /> Audit & Health
          </h2>
          <p className="text-muted" style={{ fontSize: '14px', marginTop: '4px' }}>System vitals and security logs</p>
        </div>
        <button className="btn" style={{ fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }} onClick={fetchLogs}>
          <RefreshCw size={14} className={loading ? 'spinning' : ''} /> Refresh Logs
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(0, 240, 255, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Database className="text-teal" size={24} />
          </div>
          <div>
            <div className="text-muted" style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>PostgreSQL</div>
            <div style={{ fontSize: '16px', fontWeight: 500, color: 'var(--text-primary)', marginTop: '4px' }}>Connected</div>
            <div className="mono text-teal" style={{ fontSize: '11px', marginTop: '4px' }}>Latency: &lt;10ms</div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(0, 240, 255, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Server className="text-teal" size={24} />
          </div>
          <div>
            <div className="text-muted" style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>Redis Cache</div>
            <div style={{ fontSize: '16px', fontWeight: 500, color: 'var(--text-primary)', marginTop: '4px' }}>Connected</div>
            <div className="mono text-teal" style={{ fontSize: '11px', marginTop: '4px' }}>Latency: 1ms</div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(0, 240, 255, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Brain className="text-teal" size={24} />
          </div>
          <div>
            <div className="text-muted" style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px' }}>Background Worker</div>
            <div style={{ fontSize: '16px', fontWeight: 500, color: 'var(--text-primary)', marginTop: '4px' }}>Running</div>
            <div className="mono text-teal" style={{ fontSize: '11px', marginTop: '4px' }}>Active Jobs: 0</div>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={16} className="text-teal" />
          <h3 style={{ fontSize: '14px', fontWeight: 500 }}>System Event Log</h3>
        </div>
        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto' }}>
          {loading && logs.length === 0 && (
            <div style={{ color: 'var(--text-secondary)' }}>Fetching logs...</div>
          )}
          {!loading && logs.length === 0 && (
            <div style={{ color: 'var(--text-secondary)' }}>No recent logs.</div>
          )}
          {logs.map((log, idx) => (
            <div key={idx} style={{ 
              display: 'flex', 
              gap: '16px', 
              padding: '12px', 
              borderBottom: '1px solid rgba(255,255,255,0.02)',
              fontSize: '13px'
            }}>
              <div className="mono" style={{ width: '80px', color: 'var(--text-secondary)' }}>
                {log.time}
              </div>
              <div style={{ 
                width: '60px', 
                color: log.level === 'ERROR' ? '#ef4444' : log.level === 'WARN' ? 'var(--warning-amber)' : 'var(--accent-teal)',
                fontWeight: 600
              }}>
                {log.level}
              </div>
              <div className="mono" style={{ flex: 1, color: 'var(--text-primary)' }}>
                {log.message}
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
