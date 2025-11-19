import React from 'react'

function ConnectionStatus({ isConnected }) {
  return (
    <div
      style={{
        padding: '10px',
        margin: '10px 0',
        borderRadius: '4px',
        backgroundColor: isConnected ? '#d4edda' : '#f8d7da',
        color: isConnected ? '#155724' : '#721c24',
        border: `1px solid ${isConnected ? '#c3e6cb' : '#f5c6cb'}`,
        display: 'inline-block',
      }}
    >
      <strong>WebSocket Status:</strong>{' '}
      {isConnected ? (
        <span style={{ color: '#28a745' }}>● Connected</span>
      ) : (
        <span style={{ color: '#dc3545' }}>● Disconnected</span>
      )}
    </div>
  )
}

export default ConnectionStatus

