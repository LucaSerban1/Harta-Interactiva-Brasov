import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../api';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  location_id?: number | null;
}

interface Props {
  onSelectLocation?: (id: number) => void;
  onSelectRoute?: (startId: number, endId: number) => void;
  onRefresh?: () => Promise<void>;
}

const SUGGESTIONS = [
  "Unde pot bea o cafea bună?",
  "Un loc bun pentru studiu",
  "O zonă verde pentru plimbare"
];

export default function AIAssistant({ onSelectLocation, onSelectRoute, onRefresh }: Props) {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', sender: 'ai', text: 'Salut! Sunt asistentul tău local. Cum te pot ajuta astăzi în Brașov?' }
  ]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const onSelectLocationRef = useRef(onSelectLocation);
  const onSelectRouteRef = useRef(onSelectRoute);

  useEffect(() => { onSelectLocationRef.current = onSelectLocation; }, [onSelectLocation]);
  useEffect(() => { onSelectRouteRef.current = onSelectRoute; }, [onSelectRoute]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, open, expanded]);

  // When user sends the first message, expand the window automatically
  useEffect(() => {
    if (messages.length > 1 && !expanded) {
      const timer = setTimeout(() => setExpanded(true), 10);
      return () => clearTimeout(timer);
    }
  }, [messages.length, expanded]);

  const handleAsk = async (textToSend: string) => {
    if (!textToSend.trim()) return;

    const userMessage: Message = { id: Date.now().toString(), sender: 'user', text: textToSend };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setPrompt('');
    setLoading(true);

    try {
      // Prepare history for backend
      const history = newMessages.map(m => ({
        role: m.sender === 'user' ? 'user' : 'assistant',
        content: m.text
      }));

      const data = await sendChatMessage(history);
      const textResponse = data.mesaj || data.eroare_detaliata || data.error || 'A apărut o eroare neașteptată.';
      
      const aiMessage: Message = { 
        id: (Date.now() + 1).toString(), 
        sender: 'ai', 
        text: textResponse,
        location_id: data.location_id
      };

      setMessages(prev => [...prev, aiMessage]);

      if (data.refresh_locations === "true" || data.refresh_locations === true) {
        if (onRefresh) await onRefresh();
      }

      if (data.start_location_id && data.location_id && onSelectRouteRef.current) {
        onSelectRouteRef.current(data.start_location_id, data.location_id);
      } else if (data.location_id && onSelectLocationRef.current) {
        setTimeout(() => {
          onSelectLocationRef.current!(data.location_id);
        }, 300);
      }
    } catch (_e: unknown) {
      setMessages(prev => [...prev, { 
        id: (Date.now() + 1).toString(), 
        sender: 'ai', 
        text: 'A apărut o eroare la conectarea cu AI-ul.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk(prompt);
    }
  };

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        style={{
          position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 9999,
          background: 'linear-gradient(135deg, #8b5cf6, #3b82f6)', color: 'white', padding: '1rem',
          borderRadius: '50%', border: 'none', cursor: 'pointer',
          boxShadow: '0 8px 20px rgba(139, 92, 246, 0.4)', width: '64px', height: '64px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '28px', transition: 'transform 0.2s',
        }}
        onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
        title="Recomandare AI"
      >
        ✨
      </button>
    );
  }

  // Calculate dynamic dimensions
  const windowWidth = expanded ? '400px' : '320px';
  const windowHeight = expanded ? '600px' : '400px';

  return (
    <div style={{
      position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 9999,
      width: windowWidth, height: windowHeight, 
      background: 'rgba(255, 255, 255, 0.85)', 
      backdropFilter: 'blur(16px)',
      borderRadius: '24px',
      boxShadow: '0 15px 35px rgba(0,0,0,0.2)', display: 'flex', flexDirection: 'column',
      overflow: 'hidden', color: '#1e293b',
      border: '1px solid rgba(255, 255, 255, 0.6)',
      transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
      fontFamily: '"Inter", "Segoe UI", sans-serif'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(135deg, #8b5cf6, #3b82f6)', 
        padding: '1.2rem', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
        flexShrink: 0
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '22px' }}>✨</span>
          <h3 style={{ margin: 0, fontSize: '17px', fontWeight: 600, letterSpacing: '0.5px' }}>Ghid Local AI</h3>
        </div>
        <button 
          onClick={() => setOpen(false)} 
          style={{ background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '20px', opacity: 0.8, transition: 'all 0.2s', padding: '0 4px' }} 
          onMouseOver={e => { e.currentTarget.style.opacity='1'; e.currentTarget.style.transform='scale(1.1)'; }} 
          onMouseOut={e => { e.currentTarget.style.opacity='0.8'; e.currentTarget.style.transform='scale(1)'; }}>
            ✕
        </button>
      </div>

      {/* Messages Area */}
      <div style={{ 
        padding: '1.5rem 1rem', flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px',
        scrollBehavior: 'smooth'
      }}>
        {messages.map(msg => (
          <div key={msg.id} style={{ 
            alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '85%',
            background: msg.sender === 'user' ? 'linear-gradient(135deg, #8b5cf6, #7c3aed)' : '#f8fafc',
            color: msg.sender === 'user' ? 'white' : '#334155',
            padding: '12px 16px',
            borderRadius: msg.sender === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
            fontSize: '15px',
            lineHeight: '1.5',
            boxShadow: msg.sender === 'user' ? '0 4px 10px rgba(139, 92, 246, 0.2)' : '0 2px 8px rgba(0,0,0,0.04)',
            border: msg.sender === 'user' ? 'none' : '1px solid #e2e8f0'
          }}>
            {msg.text}
          </div>
        ))}

        {loading && (
          <div style={{ 
            alignSelf: 'flex-start', background: '#f8fafc', color: '#64748b', 
            padding: '12px 16px', borderRadius: '20px 20px 20px 4px', fontSize: '15px',
            display: 'flex', gap: '6px', border: '1px solid #e2e8f0', boxShadow: '0 2px 8px rgba(0,0,0,0.04)'
          }}>
            <span style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '-0.32s' }}>•</span>
            <span style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '-0.16s' }}>•</span>
            <span style={{ animation: 'bounce 1.4s infinite ease-in-out both' }}>•</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={{ padding: '1rem', borderTop: '1px solid rgba(0,0,0,0.05)', background: 'rgba(255, 255, 255, 0.95)', flexShrink: 0 }}>
        
        {/* Suggestion Chips */}
        {!expanded && messages.length === 1 && (
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px', scrollbarWidth: 'none' }}>
            {SUGGESTIONS.map((sug, idx) => (
              <button 
                key={idx}
                onClick={() => handleAsk(sug)}
                style={{
                  background: '#f1f5f9', border: '1px solid #e2e8f0', color: '#475569',
                  borderRadius: '16px', padding: '6px 12px', fontSize: '13px', cursor: 'pointer',
                  whiteSpace: 'nowrap', transition: 'all 0.2s'
                }}
                onMouseOver={e => { e.currentTarget.style.background = '#e2e8f0'; e.currentTarget.style.color = '#1e293b'; }}
                onMouseOut={e => { e.currentTarget.style.background = '#f1f5f9'; e.currentTarget.style.color = '#475569'; }}
              >
                {sug}
              </button>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Scrie un mesaj..."
            style={{ 
              flex: 1, padding: '12px 16px', borderRadius: '24px', 
              border: '1px solid #cbd5e1', fontSize: '15px', boxSizing: 'border-box', 
              color: '#1e293b', background: '#f8fafc', outline: 'none',
              transition: 'border-color 0.2s, box-shadow 0.2s'
            }}
            onFocus={e => { e.target.style.borderColor = '#8b5cf6'; e.target.style.boxShadow = '0 0 0 3px rgba(139, 92, 246, 0.1)'; }}
            onBlur={e => { e.target.style.borderColor = '#cbd5e1'; e.target.style.boxShadow = 'none'; }}
          />
          <button
            onClick={() => handleAsk(prompt)}
            disabled={loading || !prompt.trim()}
            style={{ 
              width: '44px', height: '44px', borderRadius: '50%', flexShrink: 0,
              background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', color: 'white', border: 'none', 
              cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
              opacity: (loading || !prompt.trim()) ? 0.5 : 1, transition: 'all 0.2s',
              boxShadow: (loading || !prompt.trim()) ? 'none' : '0 4px 10px rgba(139, 92, 246, 0.3)'
            }}
            onMouseOver={e => { if(!loading && prompt.trim()) e.currentTarget.style.transform = 'scale(1.05)' }}
            onMouseOut={e => { if(!loading && prompt.trim()) e.currentTarget.style.transform = 'scale(1)' }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
      
      {/* Add keyframes for bouncing animation globally */}
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-4px); }
        }
      `}</style>
    </div>
  );
}
