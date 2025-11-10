import React, { useState } from 'react'
import { Button, Input, Typography } from 'antd'
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
      <Typography.Title level={2} style={{ marginBottom: '8px' }}>
        CSV Notes Manager v1.0.0
      </Typography.Title>

      <Typography.Paragraph style={{ marginBottom: '16px' }}>
        Browse, tag, and edit notes across every CSV import or focus on a specific row
        identifier to manage detailed follow-up work.
      </Typography.Paragraph>

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
