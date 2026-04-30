cat > frontend/src/App.jsx <<'EOF'
import React, { useEffect, useState } from 'react'

export default function App() {
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [studentId, setStudentId] = useState('')

  const loadData = async () => {
    const res = await fetch('/api/data')
    const data = await res.json()
    setItems(data)
  }

  useEffect(() => {
    loadData()
  }, [])

  const addItem = async (e) => {
    e.preventDefault()

    await fetch('/api/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, student_id: studentId })
    })

    setName('')
    setStudentId('')
    loadData()
  }

  const deleteItem = async (id) => {
    await fetch(`/api/data/${id}`, {
      method: 'DELETE'
    })

    loadData()
  }

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial' }}>
      <h1>Student List</h1>

      <form onSubmit={addItem} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Student name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="text"
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          style={{ marginLeft: '10px' }}
        />

        <button type="submit" style={{ marginLeft: '10px' }}>
          Add
        </button>
      </form>

      <ul>
        {items.map((item) => (
          <li key={item.id} style={{ marginBottom: '10px' }}>
            {item.name} - {item.student_id}
            <button onClick={() => deleteItem(item.id)} style={{ marginLeft: '10px' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
EOF
