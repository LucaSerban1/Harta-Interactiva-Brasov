import { useState } from 'react';
import { fetchAIRecommendation } from '../api';

export default function AIAssistant() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const handleAsk = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setResponse('');
    try {
      const data = await fetchAIRecommendation(prompt);
      if (data.recomandare) {
        setResponse(data.recomandare);
      } else if (data.eroare_detaliata) {
        setResponse(`Eroare: ${data.eroare_detaliata}`);
      } else if (data.error) {
        setResponse(`Eroare: ${data.error}`);
      } else {
        setResponse(JSON.stringify(data));
      }
    } catch (e: unknown) {
      setResponse('A apărut o eroare la conectarea cu AI-ul.');
    } finally {
      setLoading(false);
    }
  };

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        style={{
          position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 9999,
          background: '#8b5cf6', color: 'white', padding: '1rem',
          borderRadius: '50%', border: 'none', cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)', width: '60px', height: '60px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '24px'
        }}
        title="Recomandare AI"
      >
        ✨
      </button>
    );
  }

  return (
    <div style={{
      position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 9999,
      width: '320px', background: 'white', borderRadius: '12px',
      boxShadow: '0 4px 20px rgba(0,0,0,0.2)', display: 'flex', flexDirection: 'column',
      overflow: 'hidden', color: 'black'
    }}>
      <div style={{ background: '#8b5cf6', padding: '1rem', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '16px' }}>✨ AI Recomandări</h3>
        <button onClick={() => setOpen(false)} style={{ background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', fontSize: '16px' }}>✕</button>
      </div>
      <div style={{ padding: '1rem', flex: 1, maxHeight: '350px', overflowY: 'auto' }}>
        <p style={{ fontSize: '14px', margin: '0 0 1rem 0' }}>Spune-mi ce cauți în Brașov!</p>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ex: da-mi o recomandare de cafenea unde pot invata..."
          style={{ width: '100%', height: '80px', padding: '0.5rem', borderRadius: '8px', border: '1px solid #ccc', marginBottom: '1rem', resize: 'none', fontSize: '14px', boxSizing: 'border-box', color: 'black', background: 'white' }}
        />
        <button
          onClick={handleAsk}
          disabled={loading || !prompt.trim()}
          style={{ width: '100%', padding: '0.5rem', background: '#8b5cf6', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', opacity: (loading || !prompt.trim()) ? 0.7 : 1 }}
        >
          {loading ? 'Se gândește...' : 'Întreabă AI'}
        </button>
        {response && (
          <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#f3f4f6', borderRadius: '8px', fontSize: '14px', whiteSpace: 'pre-wrap', color: '#1f2937' }}>
            {response}
          </div>
        )}
      </div>
    </div>
  );
}
