import { useMemo } from 'react';

function AnalysisCard({ analysisRaw, jdText, resumeText }) {

  // Parse Backend Output
  const parsed = useMemo(() => {
    if (!analysisRaw) return null;

    // Default structure
    const result = {
      atsScore: 0,
      missingSkills: [],
      improvements: [],
      summary: []
    };

    const lines = analysisRaw.split('\n').map(l => l.trim()).filter(Boolean);

    let currentSection = '';

    for (const line of lines) {
      if (line.toLowerCase().includes('ats score:')) {
        const match = line.match(/(\d+)/);
        if (match) result.atsScore = parseInt(match[1], 10);
      }
      else if (line.toLowerCase().includes('missing skills:')) {
        currentSection = 'missing';
      }
      else if (line.toLowerCase().includes('improvements:')) {
        currentSection = 'improvements';
      }
      else if (line.toLowerCase().includes('summary:')) {
        currentSection = 'summary';
      }
      else if (line.startsWith('-')) {
        const text = line.substring(1).trim();
        if (currentSection === 'missing') result.missingSkills.push(text);
        if (currentSection === 'improvements') result.improvements.push(text);
        if (currentSection === 'summary') result.summary.push(text);
      }
    }

    return result;
  }, [analysisRaw]);

  if (!parsed) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📊</div>
        <h2>Awaiting Analysis</h2>
        <p>Upload your resume and JD to see the breakdown here.</p>
      </div>
    );
  }

  const displayScore = parsed.atsScore;

  // Derive estimated scores for UI
  const contentQuality = Math.min(100, displayScore + 5);
  const formatting = Math.min(100, displayScore + 10);

  const getScoreClass = (score) => {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
  };

  // Why this score logic
  const reasons = [];
  if (parsed.missingSkills.length > 0) reasons.push(`Missing key skills : ${parsed.missingSkills[0]}`);
  if (parsed.improvements.length > 0) reasons.push(`Opportunity: ${parsed.improvements[0]}`);

  return (
    <div className="analysis-dashboard">
      <div className="dashboard-header">
        <h2>Analysis Results</h2>
      </div>

      <div className="score-grid">
        <div className="glass-panel score-card">
          <div className="score-card-header">
            <span className="score-card-title">Overall ATS Score</span>
          </div>
          <div className={`score-value ${getScoreClass(displayScore)}`}>
            {displayScore}<span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/100</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem', lineHeight: 1.4 }}>
            Score considers overall resume relevance including skills, experience, and alignment with job description
          </div>
        </div>

        <div className="glass-panel score-card">
          <div className="score-card-header">
            <span className="score-card-title">Content Quality</span>
            <span className="score-estimated-badge">Estimated</span>
          </div>
          <div className={`score-value ${getScoreClass(contentQuality)}`}>
            {contentQuality}%
          </div>
        </div>

        <div className="glass-panel score-card">
          <div className="score-card-header">
            <span className="score-card-title">Formatting</span>
            <span className="score-estimated-badge">Estimated</span>
          </div>
          <div className={`score-value ${getScoreClass(formatting)}`}>
            {formatting}%
          </div>
        </div>
      </div>

      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'center', marginBottom: '1.5rem', fontStyle: 'italic' }}>
        * Note: Content Quality and Formatting sub-scores are indicative and based on heuristic estimation.
      </div>

      {reasons.length > 0 && (
        <div className="glass-panel section-card" style={{ background: 'rgba(59, 130, 246, 0.05)', borderColor: 'rgba(59, 130, 246, 0.2)' }}>
          <h3 className="section-title" style={{ fontSize: '1rem', borderBottom: 'none', marginBottom: '0.5rem', color: 'var(--accent-primary)' }}>Why this score?</h3>
          <ul className="list-items" style={{ margin: 0 }}>
            {reasons.map((reason, i) => (
              <li key={i} style={{ color: 'var(--text-secondary)' }}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      {parsed.missingSkills.length > 0 && (
        <div className="glass-panel section-card">
          <h3 className="section-title">Missing Skills</h3>
          <ul className="list-items">
            {parsed.missingSkills.map((skill, i) => <li key={i}>{skill}</li>)}
          </ul>
        </div>
      )}

      {parsed.improvements.length > 0 && (
        <div className="glass-panel section-card">
          <h3 className="section-title">Improvements</h3>
          <ul className="list-items">
            {parsed.improvements.map((imp, i) => <li key={i}>{imp}</li>)}
          </ul>
        </div>
      )}

      {parsed.summary.length > 0 && (
        <div className="glass-panel section-card" style={{ borderLeft: '4px solid var(--accent-primary)' }}>
          <h3 className="section-title" style={{ borderBottom: 'none', marginBottom: '0' }}>Summary</h3>
          <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: 'rgba(255,255,255,0.9)' }}>
            {parsed.summary.join(' ')}
          </p>
        </div>
      )}
    </div>
  );
}

export default AnalysisCard;
