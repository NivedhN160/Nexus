import React, { useState } from 'react';
import { Send } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

export default function AgentChat() {
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState<Message[]>([
    { role: 'assistant', text: 'Nexus Agent initialized. Local LLM mode active. Standing by for command.' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!inputText.trim() || isLoading) return;
    
    const userMsg = inputText.trim();
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);
    setInputText('');
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/brain/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'nexus_dev_key' // Match the .env default
        },
        body: JSON.stringify({
          text: userMsg,
          session_id: 'default',
          history: chatHistory.map(m => ({ role: m.role, content: m.text }))
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      setChatHistory(prev => [...prev, { role: 'assistant', text: data.answer }]);
      
    } catch (error) {
      console.error("Chat error:", error);
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        text: 'Error connecting to Nexus Brain. Is the backend running?' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '24px', paddingRight: '12px' }}>
        {chatHistory.map((msg, idx) => (
          <div key={idx} style={{ 
            marginBottom: '16px', 
            display: 'flex', 
            flexDirection: 'column',
            alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' 
          }}>
            <div style={{
              fontSize: '12px',
              color: 'var(--text-secondary)',
              marginBottom: '4px',
              textTransform: 'uppercase',
              letterSpacing: '1px'
            }}>
              {msg.role === 'user' ? 'Operator' : 'Nexus'}
            </div>
            <div className="glass-panel" style={{
              padding: '12px 16px',
              maxWidth: '80%',
              background: msg.role === 'user' ? 'rgba(0, 240, 255, 0.05)' : 'var(--glass-bg)',
              borderLeft: msg.role === 'assistant' ? '2px solid var(--accent-teal)' : '1px solid var(--border-color)',
              borderRight: msg.role === 'user' ? '2px solid var(--text-primary)' : '1px solid var(--border-color)'
            }}>
              <span className="mono" style={{ fontSize: '13px', lineHeight: '1.5' }}>{msg.text}</span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px', textTransform: 'uppercase', letterSpacing: '1px' }}>Nexus</div>
            <div className="glass-panel mono text-teal" style={{ padding: '12px 16px', borderLeft: '2px solid var(--accent-teal)', fontSize: '13px' }}>
              Processing local request...
            </div>
          </div>
        )}
      </div>
      
      <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', padding: '12px' }}>
        <input 
          type="text" 
          value={inputText}
          onChange={e => setInputText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="Enter command..." 
          className="mono"
          disabled={isLoading}
          style={{ 
            flex: 1, 
            background: 'transparent', 
            border: 'none', 
            color: 'var(--text-primary)', 
            outline: 'none',
            fontSize: '14px',
            opacity: isLoading ? 0.5 : 1
          }} 
        />
        <button className="btn" onClick={handleSend} disabled={isLoading} style={{ display: 'flex', alignItems: 'center', gap: '8px', opacity: isLoading ? 0.5 : 1 }}>
          <Send size={16} /> Execute
        </button>
      </div>
    </div>
  );
}
