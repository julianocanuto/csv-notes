import React, { useEffect, useState } from 'react'
import { Card, Empty, Tag, Typography } from 'antd'

const STATUS_COLORS = {
  open: 'blue',
  'in progress': 'gold',
  resolved: 'green',
  closed: 'gray',
}

function NotesList({ rowId }) {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let isActive = true
    setLoading(true)
    setError(null)

    const endpoint =
      rowId || rowId === 0
        ? `/api/v1/notes/by-row/${encodeURIComponent(rowId)}`
        : '/api/v1/notes'

    fetch(endpoint)
      .then(async response => {
        if (!response.ok) {
          const message = await response.text()
          throw new Error(message || `Request failed with status ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        if (!isActive) return
        setNotes(data.notes || [])
      })
      .catch(err => {
        if (!isActive) return
        console.error('Failed to load notes', err)
        setError('Unable to load notes.')
        setNotes([])
      })
      .finally(() => {
        if (!isActive) return
        setLoading(false)
      })

    return () => {
      isActive = false
    }
  }, [rowId])

  const heading = rowId || rowId === 0 ? `Notes for Row ${rowId}` : 'All Notes'

  if (loading) {
    return <div>Loading notes...</div>
  }

  if (error) {
    return <Empty description={error} />
  }

  if (!notes.length) {
    return <Empty description="No notes yet" />
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <Typography.Title level={3} style={{ marginBottom: '16px' }}>
        {heading}
      </Typography.Title>
      {notes.map(note => {
        const status = note.status || 'Open'
        const colorKey = status.toLowerCase()
        const tagColor = STATUS_COLORS[colorKey] || 'blue'

        return (
          <Card key={note.note_id} style={{ marginBottom: '12px' }}>
            <Tag color={tagColor} style={{ textTransform: 'capitalize' }}>
              {status}
            </Tag>
            <div style={{ marginTop: '8px', whiteSpace: 'pre-wrap' }}>{note.note_text}</div>
            <div style={{ marginTop: '12px', fontSize: '12px', color: '#666' }}>
              Row ID: <strong>{note.row_id}</strong>
              {note.primary_key_value ? ` · Key: ${note.primary_key_value}` : ''}
            </div>
            {note.created_timestamp && (
              <div style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                {new Date(note.created_timestamp).toLocaleString()}
              </div>
            )}
          </Card>
        )
      })}
    </div>
  )
}

export default NotesList
