import React from 'react'

function Transcript({ transcripts }) {
  return (
    <div
      style={{
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        marginTop: '20px',
        backgroundColor: '#f9f9f9',
        maxHeight: '400px',
        overflowY: 'auto',
      }}
    >
      <h3 style={{ marginTop: 0, marginBottom: '15px' }}>Live Transcript</h3>
      
      {transcripts.length === 0 ? (
        <p style={{ color: '#666', fontStyle: 'italic' }}>
          Start speaking to see transcriptions appear here...
        </p>
      ) : (
        <div>
          {transcripts.map((transcript, index) => (
            <div
              key={index}
              style={{
                marginBottom: '10px',
                padding: '10px',
                backgroundColor: '#fff',
                borderRadius: '4px',
                border: '1px solid #e0e0e0',
              }}
            >
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
                {new Date(transcript.timestamp).toLocaleTimeString()}
              </div>
              <div style={{ fontSize: '16px', color: '#333' }}>{transcript.text}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Transcript

