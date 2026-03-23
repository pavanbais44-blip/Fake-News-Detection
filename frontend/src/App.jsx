import { useState } from 'react'
import './App.css'

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
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: inputType === 'text' ? inputText : null,
          url: inputType === 'url' ? inputText : null
        })
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Scanner Anomaly");
      
      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 800);

    } catch (error) {
      console.error("Error:", error);
      setResult({ 
        prediction: "Error", 
        message: `System Error: ${error.message}. Backend Connection Offline.`,
        trust_score: 0,
        status_label: "🚨 ERROR",
        related_news: [],
        top_flags: [],
        source_reliability: "Unknown",
        domain: "",
        sentiment: { polarity: 0, subjectivity: 0, sentiment_label: "Error", bias_label: "Error" }
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
        <p className="subtitle">AI-POWERED TRUTH IDENTIFICATION ENGINE</p>
      </header>

      <main className="main-content">
        <div className="glass-panel input-section animate-in">
          <div className="tab-container">
            <button className={`tab ${inputType === 'text' ? 'active' : ''}`} onClick={() => { setInputType('text'); setInputText(''); setResult(null); }}>📝 DEEP ANALYSIS</button>
            <button className={`tab ${inputType === 'url' ? 'active' : ''}`} onClick={() => { setInputType('url'); setInputText(''); setResult(null); }}>🔗 URL SCANNER</button>
          </div>

          <div className="input-area">
            {inputType === 'text' ? (
              <textarea placeholder="Paste the source material here to analyze neural patterns..." value={inputText} onChange={(e) => setInputText(e.target.value)} rows={6} />
            ) : (
              <input type="url" placeholder="Enter live news URL for instant credibility scan..." value={inputText} onChange={(e) => setInputText(e.target.value)} className="url-input" />
            )}
          </div>

          <button className={`scan-btn ${loading ? 'loading' : ''} ${!inputText ? 'disabled' : ''}`} onClick={handleScan} disabled={!inputText || loading}>
            {loading ? "INITIALIZING NEURAL SCAN..." : "⚡ START ENGINE"}
          </button>
        </div>

        {result && (
          <div className="result-section">
            
            <div className="bento-card bento-score animate-in">
               <div className="score-header"><h3>Current Trust</h3></div>
               <div className="circular-progress">
                  <div className="inner-circle">
                    <span className="score-value" style={{ color: result.prediction === 'Real' ? '#10b981' : '#f43f5e' }}>{result.trust_score}%</span>
                  </div>
               </div>
               <div className={`score-badge ${result.prediction === 'Real' ? 'real' : 'fake'}`}>{result.status_label}</div>
            </div>

            <div className="bento-card bento-insight animate-in" style={{ animationDelay: '0.1s' }}>
                <div className="insight-header">AI Neural Analysis</div>
                <div className="insight-msg">{result.message}</div>
            </div>

            {/* --- 🧠 SENTIMENT & BIAS ANALYSIS BENTO BOX --- */}
            <div className="bento-card bento-flags animate-in" style={{ animationDelay: '0.2s' }}>
                <div className="insight-header">Emotional Tone & Bias</div>
                <div className="sentiment-data">
                  <div className="s-row">
                    <span>Tone: </span>
                    <strong style={{ color: result.sentiment.polarity < -0.2 ? '#f43f5e' : result.sentiment.polarity > 0.2 ? '#10b981' : '#64748b' }}>
                      {result.sentiment.sentiment_label}
                    </strong>
                  </div>
                  <div className="s-row">
                    <span>Bias Type: </span>
                    <strong style={{ color: result.sentiment.subjectivity > 0.5 ? '#f59e0b' : '#10b981' }}>
                      {result.sentiment.bias_label}
                    </strong>
                  </div>
                  <div className="bias-meter-container">
                    <div className="meter-label">Fact vs Opinion</div>
                    <div className="meter"><div className="meter-fill" style={{ width: `${result.sentiment.subjectivity * 100}%`, background: result.sentiment.subjectivity > 0.5 ? '#f59e0b' : '#6366f1' }}></div></div>
                  </div>
                </div>
            </div>

            {result.domain && (
               <div className="bento-card bento-domain animate-in" style={{ animationDelay: '0.3s' }}>
                  <div className="insight-header">Publisher ID</div>
                  <div className="domain-name">{result.domain}</div>
                  <div className={`reliability-badge ${result.source_reliability.toLowerCase().includes('high') ? 'reliable' : result.source_reliability.toLowerCase().includes('low') ? 'danger' : 'neutral'}`}>
                    {result.source_reliability}
                  </div>
               </div>
            )}

            <div className="bento-card animate-in" style={{ animationDelay: '0.4s' }}>
                <div className="insight-header">{result.prediction === 'Fake' ? '🔴 RED FLAGS' : '🔵 KEYWORDS'}</div>
                <div className="flags-grid">
                  {result.top_flags && result.top_flags.map((flag, idx) => (
                    <span key={idx} className={`flag-chip ${result.prediction === 'Real' ? 'real' : 'fake'}`}>{flag}</span>
                  ))}
                </div>
            </div>

            {result.related_news && result.related_news.length > 0 && (
               <div className="bento-card bento-related animate-in" style={{ animationDelay: '0.5s' }}>
                  <div className="insight-header">📡 LIVE CROSS-REFERENCE (REAL NEWS)</div>
                  <div className="news-grid">
                    {result.related_news.map((news, idx) => (
                      <a href={news.url} target="_blank" rel="noreferrer" className="news-card" key={idx}>
                        <h4>{news.title}</h4>
                        <p>{news.body}</p>
                        <span className="read-more">VIEW SOURCE ↗</span>
                      </a>
                    ))}
                  </div>
               </div>
            )}

          </div>
        )}
      </main>
    </div>
  )
}

export default App
