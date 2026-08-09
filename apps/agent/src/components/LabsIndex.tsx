import React, { useState, useEffect } from 'react';
import { ExternalLink, Database, Cpu, Globe, UserCheck } from 'lucide-react';

export default function LabsIndex({ onOpenLab }: { onOpenLab?: (id: string) => void }) {
  const myLabs = [
    { id: 'terra-x', title: 'Terra-X', desc: 'Global climate modeling & offline weather', status: 'Active', icon: Globe },
    { id: 'stock', title: 'Stock Analyser', desc: 'Realtime stock simulator & charting', status: 'Active', icon: Cpu }
  ];

  const [isPresent, setIsPresent] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/labs/presence')
      .then(res => res.json())
      .then(data => setIsPresent(data.is_present))
      .catch(console.error);
  }, []);

  const togglePresence = async () => {
    const newVal = !isPresent;
    setIsPresent(newVal);
    await fetch('http://localhost:8000/labs/presence', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_present: newVal })
    });
  };

  const resources = [
    { title: 'Free APIs for Devs', link: 'https://github.com/public-apis/public-apis', icon: Globe, desc: 'A collective list of free APIs' },
    { title: 'Open Source Alternative To', link: 'https://github.com/RunaCapital/awesome-oss-alternatives', icon: Database, desc: 'OSS alternatives to SaaS' },
    { title: 'Free Tier Services', link: 'https://free-for.dev/', icon: Cpu, desc: 'List of software/services with free tiers' }
  ];

  return (
    <div style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
      <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>Labs & Resources</h2>
      <p className="text-muted" style={{ marginBottom: '32px' }}>Experimental modules and curated free resources.</p>
      
      <h3 style={{ fontSize: '20px', marginBottom: '16px' }}>My labs</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px', marginBottom: '32px' }}>
        {myLabs.map((lab, idx) => (
          <div key={idx} className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px', opacity: 0.7 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <lab.icon className="text-muted" size={24} />
              <span style={{ fontSize: '12px', padding: '4px 8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', color: '#888' }}>
                {lab.status}
              </span>
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '4px', color: '#fff' }}>{lab.title}</h3>
              <p className="text-muted" style={{ fontSize: '13px' }}>{lab.desc}</p>
            </div>
            <button 
              onClick={() => onOpenLab && onOpenLab(lab.id)}
              style={{ marginTop: 'auto', padding: '8px', background: 'var(--accent-teal)', color: '#000', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600 }}>
              Open
            </button>
          </div>
        ))}

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <UserCheck className="text-teal" size={24} />
            <span style={{ fontSize: '12px', padding: '4px 8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', color: 'var(--accent-teal)' }}>
              Active
            </span>
          </div>
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>Presence Provider</h3>
            <p className="text-muted" style={{ fontSize: '13px' }}>Mock contextual presence for the agent.</p>
          </div>
          <button 
            onClick={togglePresence}
            style={{ marginTop: 'auto', padding: '8px', background: isPresent ? 'var(--accent-teal)' : '#333', color: isPresent ? '#000' : '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600 }}
          >
            {isPresent ? "User is Present" : "User is Away"}
          </button>
        </div>

      </div>

      <h3 style={{ fontSize: '20px', marginBottom: '16px' }}>Free resources</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
        {resources.map((res, idx) => (
          <a key={idx} href={res.link} target="_blank" rel="noreferrer" className="glass-panel" style={{ padding: '20px', textDecoration: 'none', color: 'inherit', display: 'flex', flexDirection: 'column', gap: '12px', transition: 'all 0.2s' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <res.icon className="text-teal" size={24} />
              <ExternalLink size={16} className="text-muted" />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '4px' }}>{res.title}</h3>
              <p className="text-muted" style={{ fontSize: '13px' }}>{res.desc}</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
