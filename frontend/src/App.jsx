import { useState, useEffect } from 'react';
import './App.css';
import { analyzeNews } from './services/api';
import BentoCard from './components/BentoCard';

function App() {
  const [inputText, setInputText] = useState('');
  const [inputType, setInputType] = useState('text');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    "ClaimAgent: Isolating keywords & entities...",
    "WebAgent: Scouting global news databases...",
    "ScraperAgent: Extracting neural content...",
    "EvidenceAgent: Analyzing BERT similarity...",
    "BiasAgent: Measuring emotional subjectivity...",
    "ReflectionAgent: Evaluating truth confidence..."
  ];

  useEffect(() => {
    let interval;
    if (loading) {
      setActiveStep(0);
      interval = setInterval(() => {
        setActiveStep(prev => (prev < steps.length - 1 ? prev + 1 : prev));
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleScan = async () => {
    if (!inputText) return;
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeNews(inputText, inputType);
      // Wait for terminal simulation to finish if it's too fast
      setResult(data);
      setLoading(false);
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
        <p className="subtitle">DECENTRALIZED MULTI-AGENT TRUTH IDENTIFICATION</p>
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
            {loading ? "DISTRIBUTING TO AGENT NETWORK..." : "⚡ START NEURAL SCAN"}
          </button>

          {loading && (
            <div className="neural-terminal animate-in">
              <div className="terminal-header">
                <span className="dot red"></span><span className="dot yellow"></span><span className="dot green"></span>
                <span className="terminal-title">AGENT_ACTIVITY_LOG</span>
              </div>
              <div className="terminal-body">
                {steps.map((step, i) => (
                  <div key={i} className={`log-line ${i === activeStep ? 'active' : i < activeStep ? 'done' : 'pending'}`}>
                    <span className="status-icon">{i < activeStep ? '✓' : i === activeStep ? '●' : '○'}</span>
                    <span className="log-text">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        {result && (
          <section className="result-section">
            
            <BentoCard className="bento-score" delay="0s">
               <div className="score-header"><h3>Neural Verdict</h3></div>
               <div className="circular-progress">
                  <div className="inner-circle">
                    <span className="score-value" style={{ color: result.prediction === 'Real' ? '#10b981' : result.prediction === 'Fake' ? '#f43f5e' : '#f59e0b' }}>
                      {Math.round(result.trust_score)}%
                    </span>
                  </div>
               </div>
               <div className={`score-badge ${result.prediction.toLowerCase()}`}>{result.status_label}</div>
               <div className="confidence-label">Confidence: <span>{result.confidence || 'Medium'}</span></div>
            </BentoCard>

            <BentoCard title="Neural Synthesis & Reasoning" delay="0.1s" className="bento-reasons">
                {result.neural_synthesis && (
                  <div className="synthesis-text animate-in">
                    <p>{result.neural_synthesis}</p>
                  </div>
                )}
                <div className="reason-divider">FOUNDATION FACTORS:</div>
                <ul className="reason-list">
                  {result.explanation ? result.explanation.map((r, i) => (
                    <li key={i} className="reason-item">{r}</li>
                  )) : (
                    <p className="insight-msg">{result.message}</p>
                  )}
                </ul>
            </BentoCard>

            <BentoCard title="Emotional Tone & Focus" delay="0.2s">
                <div className="sentiment-data">
                  <div className="s-row">
                    <span>Sentiment: </span>
                    <strong style={{ color: result.sentiment?.sentiment_label === 'Positive' ? '#10b981' : '#f43f5e' }}>{result.sentiment?.sentiment_label || 'Neutral'}</strong>
                  </div>
                  <div className="s-row">
                    <span>Subjectivity: </span>
                    <strong>{result.sentiment?.bias_label || 'Balanced'}</strong>
                  </div>
                  <div className="meter-label">Neural Bias Intensity</div>
                  <div className="bias-meter"><div className="meter-fill" style={{ width: `${(result.sentiment?.subjectivity || 0) * 100}%` }}></div></div>
                </div>
            </BentoCard>

            {result.top_flags && result.top_flags.length > 0 && (
               <BentoCard title="Neural Red Flags" delay="0.3s">
                  <div className="flags-grid">
                    {result.top_flags.map((flag, idx) => (
                      <span key={idx} className={`flag-chip ${result.prediction === 'Real' ? 'real' : 'fake'}`}>{flag}</span>
                    ))}
                  </div>
               </BentoCard>
            )}

            {result.related_news && result.related_news.length > 0 && (
               <BentoCard title="Live Cross-Reference (Found Evidence)" className="bento-related" delay="0.4s">
                  <div className="news-grid">
                    {result.related_news.map((news, idx) => (
                      <a href={news.url} target="_blank" rel="noreferrer" className="news-card" key={idx}>
                        <h4>{news.title}</h4>
                        <p>{news.body}</p>
                        <span className="read-more">SOURCE: {new URL(news.url).hostname.replace('www.', '')} ↗</span>
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
