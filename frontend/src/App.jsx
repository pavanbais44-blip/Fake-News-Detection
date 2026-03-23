import { useState } from 'react';
import './App.css';
import { analyzeNews } from './services/api';
import BentoCard from './components/BentoCard';

function App() {
  const [inputText, setInputText] = useState('');
  const [inputType, setInputType] = useState('text');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleScan = async () => {
    if (!inputText) return;
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeNews(inputText, inputType);
      
      // Artificial delay for better UX neural scan feeling
      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 1000);

    } catch (error) {
      setResult({ 
        prediction: "Error", 
        message: `Neural Engine Offline: ${error.message}`,
        trust_score: 0,
        status_label: "🚨 ERROR",
        sentiment: { polarity: 0, subjectivity: 0, sentiment_label: "Offline", bias_label: "Offline" }
      });
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="mesh-glow-1"></div>
      <div className="mesh-glow-2"></div>
      
      <header className="header animate-in">
        <h1 className="logo">🛡️ Truth<span>Guard</span></h1>
        <p className="subtitle">DECENTRALIZED AGENTIC TRUTH IDENTIFICATION</p>
      </header>

      <main className="main-content">
        <section className="glass-panel input-section animate-in">
          <div className="tab-container">
            <button className={`tab ${inputType === 'text' ? 'active' : ''}`} onClick={() => { setInputType('text'); setInputText(''); setResult(null); }}>📝 DEEP SCAN</button>
            <button className={`tab ${inputType === 'url' ? 'active' : ''}`} onClick={() => { setInputType('url'); setInputText(''); setResult(null); }}>🔗 URL SCAN</button>
          </div>

          <div className="input-area">
            {inputType === 'text' ? (
              <textarea placeholder="Paste source material here for agentic analysis..." value={inputText} onChange={(e) => setInputText(e.target.value)} rows={6} />
            ) : (
              <input type="url" placeholder="Enter news URL for a real-time credibility scan..." value={inputText} onChange={(e) => setInputText(e.target.value)} className="url-input" />
            )}
          </div>

          <button className={`scan-btn ${loading ? 'loading' : ''} ${!inputText ? 'disabled' : ''}`} onClick={handleScan} disabled={!inputText || loading}>
            {loading ? "DISTRIBUTING TASKS TO AGENTS..." : "⚡ START NEURAL SCAN"}
          </button>
        </section>

        {result && (
          <section className="result-section">
            
            <BentoCard className="bento-score" delay="0s">
               <div className="score-header"><h3>Neural Verdict</h3></div>
               <div className="circular-progress">
                  <div className="inner-circle">
                    <span className="score-value" style={{ color: result.prediction === 'Real' ? '#10b981' : '#f43f5e' }}>{result.trust_score}%</span>
                  </div>
               </div>
               <div className={`score-badge ${result.prediction === 'Real' ? 'real' : 'fake'}`}>{result.status_label}</div>
            </BentoCard>

            <BentoCard title="Agent Insights" delay="0.1s">
                <div className="insight-msg">{result.message || "Deep learning scan complete."}</div>
            </BentoCard>

            <BentoCard title="Bias Analysis" delay="0.2s">
                <div className="sentiment-data">
                  <div className="s-row">
                    <span>Tone: </span>
                    <strong style={{ color: result.sentiment?.polarity < -0.2 ? '#f43f5e' : '#10b981' }}>{result.sentiment?.sentiment_label}</strong>
                  </div>
                  <div className="s-row">
                    <span>Subjectivity: </span>
                    <strong style={{ color: result.sentiment?.subjectivity > 0.5 ? '#f59e0b' : '#10b981' }}>{result.sentiment?.bias_label}</strong>
                  </div>
                  <div className="bias-meter"><div className="meter-fill" style={{ width: `${(result.sentiment?.subjectivity || 0) * 100}%` }}></div></div>
                </div>
            </BentoCard>

            {result.top_flags && (
               <BentoCard title="Context Flags" delay="0.3s">
                  <div className="flags-grid">
                    {result.top_flags.map((flag, idx) => (
                      <span key={idx} className={`flag-chip ${result.prediction === 'Real' ? 'real' : 'fake'}`}>{flag}</span>
                    ))}
                  </div>
               </BentoCard>
            )}

            {result.related_news && result.related_news.length > 0 && (
               <BentoCard title="Live Cross-Reference" className="bento-related" delay="0.4s">
                  <div className="news-grid">
                    {result.related_news.map((news, idx) => (
                      <a href={news.url} target="_blank" rel="noreferrer" className="news-card" key={idx}>
                        <h4>{news.title}</h4>
                        <p>{news.body}</p>
                        <span className="read-more">VIEW SOURCE ↗</span>
                      </a>
                    ))}
                  </div>
               </BentoCard>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
