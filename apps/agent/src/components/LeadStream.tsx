import React, { useState, useEffect } from 'react';
import { Layers, CheckCircle2, XCircle, Target, Filter } from 'lucide-react';

interface Lead {
  id: number;
  name: string;
  email: string;
  message: string;
  geo: string | null;
  status: string;
}

export default function LeadStream() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/leads/admin/submissions`, {
          headers: {
            'X-API-Key': import.meta.env.VITE_API_KEY || 'nexus_dev_key'
          }
        });
        if (res.ok) {
          const data = await res.json();
          setLeads(data);
        }
      } catch (e) {
        console.error('Failed to fetch leads', e);
      } finally {
        setLoading(false);
      }
    };
    fetchLeads();
  }, []);

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '24px', padding: '24px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers className="text-teal" size={20} /> Lead Stream
          </h2>
          <p className="text-muted" style={{ fontSize: '14px', marginTop: '4px' }}>Inbound pipeline from public surfaces</p>
        </div>
        <button className="btn" style={{ fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Filter size={14} /> Filter Stream
        </button>
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', backgroundColor: 'rgba(0,0,0,0.2)' }}>
              <th style={{ padding: '16px', fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>ID / Region</th>
              <th style={{ padding: '16px', fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Prospect</th>
              <th style={{ padding: '16px', fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Message</th>
              <th style={{ padding: '16px', fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>AI Intent</th>
              <th style={{ padding: '16px', fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={5} style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  Loading leads...
                </td>
              </tr>
            )}
            {!loading && leads.length === 0 && (
              <tr>
                <td colSpan={5} style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  No leads found.
                </td>
              </tr>
            )}
            {leads.map(lead => (
              <tr key={lead.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.02)' }}>
                <td style={{ padding: '16px' }}>
                  <div className="mono text-teal" style={{ fontSize: '12px' }}>LD-{lead.id}</div>
                  <div className="text-muted" style={{ fontSize: '11px', marginTop: '4px' }}>{lead.geo || 'Unknown'}</div>
                </td>
                <td style={{ padding: '16px' }}>
                  <div style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-primary)' }}>{lead.name}</div>
                  <div className="text-muted" style={{ fontSize: '12px', marginTop: '4px' }}>{lead.email}</div>
                </td>
                <td style={{ padding: '16px' }}>
                  <div style={{ fontSize: '13px', color: 'var(--text-secondary)', maxWidth: '250px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {lead.message}
                  </div>
                </td>
                <td style={{ padding: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Target size={14} className="text-teal" />
                    <span className="mono" style={{ fontSize: '13px' }}>--%</span>
                  </div>
                </td>
                <td style={{ padding: '16px' }}>
                  {lead.status === 'new' ? (
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button style={{ background: 'rgba(0, 240, 255, 0.1)', border: '1px solid var(--accent-teal)', color: 'var(--accent-teal)', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px' }}>
                        <CheckCircle2 size={14} /> Accept
                      </button>
                      <button style={{ background: 'rgba(255, 255, 255, 0.05)', border: '1px solid transparent', color: 'var(--text-secondary)', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px' }}>
                        <XCircle size={14} /> Discard
                      </button>
                    </div>
                  ) : (
                    <span style={{ fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'capitalize' }}>
                      {lead.status}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
