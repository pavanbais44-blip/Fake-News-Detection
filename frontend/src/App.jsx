import { useState, useEffect } from 'react';
import './App.css';
import { analyzeNews, submitFeedback, generateFake } from './services/api';

function App() {
  const [inputText, setInputText] = useState('');
  const [inputType, setInputType] = useState('text');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [deepAnalysis, setDeepAnalysis] = useState(true);
  const [feedbackSent, setFeedbackSent] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('tg_history');
    return saved ? JSON.parse(saved) : [];
  });
  
  const steps = [
    "ISOLATING CLAIM ENTITIES",
    "CROSS-REFERENCING GLOBAL DATABASES",
    "SCRAPING VERIFIED SOURCES",
    "ANALYZING NEURAL PATTERNS",
    "EVALUATING EMOTIONAL BIAS",
    "FINALIZING FORENSIC VERDICT"
  ];

  useEffect(() => {
    localStorage.setItem('tg_history', JSON.stringify(history.slice(0, 5)));
  }, [history]);

  useEffect(() => {
    let interval;
    if (loading) {
      setActiveStep(0);
      interval = setInterval(() => {
        setActiveStep(prev => (prev < steps.length - 1 ? prev + 1 : prev));
      }, deepAnalysis ? 1500 : 700);
    }
    return () => clearInterval(interval);
  }, [loading, deepAnalysis]);

  const handleScan = async () => {
    if (!inputText) return;
    setLoading(true);
    setResult(null);
    setFeedbackSent(false);

    try {
      const data = await analyzeNews(inputText, inputType);
      setHistory(prev => [{ text: inputText.substring(0, 30) + "...", verdict: data.final_verdict, date: new Date().toLocaleTimeString() }, ...prev]);
      setResult(data);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      alert("Neural Lab Connection Failed.");
    }
  };

  const handleGenerate = async () => {
    if (!inputText) return;
    setIsGenerating(true);
    try {
      const data = await generateFake(inputText);
      setInputText(data.synthetic_fake);
      setIsGenerating(false);
    } catch (e) {
      setIsGenerating(false);
      alert("Calibration Error.");
    }
  };

  const handleFeedback = async (label) => {
    try {
      await submitFeedback(inputText, label);
      setFeedbackSent(true);
    } catch (e) {
      alert("Calibration Error.");
    }
  };

  return (
    <div className="app-wrapper">
      <div className="bg-glow"></div>
      
      {/* 🏛️ NAVIGATION */}
      <nav className="navbar animate-in">
        <div className="nav-logo">TRUTH<span>GUARD</span>.LAB</div>
        <div className="nav-actions">
           <div className="scan-mode">
              <span>{deepAnalysis ? "DEEP FORENSICS" : "QUICK SCAN"}</span>
              <label className="switch">
                 <input type="checkbox" checked={deepAnalysis} onChange={() => setDeepAnalysis(!deepAnalysis)} />
                 <span className="slider round"></span>
              </label>
           </div>
           <div className="history-badge">HISTORY: {history.length}</div>
        </div>
      </nav>

      <main className="container">
        
        {/* 🔍 INPUT HUB */}
        {!result && !loading && (
          <section className="hero-section animate-in">
            <h1 className="hero-title">Verify the World's Information.</h1>
            <p className="hero-subtitle">Agentic Multi-Layer Disinformation Detection Engine</p>
            
            <div className="input-card">
               <div className="input-tabs">
                  <button className={inputType === 'text' ? 'active' : ''} onClick={() => setInputType('text')}>TEXT INPUT</button>
                  <button className={inputType === 'url' ? 'active' : ''} onClick={() => setInputType('url')}>URL LINK</button>
               </div>
               <div className="input-field">
                  {inputType === 'text' ? (
                    <textarea placeholder="Paste your source text here..." value={inputText} onChange={(e) => setInputText(e.target.value)} rows={5} />
                  ) : (
                    <input type="url" placeholder="Enter article URL..." value={inputText} onChange={(e) => setInputText(e.target.value)} />
                  )}
               </div>
               <div className="action-row">
                  <button className="main-scan-btn" onClick={handleScan}>RUN FORENSIC ANALYSIS</button>
                  <button className="gen-fake-btn" onClick={handleGenerate} disabled={isGenerating}>
                     {isGenerating ? "GENERATING..." : "SYNTHETIC LAB 🧪"}
                  </button>
               </div>
            </div>
          </section>
        )}

        {/* 🚦 ANALYZING STATE */}
        {loading && (
          <section className="loading-stage animate-in">
             <div className="scanner-ui">
                <div className="scan-line"></div>
                <h2>Neural Investigation in Progress...</h2>
                <div className="step-viewer">
                   {steps[activeStep]}
                </div>
                <div className="progress-pills">
                  {steps.map((_, i) => <div key={i} className={`pill ${i <= activeStep ? 'active' : ''}`}></div>)}
                </div>
             </div>
          </section>
        )}

        {/* 📊 FORENSIC REPORT RESULTS */}
        {result && !loading && (
          <section className="report-layout animate-in">
            <div className="report-header">
               <button className="back-btn" onClick={() => setResult(null)}>← NEW INVESTIGATION</button>
               <div className="report-id">REPORT ID: #{Math.random().toString(36).substring(7).toUpperCase()} | <span className="h-guard">HALLUCINATION GUARD: {result.confidence === 'high' ? 'PASSED' : 'CAUTION'}</span></div>
            </div>

             {/* MAIN VERDICT CARD */}
             <div className={`verdict-banner ${result.final_verdict.toLowerCase()}`}>
                <div className="v-label">
                  NEURAL VERDICT - {result.risk_level}
                  {result.temporal && !result.temporal.is_suspiciously_stale && (
                    <span className="live-badge-glow">● LIVE NEWS INDEXED</span>
                  )}
                </div>
                <div className="v-status">{result.final_verdict.toUpperCase()}</div>
                <div className="v-trust">
                   <span>TRUTH SCORE: {Math.round(result.truth_score * 100)}%</span>
                   <div className="trust-meter"><div className="fill" style={{ width: `${result.truth_score * 100}%` }}></div></div>
                </div>
             </div>

            <div className="insight-section">
               <h3>Synthesis Narrative</h3>
               <p className="narrative-text">"{result.neural_synthesis}"</p>
            </div>

            {/* 🟢 TOP TRUTH SOURCE (New Focal Point) */}
            {result.truth_source && (
               <div className={`truth-source-callout ${result.truth_source.label.toLowerCase()}`}>
                  <div className="callout-header">
                     <span className="source-type-badge">{result.final_verdict === 'Fake' ? 'CORRECTION SOURCE' : 'PRIMARY VERIFIER'}</span>
                     <span className="source-domain-inline">{new URL(result.truth_source.url).hostname.replace('www.', '')}</span>
                  </div>
                  <h4>{result.truth_source.title}</h4>
                  <p>{result.truth_source.snippet}</p>
                  <a href={result.truth_source.url} target="_blank" rel="noreferrer" className="truth-link">READ FULL REPORT ↗</a>
               </div>
            )}

            {/* NEURAL DEBATE ARENA (UPGRADE 1) */}
            <div className="debate-arena">
               <div className="debate-header">Neural Argumentative Cross-Examination</div>
               <div className="debate-grid">
                  <div className="debate-card alpha">
                     <label>AGENT ALPHA (REAL-ARGUE)</label>
                     <p>{result.debate?.real_argument}</p>
                  </div>
                  <div className="debate-card omega">
                     <label>AGENT OMEGA (FAKE-ARGUE)</label>
                     <p>{result.debate?.fake_argument}</p>
                  </div>
               </div>
               <div className="judge-box">JUDGE RATIONALE: {result.debate?.judge_rationale}</div>
            </div>

            {/* TOOL USAGE FLOW (UPGRADE 13) */}
            <div className="tool-viz">
               <h3>Pipeline Execution Trace</h3>
               <div className="trace-row">
                  {result.details.agent_activities?.map((a, i) => (
                    <div key={i} className="trace-item">
                       <span className="t-name">{a.agent}</span>
                       <span className="t-status">●</span>
                    </div>
                  ))}
               </div>
            </div>

            <div className="stats-grid">
               <div className="stat-card">
                  <label>NEURAL ACCURACY</label>
                  <div className="val">{Math.round(result.details.bert_score * 100)}%</div>
                  <div className="sub">Consistent with {result.final_verdict === 'Real' ? 'Fact' : 'Propaganda'}</div>
               </div>
               <div className="stat-card">
                  <label>EVIDENCE DENSITY</label>
                  <div className="val">{result.details.supporting}</div>
                  <div className="sub">Trusted news sources found</div>
               </div>
               <div className="stat-card">
                  <label>BIAS INTENSITY</label>
                  <div className="val neg">{Math.round(result.details.bias_penalty * 100)}%</div>
                  <div className="sub">Neural subjectivity penalty</div>
               </div>
            </div>

            {/* ATOMIC CLAIM DECOMPOSITION (UPGRADE 2) */}
            <div className="decomposition-section">
               <h3>Atomic Claim Verification</h3>
               <div className="claim-list">
                  {result.decomposed_claims?.map((c, i) => (
                    <div key={i} className="claim-pill">CLAIM {i+1}: {c.text}</div>
                  ))}
               </div>
            </div>

            <div className="evidence-timeline">
               <h3>Chain of Evidence</h3>
               <div className="timeline-items">
                  {result.details.article_results?.map((news, i) => (
                    <div key={i} className={`timeline-card ${news.label.toLowerCase()}`}>
                       <div className="t-meta">
                          <span className="source-domain">{new URL(news.url).hostname.replace('www.', '')}</span>
                          <span className="label-badge">{news.label}</span>
                       </div>
                       <h4>{news.title}</h4>
                       <p>{news.snippet}</p>
                       <a href={news.url} target="_blank" rel="noreferrer" className="view-link">VIEW SOURCE ↗</a>
                    </div>
                  ))}
               </div>
            </div>

            <div className="forensic-meta">
               <div className="meta-box">
                  <label>DETECTED STYLISTIC PATTERNS</label>
                  <div className="chips">
                    {result.metadata?.patterns.map((p, i) => <span key={i} className="badge alert">{p.replace('_', ' ')}</span>)}
                  </div>
               </div>
               <div className="meta-box">
                  <label>RELATIONAL ENTITIES (GRAPH)</label>
                  <div className="chips">
                    {result.metadata?.entities.map((e, i) => <span key={i} className="badge trust">{e}</span>)}
                  </div>
               </div>
            </div>

            {/* UNCERTAINTY AWARENESS (UPGRADE 6) */}
            <div className="uncertainty-box">
               <div className="u-header">What If We're Wrong? (Self-Reflection)</div>
               <ul>
                  {result.counter_points?.map((p, i) => <li key={i}>{p}</li>)}
               </ul>
            </div>

            {/* NEURAL CALIBRATION */}
            <div className={`calibration-section ${feedbackSent ? 'sent' : ''}`}>
               <div className="c-info">
                  <h4>Neural Calibration Hub</h4>
                  <p>Does this verdict seem incorrect? Manually flagging this report helps our engine learn from its mistakes.</p>
               </div>
               {!feedbackSent ? (
                 <div className="c-actions">
                    <button className="c-btn real" onClick={() => handleFeedback('Real')}>FLAG AS REAL NEWS</button>
                    <button className="c-btn fake" onClick={() => handleFeedback('Fake')}>FLAG AS DISINFORMATION</button>
                 </div>
               ) : (
                 <div className="c-success">NEURAL EXPERIENCE SYNCED. THANK YOU.</div>
               )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
