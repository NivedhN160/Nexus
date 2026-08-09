import React from 'react';
import { ExternalLink, Database, Cpu, Globe } from 'lucide-react';

export default function LabsIndex() {
  const resources = [
    { title: 'Free APIs for Devs', link: 'https://github.com/public-apis/public-apis', icon: Globe, desc: 'A collective list of free APIs' },
    { title: 'Open Source Alternative To', link: 'https://github.com/RunaCapital/awesome-oss-alternatives', icon: Database, desc: 'OSS alternatives to SaaS' },
    { title: 'Free Tier Services', link: 'https://free-for.dev/', icon: Cpu, desc: 'List of software/services with free tiers' }
  ];

  return (
    <div style={{ padding: '24px', height: '100%', overflowY: 'auto' }}>
      <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>Labs & Resources</h2>
      <p className="text-muted" style={{ marginBottom: '32px' }}>Curated free resources inspired by the icopy-site/awesome index.</p>
      
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
