import React, { useState } from 'react'
import { Button, Input } from 'antd'
import NotesList from './components/NotesList'

function App() {
  const [inputValue, setInputValue] = useState('1')
  const [activeRowId, setActiveRowId] = useState('1')

  const handleLoadNotes = () => {
    const trimmed = inputValue.trim()
    setActiveRowId(trimmed || null)
  }

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1>CSV Notes Manager v0.6.0</h1>

      <div style={{ marginBottom: '24px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <Input
          style={{ width: '240px' }}
          placeholder="Enter Row ID"
          value={inputValue}
          onChange={event => setInputValue(event.target.value)}
          onPressEnter={handleLoadNotes}
          allowClear
        />
        <Button type="primary" onClick={handleLoadNotes} disabled={!inputValue.trim()}>
          Load Notes
        </Button>
      </div>

      <NotesList rowId={activeRowId} />
    </div>
  )
}

export default App
