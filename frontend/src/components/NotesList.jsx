import React, { useCallback, useEffect, useState } from 'react'
import {
  Button,
  Card,
  Empty,
  Form,
  Input,
  Modal,
  Select,
  Space,
  Tag as AntTag,
  Typography,
  message,
} from 'antd'

const STATUS_COLORS = {
  open: 'blue',
  'in progress': 'gold',
  resolved: 'green',
  closed: 'gray',
}

const STATUS_OPTIONS = [
  { value: 'Open', label: 'Open' },
  { value: 'In Progress', label: 'In Progress' },
  { value: 'Resolved', label: 'Resolved' },
  { value: 'Closed', label: 'Closed' },
]

const DEFAULT_STATUS = 'Open'

function NotesList({ rowId }) {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [editingNote, setEditingNote] = useState(null)
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form] = Form.useForm()

  const loadNotes = useCallback(async () => {
    const endpoint =
      rowId || rowId === 0
        ? `/api/v1/notes/by-row/${encodeURIComponent(rowId)}`
        : '/api/v1/notes'

    const response = await fetch(endpoint)
    if (!response.ok) {
      const messageText = await response.text()
      throw new Error(messageText || `Request failed with status ${response.status}`)
    }

    const data = await response.json()
    return Array.isArray(data.notes) ? data.notes : []
  }, [rowId])

  useEffect(() => {
    let isActive = true
    setLoading(true)
    setError(null)

    loadNotes()
      .then(fetchedNotes => {
        if (!isActive) return
        setNotes(fetchedNotes.map(note => ({ ...note, tags: note.tags || [] })))
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
  }, [loadNotes])

  const heading = rowId || rowId === 0 ? `Notes for Row ${rowId}` : 'All Notes'

  const openEditor = note => {
    setEditingNote(note)
    form.setFieldsValue({
      note_text: note.note_text,
      status: note.status || DEFAULT_STATUS,
      tags: note.tags || [],
    })
    setIsModalVisible(true)
  }

  const closeEditor = () => {
    setIsModalVisible(false)
    setEditingNote(null)
    form.resetFields()
  }

  const handleUpdate = async () => {
    try {
      const values = await form.validateFields()
      setSaving(true)

      const response = await fetch(`/api/v1/notes/${editingNote.note_id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          note_text: values.note_text,
          status: values.status,
          tags: values.tags || [],
        }),
      })

      if (!response.ok) {
        const messageText = await response.text()
        throw new Error(messageText || `Update failed with status ${response.status}`)
      }

      const data = await response.json()
      setNotes(current =>
        current.map(note => (note.note_id === data.note_id ? { ...note, ...data } : note)),
      )
      message.success('Note updated')
      closeEditor()
    } catch (err) {
      if (err?.errorFields) {
        return
      }
      console.error('Failed to update note', err)
      message.error('Unable to update note. Please try again.')
    } finally {
      setSaving(false)
    }
  }

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
        const status = note.status || DEFAULT_STATUS
        const colorKey = status.toLowerCase()
        const tagColor = STATUS_COLORS[colorKey] || 'blue'
        const created = note.created_timestamp
          ? new Date(note.created_timestamp).toLocaleString()
          : null
        const updated = note.updated_timestamp
          ? new Date(note.updated_timestamp).toLocaleString()
          : null
        const wasUpdated = created && updated && created !== updated

        return (
          <Card
            key={note.note_id}
            style={{ marginBottom: '12px' }}
            extra={
              <Button type="link" onClick={() => openEditor(note)}>
                Edit Note
              </Button>
            }
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <AntTag color={tagColor} style={{ textTransform: 'capitalize' }}>
                {status}
              </AntTag>
              <Typography.Text strong>Row ID: {note.row_id}</Typography.Text>
              {note.primary_key_value ? (
                <Typography.Text type="secondary">
                  Key: {note.primary_key_value}
                </Typography.Text>
              ) : null}
            </div>

            <Typography.Paragraph style={{ marginTop: '12px', whiteSpace: 'pre-wrap' }}>
              {note.note_text}
            </Typography.Paragraph>

            {note.tags?.length ? (
              <Space size={[0, 8]} wrap style={{ marginTop: '4px' }}>
                {note.tags.map(tag => (
                  <AntTag key={tag} color="geekblue">
                    {tag}
                  </AntTag>
                ))}
              </Space>
            ) : null}

            {(created || updated) && (
              <div style={{ fontSize: '12px', color: '#999', marginTop: '12px' }}>
                {created ? `Created: ${created}` : null}
                {wasUpdated ? ` · Updated: ${updated}` : null}
              </div>
            )}
          </Card>
        )
      })}

      <Modal
        open={isModalVisible}
        onCancel={closeEditor}
        onOk={handleUpdate}
        confirmLoading={saving}
        title={editingNote ? `Edit Note #${editingNote.note_id}` : 'Edit Note'}
        okText="Save Changes"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            label="Note Text"
            name="note_text"
            rules={[{ required: true, message: 'Note text is required' }]}
          >
            <Input.TextArea rows={4} placeholder="Update the note details" />
          </Form.Item>
          <Form.Item
            label="Status"
            name="status"
            rules={[{ required: true, message: 'Status is required' }]}
          >
            <Select options={STATUS_OPTIONS} />
          </Form.Item>
          <Form.Item label="Tags" name="tags">
            <Select
              mode="tags"
              tokenSeparators={[',']}
              placeholder="Add tags"
              style={{ width: '100%' }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default NotesList
