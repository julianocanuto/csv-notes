import React, { useEffect, useMemo, useState } from 'react'
import { Card, Empty, Select, Space, Spin, Table, Typography, message } from 'antd'

function CsvImportsViewer({ onSelectRow }) {
  const [imports, setImports] = useState([])
  const [loadingImports, setLoadingImports] = useState(false)
  const [importsError, setImportsError] = useState(null)
  const [selectedImportId, setSelectedImportId] = useState(null)
  const [rows, setRows] = useState([])
  const [columns, setColumns] = useState([])
  const [loadingRows, setLoadingRows] = useState(false)
  const [rowsError, setRowsError] = useState(null)

  useEffect(() => {
    const fetchImports = async () => {
      setLoadingImports(true)
      setImportsError(null)
      try {
        const response = await fetch('/api/v1/csv/imports')
        if (!response.ok) {
          const messageText = await response.text()
          throw new Error(messageText || `Request failed with status ${response.status}`)
        }

        const data = await response.json()
        const fetchedImports = Array.isArray(data.imports) ? data.imports : []
        setImports(fetchedImports)

        if (fetchedImports.length) {
          setSelectedImportId(current => current ?? fetchedImports[0].import_id)
        } else {
          setSelectedImportId(null)
        }
      } catch (err) {
        console.error('Failed to load imports', err)
        setImportsError('Unable to load CSV imports.')
        message.error('Unable to load CSV imports.')
      } finally {
        setLoadingImports(false)
      }
    }

    fetchImports()
  }, [])

  useEffect(() => {
    const fetchRows = async () => {
      if (!selectedImportId) {
        setRows([])
        setColumns([])
        return
      }

      setLoadingRows(true)
      setRowsError(null)
      try {
        const response = await fetch(`/api/v1/csv/imports/${selectedImportId}/rows`)
        if (!response.ok) {
          const messageText = await response.text()
          throw new Error(messageText || `Request failed with status ${response.status}`)
        }

        const data = await response.json()
        const fetchedRows = Array.isArray(data.rows) ? data.rows : []
        const fetchedColumns = Array.isArray(data.columns) ? data.columns : []

        setRows(fetchedRows)
        setColumns(fetchedColumns)
      } catch (err) {
        console.error('Failed to load CSV rows', err)
        setRowsError('Unable to load CSV content for this import.')
        message.error('Unable to load CSV content for this import.')
        setRows([])
        setColumns([])
      } finally {
        setLoadingRows(false)
      }
    }

    fetchRows()
  }, [selectedImportId])

  const tableData = useMemo(() => {
    return rows.map(row => {
      const flattened = {
        key: row.row_id,
        rowId: row.row_id,
        primaryKey: row.primary_key_value || '',
        notesDetails: Array.isArray(row.notes) ? row.notes : [],
      }

      columns.forEach(columnName => {
        const value = row.data && Object.prototype.hasOwnProperty.call(row.data, columnName)
          ? row.data[columnName]
          : ''
        flattened[columnName] = value ?? ''
      })

      flattened.notesSummary = flattened.notesDetails
        .map(note => note.note_text?.trim())
        .filter(Boolean)
        .join('\n\n')

      return flattened
    })
  }, [rows, columns])

  const tableColumns = useMemo(() => {
    const dynamicColumns = columns.map(columnName => ({
      title: columnName,
      dataIndex: columnName,
      key: columnName,
      ellipsis: true,
      render: value => (value === null || value === undefined || value === '' ? <Typography.Text type="secondary">(blank)</Typography.Text> : value),
    }))

    return [
      {
        title: 'Row ID',
        dataIndex: 'rowId',
        key: 'rowId',
        width: 100,
        sorter: (a, b) => a.rowId - b.rowId,
      },
      {
        title: 'Primary Key',
        dataIndex: 'primaryKey',
        key: 'primaryKey',
        width: 160,
        ellipsis: true,
      },
      ...dynamicColumns,
      {
        title: 'Notes',
        dataIndex: 'notesSummary',
        key: 'notesSummary',
        ellipsis: true,
        render: (_, record) => {
          if (!record.notesDetails.length) {
            return <Typography.Text type="secondary">No notes</Typography.Text>
          }

          return (
            <div style={{ maxHeight: '220px', overflowY: 'auto' }}>
              {record.notesDetails.map(note => (
                <Typography.Paragraph
                  key={note.note_id}
                  style={{ marginBottom: '8px', whiteSpace: 'pre-wrap' }}
                >
                  {note.note_text}
                </Typography.Paragraph>
              ))}
            </div>
          )
        },
      },
    ]
  }, [columns])

  const handleRowClick = record => {
    if (!onSelectRow) {
      return
    }

    const identifier = record.primaryKey || record.rowId
    if (identifier) {
      onSelectRow(identifier)
    }
  }

  const importOptions = imports.map(item => ({
    label: `${item.filename} (${item.row_count} rows, PK: ${item.primary_key || 'n/a'})`,
    value: item.import_id,
  }))

  return (
    <Card title="Imported CSVs" style={{ marginTop: '24px' }}>
      {loadingImports ? (
        <div style={{ textAlign: 'center', padding: '24px 0' }}>
          <Spin />
        </div>
      ) : !imports.length ? (
        <Empty description={importsError || 'No CSV imports yet'} />
      ) : (
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Space wrap>
            <Typography.Text strong>Select Import:</Typography.Text>
            <Select
              style={{ minWidth: 260 }}
              value={selectedImportId}
              options={importOptions}
              onChange={value => setSelectedImportId(value)}
            />
          </Space>

          {loadingRows ? (
            <div style={{ textAlign: 'center', padding: '24px 0' }}>
              <Spin />
            </div>
          ) : rowsError ? (
            <Empty description={rowsError} />
          ) : !rows.length ? (
            <Empty description="No rows found for this import" />
          ) : (
            <Table
              dataSource={tableData}
              columns={tableColumns}
              scroll={{ x: true }}
              pagination={{ pageSize: 10, showSizeChanger: true }}
              onRow={record => ({
                onClick: () => handleRowClick(record),
                style: { cursor: onSelectRow ? 'pointer' : 'default' },
              })}
            />
          )}
        </Space>
      )}
    </Card>
  )
}

export default CsvImportsViewer
