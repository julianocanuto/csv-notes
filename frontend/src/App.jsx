import React, { useState } from 'react'
import { Button, Input } from 'antd'
import NotesList from './components/NotesList'

function App() {
  const [inputValue, setInputValue] = useState('')
  const [activeRowId, setActiveRowId] = useState(null)

  const handleLoadNotes = () => {
    const trimmed = inputValue.trim()
    setActiveRowId(trimmed || null)
  }

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1>CSV Notes Manager v0.6.0</h1>

      <p style={{ marginBottom: '16px', color: '#555' }}>
        Browse every note in the system or filter by a specific row identifier.
      </p>

      <div style={{ marginBottom: '24px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <Input
          style={{ width: '260px' }}
          placeholder="Filter by Row ID"
          value={inputValue}
          onChange={event => setInputValue(event.target.value)}
          onPressEnter={handleLoadNotes}
          allowClear
        />
        <Button type="primary" onClick={handleLoadNotes}>
          Apply Filter
        </Button>
        <Button onClick={() => { setInputValue(''); setActiveRowId(null) }}>
          Clear Filter
        </Button>
      </div>

      <NotesList rowId={activeRowId} />
    </div>
  )
}

export default App
