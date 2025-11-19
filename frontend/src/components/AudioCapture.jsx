import React from 'react'

function AudioCapture({ isCapturing, permissionStatus, error, onStart, onStop }) {
  const getStatusColor = () => {
    if (error || permissionStatus === 'denied' || permissionStatus === 'error') {
      return '#dc3545' // Red
    }
    if (isCapturing) {
      return '#28a745' // Green
    }
    if (permissionStatus === 'granted') {
      return '#17a2b8' // Blue
    }
    return '#6c757d' // Gray
  }

  const getStatusText = () => {
    if (error) {
      return 'Error'
    }
    if (permissionStatus === 'denied') {
      return 'Permission Denied'
    }
    if (permissionStatus === 'error') {
      return 'Error'
    }
    if (isCapturing) {
      return 'Microphone Active'
    }
    if (permissionStatus === 'granted') {
      return 'Ready'
    }
    return 'Not Started'
  }

  return (
    <div
      style={{
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        marginTop: '20px',
        backgroundColor: '#f9f9f9',
      }}
    >
      <h3 style={{ marginTop: 0 }}>Audio Capture</h3>
      
      <div style={{ marginBottom: '15px' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            padding: '10px 15px',
            borderRadius: '4px',
            backgroundColor: getStatusColor() + '20',
            border: `2px solid ${getStatusColor()}`,
          }}
        >
          <span
            style={{
              display: 'inline-block',
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor: getStatusColor(),
              marginRight: '10px',
              animation: isCapturing ? 'pulse 1.5s ease-in-out infinite' : 'none',
            }}
          />
          <strong style={{ color: getStatusColor() }}>{getStatusText()}</strong>
        </div>
      </div>

      {error && (
        <div
          style={{
            padding: '10px',
            marginBottom: '15px',
            backgroundColor: '#f8d7da',
            color: '#721c24',
            border: '1px solid #f5c6cb',
            borderRadius: '4px',
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {permissionStatus === 'denied' && (
        <div
          style={{
            padding: '10px',
            marginBottom: '15px',
            backgroundColor: '#fff3cd',
            color: '#856404',
            border: '1px solid #ffeaa7',
            borderRadius: '4px',
          }}
        >
          <strong>Permission Denied:</strong> Please allow microphone access in your browser settings and refresh the page.
        </div>
      )}

      <div>
        {!isCapturing ? (
          <button
            onClick={onStart}
            disabled={permissionStatus === 'denied'}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: permissionStatus === 'denied' ? '#6c757d' : '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: permissionStatus === 'denied' ? 'not-allowed' : 'pointer',
            }}
          >
            Start Audio Capture
          </button>
        ) : (
          <button
            onClick={onStop}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Stop Audio Capture
          </button>
        )}
      </div>

      <style>
        {`
          @keyframes pulse {
            0%, 100% {
              opacity: 1;
            }
            50% {
              opacity: 0.5;
            }
          }
        `}
      </style>
    </div>
  )
}

export default AudioCapture

