import React, { useEffect, useState } from 'react'

function App() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/v1/health')
      .then(response => {
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`)
        }
        return response.json()
      })
      .then(data => setHealth(data))
      .catch(err => setError(err.message))
  }, [])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>CSV Notes Manager v0.5.0</h1>
      {error && <p style={{ color: 'red' }}>Error loading health status: {error}</p>}
      {health ? (
        <div>
          <p>Status: {health.status}</p>
          <p>Version: {health.version}</p>
          {health.database && <p>Database: {health.database}</p>}
        </div>
      ) : (
        !error && <p>Loading health information...</p>
      )}
    </div>
  )
}

export default App
