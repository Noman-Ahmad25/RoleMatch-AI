import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [resume, setResume] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleClear = () => {
    setResume('')
    setResult(null)
    setError('')
  }
  const handlePredict = async () => {
    if (!resume.trim()) return
    
    setLoading(true)
    setError('')
    setResult(null)

    try {
      // Connect to your local Python Server
      const response = await axios.post('https://rolematch-ai.onrender.com/predict', {
        resume: resume
      })
      
      setResult(response.data)
    } catch (err) {
      setError("Failed to connect to AI server. Please try again later.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>Role Match AI</h1>
        <p>Powered by NLP & Logistic Regression</p>
      </header>

      <div className="card">
        <textarea 
          placeholder="Paste candidate resume or job description here..."
          value={resume}
          onChange={(e) => setResume(e.target.value)}
          rows="8"
        />

       <div style={{ display: 'flex', gap: '10px' }}>
  <button onClick={handlePredict} disabled={loading || !resume}>
    {loading ? 'Analyzing...' : 'Predict Role'}
  </button>
  
  <button 
    onClick={handleClear} 
    style={{ backgroundColor: '#64748b' }} 
    disabled={!resume && !result}
  >
    Clear
  </button>
</div>

        {error && <div className="error">{error}</div>}

        {result && (
          
            parseFloat(result.confidence) < 30 ? (
      <p style={{ color: 'red' }}>
        <strong>⚠️ No matching role found.</strong> 
        <br/>(Confidence too low: {result.confidence})
      </p>
    ):
            <div className="result-box">
            <h3>Predicted Role:</h3>
            <h2 className="role-title">{result.role}</h2>
            
            <div className="progress-bar-bg">
              <div 
                className="progress-bar-fill" 
                style={{width: `${result.confidence}%`}}
              ></div>
            </div>
            <p className="confidence">Confidence: {result.confidence}%</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
