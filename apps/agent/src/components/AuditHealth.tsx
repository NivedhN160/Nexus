import React from 'react';
import { ShieldAlert, Database, Server, Brain, Activity, RefreshCw } from 'lucide-react';

export default function AuditHealth() {
  const logs = [
    { time: '10:42:01', level: 'INFO', message: 'Nexus Worker authenticated successfully.' },
    { time: '10:41:15', level: 'WARN', message: 'Rate limit approaching for Groq LLM (82%).' },
    { time: '10:35:09', level: 'INFO', message: 'Idempotency sweep complete. 4 stale keys removed.' },
    { time: '10:20:00', level: 'ERROR', message: 'Webhook signature verification failed from IP 192.168.1.1' },
    { time: '10:15:33', level: 'INFO', message: 'System startup sequence initiated.' },
  ];

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert className="text-teal" size={20} /> Audit & Health
          </h2>
          <p className="text-muted" style={{ fontSize: '14px', marginTop: '4px' }}>System vitals and security logs</p>
        </div>
        <button className="btn" style={{ fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <RefreshCw size={14} /> Refresh Logs
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
            <div className="mono text-teal" style={{ fontSize: '11px', marginTop: '4px' }}>Latency: 4ms</div>
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
            <div className="mono text-teal" style={{ fontSize: '11px', marginTop: '4px' }}>Active Jobs: 2</div>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={16} className="text-teal" />
          <h3 style={{ fontSize: '14px', fontWeight: 500 }}>System Event Log</h3>
        </div>
        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto' }}>
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
