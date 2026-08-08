import React, { useState } from 'react';
import { 
  Terminal, Activity, ShieldAlert, Cpu, 
  Send, Maximize2, Share2, Layers, Play
} from 'lucide-react';
import SocialGraph from './components/SocialGraph';
import LeadStream from './components/LeadStream';
import AuditHealth from './components/AuditHealth';
import AgentChat from './components/AgentChat';

export default function App() {
  const [activeTab, setActiveTab] = useState('agent');

  return (
    <div className="nexus-layout">
      {/* Top Bar */}
      <header className="top-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: 'var(--accent-teal)', boxShadow: '0 0 8px var(--accent-teal)' }}></div>
          <h1 style={{ fontSize: '18px', fontWeight: 600, letterSpacing: '2px' }}>NEXUS</h1>
        </div>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <span className="mono text-muted" style={{ fontSize: '12px' }}>SYS.REQ.001</span>
          <Activity size={18} className="text-teal" />
        </div>
      </header>

      {/* Left Navigation */}
      <nav className="left-nav">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {[
            { id: 'agent', icon: Terminal, label: 'Agent Console' },
            { id: 'content', icon: Layers, label: 'Content Pipeline' },
            { id: 'social', icon: Share2, label: 'Social Graph' },
            { id: 'leads', icon: Layers, label: 'Lead Stream' },
            { id: 'match', icon: Activity, label: 'Matchmaking' },
            { id: 'audit', icon: ShieldAlert, label: 'Dev Audit' },
            { id: 'labs', icon: Cpu, label: 'Labs (Terra-X)' }
          ].map(item => (
            <div 
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                borderRadius: '8px',
                cursor: 'pointer',
                background: activeTab === item.id ? 'var(--accent-teal-dim)' : 'transparent',
                color: activeTab === item.id ? 'var(--accent-teal)' : 'var(--text-secondary)',
                border: activeTab === item.id ? '1px solid var(--accent-teal)' : '1px solid transparent'
              }}
            >
              <item.icon size={18} />
              <span style={{ fontSize: '14px', fontWeight: 500 }}>{item.label}</span>
            </div>
          ))}
        </div>
      </nav>

      {/* Main Stage */}
      <main className="main-stage">
        {activeTab === 'agent' && (
          <AgentChat />
        )}
        
        {activeTab !== 'agent' && activeTab !== 'social' && activeTab !== 'leads' && activeTab !== 'audit' && (
          <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div className="glass-panel" style={{ padding: '48px', textAlign: 'center' }}>
              <Cpu size={48} className="text-teal" style={{ marginBottom: '16px', opacity: 0.5 }} />
              <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>{activeTab.toUpperCase()} Module</h2>
              <p className="text-muted">Module loaded and standing by.</p>
            </div>
          </div>
        )}

        {activeTab === 'social' && <SocialGraph />}
        {activeTab === 'leads' && <LeadStream />}
        {activeTab === 'audit' && <AuditHealth />}
      </main>

      {/* Right Context */}
      <aside className="right-context">
        <h3 style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
          System Telemetry
        </h3>
        
        <div className="glass-panel" style={{ padding: '16px', marginBottom: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span className="text-muted" style={{ fontSize: '12px' }}>CPU Load</span>
            <span className="text-teal mono" style={{ fontSize: '12px' }}>14%</span>
          </div>
          <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
            <div style={{ height: '100%', width: '14%', background: 'var(--accent-teal)', borderRadius: '2px' }}></div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '16px', marginBottom: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span className="text-muted" style={{ fontSize: '12px' }}>Memory</span>
            <span className="text-amber mono" style={{ fontSize: '12px' }}>82%</span>
          </div>
          <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
            <div style={{ height: '100%', width: '82%', background: 'var(--warning-amber)', borderRadius: '2px' }}></div>
          </div>
        </div>
        
        <h3 style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--text-secondary)', marginBottom: '16px', marginTop: '32px' }}>
          Active Tools
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {['Web_Scraper_v2', 'Social_Queue_Mgr', 'Data_Guard_Alpha'].map(t => (
            <div key={t} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Play size={12} className="text-teal" />
              <span className="mono" style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{t}</span>
            </div>
          ))}
        </div>
      </aside>

      {/* Bottom Ops Strip */}
      <footer className="bottom-strip">
        <div style={{ display: 'flex', gap: '24px' }}>
          <span><span className="text-muted">NET:</span> <span className="text-teal">SECURE</span></span>
          <span><span className="text-muted">LATENCY:</span> 24ms</span>
          <span><span className="text-muted">V:</span> 1.0.0-rc</span>
        </div>
        <div>
          <Maximize2 size={14} className="text-muted" style={{ cursor: 'pointer' }} />
        </div>
      </footer>
    </div>
  );
}
