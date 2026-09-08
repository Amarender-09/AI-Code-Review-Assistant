import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL

function App() {
  const [mode, setMode] = useState('code')
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [repository, setRepository] = useState('')
  const [pullNumber, setPullNumber] = useState('')

  const [reviewResult, setReviewResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleReview = async () => {
    setError('')
    setReviewResult(null)

    if (mode === 'code') {
      if (!code.trim()) {
        setError('Please paste some code before starting the review.')
        return
      }

      setLoading(true)

      try {
        const response = await fetch(
          `${API_URL}/review/code`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              code,
              language,
            }),
          }
        )

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Code review failed.')
        }

        setReviewResult(data)
      } catch (error) {
        setError(error.message)
      } finally {
        setLoading(false)
      }

      return
    }

    if (!repository.trim() || !pullNumber.trim()) {
      setError(
        'Please enter both the repository and pull request number.'
      )
      return
    }

    const repositoryParts = repository.trim().split('/')

    if (
      repositoryParts.length !== 2 ||
      !repositoryParts[0] ||
      !repositoryParts[1]
    ) {
      setError('Repository must use the format owner/repository.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch(
        `${API_URL}/review/github`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            repository: repository.trim(),
            pull_number: Number(pullNumber),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'GitHub PR review failed.'
        )
      }

      setReviewResult(data)
    } catch (error) {
      setError(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">🤖</div>

          <div>
            <h1>AI Code Review Assistant</h1>
            <p>Find bugs. Improve code. Ship with confidence.</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Reviewer
        </div>
      </header>

      <main className="main-content">
        <section className="hero-section">
          <div className="hero-badge">
            AI-POWERED CODE ANALYSIS
          </div>

          <h2>
            Review your code with
            <span> AI intelligence.</span>
          </h2>

          <p className="hero-description">
            Detect bugs, security issues, performance problems,
            code-quality issues, and testing gaps before they
            reach production.
          </p>
        </section>

        <section className="review-card">
          <div className="mode-switcher">
            <button
              className={
                mode === 'code'
                  ? 'mode-button active'
                  : 'mode-button'
              }
              onClick={() => {
                setMode('code')
                setError('')
                setReviewResult(null)
              }}
              type="button"
            >
              <span>📋</span>
              Paste Code
            </button>

            <button
              className={
                mode === 'github'
                  ? 'mode-button active'
                  : 'mode-button'
              }
              onClick={() => {
                setMode('github')
                setError('')
                setReviewResult(null)
              }}
              type="button"
            >
              <span>🔗</span>
              GitHub PR
            </button>
          </div>

          {mode === 'code' ? (
            <div className="review-content">
              <div className="section-heading">
                <div>
                  <h3>Review Your Code</h3>
                  <p>
                    Paste your code below and let the AI analyze it.
                  </p>
                </div>

                <select
                  className="language-select"
                  value={language}
                  onChange={(event) =>
                    setLanguage(event.target.value)
                  }
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                </select>
              </div>

              <div className="code-editor">
                <div className="editor-header">
                  <div className="editor-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>

                  <span>
                    {language === 'python'
                      ? 'code.py'
                      : language === 'javascript'
                        ? 'code.js'
                        : 'code.ts'}
                  </span>
                </div>

                <textarea
                  value={code}
                  onChange={(event) =>
                    setCode(event.target.value)
                  }
                  placeholder={`# Paste your Python code here...

def add(a, b):
    return a - b`}
                  spellCheck="false"
                />
              </div>

              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}

              <div className="action-row">
                <span className="helper-text">
                  {code.length} characters
                </span>

                <button
                  className="review-button"
                  onClick={handleReview}
                  type="button"
                  disabled={loading}
                >
                  {loading
                    ? '⏳ Reviewing...'
                    : '🔍 Review Code'}
                </button>
              </div>

              {reviewResult && (
                <ReviewResults result={reviewResult} />
              )}
            </div>
          ) : (
            <div className="review-content">
              <div className="section-heading">
                <div>
                  <h3>Review a GitHub Pull Request</h3>
                  <p>
                    Enter a repository and pull request number
                    to start a review.
                  </p>
                </div>
              </div>

              <div className="github-form">
                <div className="form-group">
                  <label htmlFor="repository">
                    Repository
                  </label>

                  <input
                    id="repository"
                    type="text"
                    value={repository}
                    onChange={(event) =>
                      setRepository(event.target.value)
                    }
                    placeholder="owner/repository"
                  />

                  <span className="input-help">
                    Example: octocat/Hello-World
                  </span>
                </div>

                <div className="form-group">
                  <label htmlFor="pull-number">
                    Pull Request Number
                  </label>

                  <input
                    id="pull-number"
                    type="number"
                    min="1"
                    value={pullNumber}
                    onChange={(event) =>
                      setPullNumber(event.target.value)
                    }
                    placeholder="123"
                  />
                </div>
              </div>

              {error && (
                <div className="error-message">
                  {error}
                </div>
              )}

              <div className="action-row">
                <span className="helper-text">
                  Your GitHub PR will be analyzed by the review
                  engine.
                </span>

                <button
                  className="review-button"
                  onClick={handleReview}
                  type="button"
                  disabled={loading}
                >
                  {loading
                    ? '⏳ Reviewing...'
                    : '🔍 Review PR'}
                </button>
              </div>

              {reviewResult && (
                <ReviewResults result={reviewResult} />
              )}
            </div>
          )}
        </section>

        <section className="features">
          <div className="feature-card">
            <div className="feature-icon">🐛</div>
            <h3>Bug Detection</h3>
            <p>
              Find logical errors and potential bugs in your code.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔐</div>
            <h3>Security Analysis</h3>
            <p>
              Identify security risks and vulnerable coding
              patterns.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Performance</h3>
            <p>
              Detect inefficient code and performance bottlenecks.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🧪</div>
            <h3>Testing Insights</h3>
            <p>
              Discover missing tests and improve code reliability.
            </p>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>
          AI Code Review Assistant • Powered by AI + Static
          Analysis
        </p>
      </footer>
    </div>
  )
}


function ReviewResults({ result }) {
  const findings = result.findings || []
  const warnings = result.warnings || []

  return (
    <div className="results-section">
      <div className="results-header">
        <div>
          <h3>Review Results</h3>

          <p>
            {findings.length} finding
            {findings.length !== 1 ? 's' : ''} detected
          </p>
        </div>
      </div>

      {findings.length === 0 ? (
        <div className="no-findings">
          <h4>✅ No issues found</h4>

          <p>
            The review engine did not find any meaningful
            issues in this code.
          </p>
        </div>
      ) : (
        <div className="findings-list">
          {findings.map((finding) => (
            <div
              className="finding-card"
              key={finding.id}
            >
              <div className="finding-top">
                <span className="finding-title">
                  {finding.title}
                </span>

                <span
                  className={`severity ${finding.severity}`}
                >
                  {finding.severity.toUpperCase()}
                </span>
              </div>

              <div className="finding-meta">
                {finding.location?.file_path && (
                  <span>
                    📁 {finding.location.file_path}
                  </span>
                )}

                {finding.location?.start_line && (
                  <span>
                    📍 Line {finding.location.start_line}

                    {finding.location.end_line &&
                    finding.location.end_line !==
                      finding.location.start_line
                      ? `-${finding.location.end_line}`
                      : ''}
                  </span>
                )}

                <span>
                  🎯{' '}
                  {Math.round(
                    finding.confidence * 100
                  )}
                  % confidence
                </span>

                <span>
                  🤖 {finding.source}
                </span>
              </div>

              <p className="finding-description">
                {finding.description}
              </p>

              <div className="finding-detail">
                <strong>Why it matters</strong>
                <p>{finding.why_it_matters}</p>
              </div>

              <div className="finding-detail">
                <strong>Recommendation</strong>
                <p>{finding.recommendation}</p>
              </div>

              {finding.evidence && (
                <div className="finding-evidence">
                  <strong>Evidence</strong>

                  <code>
                    {finding.evidence}
                  </code>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {warnings.length > 0 && (
        <div className="warnings-section">
          <h4>⚠️ Review Warnings</h4>

          {warnings.map((warning, index) => (
            <p key={index}>{warning}</p>
          ))}
        </div>
      )}

      {result.publish_result && (
        <div className="publish-result">
          <strong>GitHub Review</strong>

          <p>
            The review was successfully processed for this
            Pull Request.
          </p>
        </div>
      )}
    </div>
  )
}


export default App