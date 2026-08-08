import React, { useState, useEffect } from 'react';
import { Share2, Clock, CheckCircle2, AlertCircle } from 'lucide-react';

interface CampaignPost {
  platform: string;
  caption: string;
  status: string;
}

interface Campaign {
  id: number;
  run_at: string | null;
  status: string;
  posts: CampaignPost[];
}

export default function SocialGraph() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/campaigns`, {
          headers: {
            'X-API-Key': import.meta.env.VITE_API_KEY || 'nexus_dev_key'
          }
        });
        if (res.ok) {
          const data = await res.json();
          setCampaigns(data);
        }
      } catch (e) {
        console.error('Failed to fetch campaigns', e);
      } finally {
        setLoading(false);
      }
    };
    fetchCampaigns();
  }, []);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Share2 className="text-teal" size={20} /> Social Graph
          </h2>
          <p className="text-muted" style={{ fontSize: '14px', marginTop: '4px' }}>Multi-platform distribution campaigns</p>
        </div>
        <button className="btn" style={{ fontSize: '13px' }}>
          + New Campaign
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', flex: 1, overflowY: 'auto' }}>
        {loading && (
          <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
            Loading campaigns...
          </div>
        )}
        
        {!loading && campaigns.length === 0 && (
          <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
            No campaigns active.
          </div>
        )}

        {campaigns.map((camp) => (
          <div key={camp.id} className="glass-panel" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: 600 }}>Campaign #{camp.id}</h3>
                <span style={{ 
                  fontSize: '11px', 
                  padding: '4px 8px', 
                  borderRadius: '12px', 
                  background: camp.status === 'draft' ? 'rgba(255,255,255,0.1)' : 'rgba(0, 240, 255, 0.1)',
                  color: camp.status === 'draft' ? 'var(--text-secondary)' : 'var(--accent-teal)',
                  textTransform: 'uppercase'
                }}>
                  {camp.status}
                </span>
              </div>
              <div className="mono text-muted" style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Clock size={12} /> {camp.run_at ? new Date(camp.run_at).toLocaleString() : 'Not scheduled'}
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              {camp.posts.map((post, pIdx) => (
                <div key={pIdx} style={{ background: 'rgba(0,0,0,0.2)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span style={{ fontWeight: 600, fontSize: '14px', color: 'var(--text-primary)' }}>{post.platform}</span>
                    {post.status === 'delivered' ? (
                      <CheckCircle2 size={16} className="text-teal" />
                    ) : post.status === 'failed' ? (
                      <AlertCircle size={16} className="text-amber" />
                    ) : (
                      <Clock size={16} className="text-muted" />
                    )}
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                    {post.caption}
                  </p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
