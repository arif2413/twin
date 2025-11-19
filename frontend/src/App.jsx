import React, { useState, useEffect, useRef } from 'react'
import WebSocketClient from './utils/websocket'
import ConnectionStatus from './components/ConnectionStatus'
import AudioCapture from './components/AudioCapture'
import Transcript from './components/Transcript'
import useAudioCapture from './hooks/useAudioCapture'

function App() {
  const [isConnected, setIsConnected] = useState(false)
  const [messages, setMessages] = useState([])
  const [transcripts, setTranscripts] = useState([])
  const wsClientRef = useRef(null)
  
  // Audio capture hook - will be updated when WebSocket connects
  const {
    isCapturing,
    permissionStatus,
    error: audioError,
    startCapture,
    stopCapture,
    setWsClient,
  } = useAudioCapture()

  useEffect(() => {
    // Initialize WebSocket client
    const wsUrl = 'ws://localhost:8000/ws'
    wsClientRef.current = new WebSocketClient(wsUrl)

    // Set up event listeners
    wsClientRef.current.on('open', () => {
      setIsConnected(true)
      console.log('WebSocket connection opened')
      
      // Update audio capture hook with WebSocket client
      if (setWsClient) {
        setWsClient(wsClientRef.current)
      }
      
      // Send a test message after connection
      setTimeout(() => {
        const testMessage = 'Hello from frontend!'
        wsClientRef.current.send(testMessage)
        setMessages((prev) => [...prev, { type: 'sent', text: testMessage }])
      }, 500)
    })

    wsClientRef.current.on('close', () => {
      setIsConnected(false)
      console.log('WebSocket connection closed')
    })

    wsClientRef.current.on('message', (data) => {
      console.log('Received message:', data)
      
      // Skip binary messages (ArrayBuffer) - we only expect text/JSON
      if (data instanceof ArrayBuffer) {
        console.log('Received binary message (ignoring):', data.byteLength, 'bytes')
        return
      }
      
      // Try to parse as JSON (for transcription messages)
      try {
        const parsed = JSON.parse(data)
        console.log('Parsed JSON message:', parsed)
        if (parsed.type === 'transcription') {
          // Handle transcription message
          console.log('📝 Received transcription:', parsed.text)
          setTranscripts((prev) => [
            ...prev,
            {
              text: parsed.text,
              timestamp: parsed.timestamp || Date.now(),
            },
          ])
          return
        }
      } catch (e) {
        // Not JSON, treat as regular text message
        console.log('Not JSON, treating as text:', data)
      }
      
      // Handle regular text messages
      setMessages((prev) => [...prev, { type: 'received', text: data }])
    })

    wsClientRef.current.on('error', (error) => {
      console.error('WebSocket error:', error)
    })

    // Connect to WebSocket
    wsClientRef.current.connect()

    // Cleanup on unmount
    return () => {
      if (wsClientRef.current) {
        wsClientRef.current.close()
      }
    }
  }, [])

  const sendTestMessage = () => {
    if (wsClientRef.current && isConnected) {
      const message = `Test message at ${new Date().toLocaleTimeString()}`
      wsClientRef.current.send(message)
      setMessages((prev) => [...prev, { type: 'sent', text: message }])
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Emotion-Aware Customer Service Assistant</h1>
      <ConnectionStatus isConnected={isConnected} />
      
      <div style={{ marginTop: '20px' }}>
        <button
          onClick={sendTestMessage}
          disabled={!isConnected}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: isConnected ? '#007bff' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isConnected ? 'pointer' : 'not-allowed',
          }}
        >
          Send Test Message
        </button>
      </div>

      <AudioCapture
        isCapturing={isCapturing}
        permissionStatus={permissionStatus}
        error={audioError}
        onStart={startCapture}
        onStop={stopCapture}
      />

      <Transcript transcripts={transcripts} />

      <div style={{ marginTop: '20px' }}>
        <h3>Messages:</h3>
        <div
          style={{
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '10px',
            maxHeight: '300px',
            overflowY: 'auto',
            backgroundColor: '#f9f9f9',
          }}
        >
          {messages.length === 0 ? (
            <p style={{ color: '#666' }}>No messages yet...</p>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  marginBottom: '10px',
                  padding: '8px',
                  backgroundColor: msg.type === 'sent' ? '#e3f2fd' : '#f1f8e9',
                  borderRadius: '4px',
                }}
              >
                <strong>{msg.type === 'sent' ? 'Sent' : 'Received'}:</strong>{' '}
                {msg.text}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default App

