import React from 'react';
import { Share2, Clock, CheckCircle2, Activity, Globe } from 'lucide-react';

export default function SocialGraph() {
  const scheduledPosts = [
    { id: 1, platform: 'Twitter / X', content: 'Excited to announce the new Nexus platform architecture! 🚀 #AI #BuildInPublic', time: 'In 2 hours', status: 'queued' },
    { id: 2, platform: 'LinkedIn', content: 'Just finished migrating our entire stack to a monolithic decoupled architecture. The performance gains are incredible.', time: 'In 5 hours', status: 'queued' },
    { id: 3, platform: 'Twitter / X', content: 'Micro-cents for LLM pricing? Yes, it solves floating point errors at scale. 💡', time: 'Yesterday', status: 'published' }
  ];

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Share2 className="text-teal" size={20} /> Social Graph
          </h2>
          <p className="text-muted" style={{ fontSize: '14px', marginTop: '4px' }}>Cross-platform distribution & variant generation</p>
        </div>
        <button className="btn" style={{ fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={14} /> Force Sync
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px' }}>
        {[
          { label: 'Total Reach', value: '14.2k', change: '+12%' },
          { label: 'Active Platforms', value: '2', change: 'X, LinkedIn' },
          { label: 'Queued Posts', value: '12', change: 'Next: 2 hrs' }
        ].map(stat => (
          <div key={stat.label} className="glass-panel" style={{ padding: '20px' }}>
            <div className="text-muted" style={{ fontSize: '13px', textTransform: 'uppercase', letterSpacing: '1px' }}>{stat.label}</div>
            <div className="mono text-teal" style={{ fontSize: '28px', margin: '8px 0' }}>{stat.value}</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{stat.change}</div>
          </div>
        ))}
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Globe size={16} className="text-teal" />
          <h3 style={{ fontSize: '14px', fontWeight: 500 }}>Content Pipeline</h3>
        </div>
        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto' }}>
          {scheduledPosts.map(post => (
            <div key={post.id} style={{ 
              display: 'flex', 
              gap: '16px', 
              padding: '16px', 
              background: 'rgba(0,0,0,0.2)', 
              borderRadius: '8px',
              borderLeft: post.status === 'published' ? '2px solid var(--text-secondary)' : '2px solid var(--accent-teal)'
            }}>
              <div style={{ width: '100px', flexShrink: 0 }}>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px' }}>{post.platform}</div>
                <div className="mono text-teal" style={{ fontSize: '11px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  {post.status === 'published' ? <CheckCircle2 size={12} /> : <Clock size={12} />}
                  {post.time}
                </div>
              </div>
              <div style={{ flex: 1, fontSize: '14px', color: 'var(--text-primary)', lineHeight: '1.5' }}>
                {post.content}
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
