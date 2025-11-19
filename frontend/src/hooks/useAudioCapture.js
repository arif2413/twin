import { useState, useEffect, useRef, useCallback } from 'react'

function useAudioCapture() {
  const [isCapturing, setIsCapturing] = useState(false)
  const [permissionStatus, setPermissionStatus] = useState('prompt') // 'prompt', 'granted', 'denied', 'error'
  const [error, setError] = useState(null)
  const streamRef = useRef(null)
  const audioContextRef = useRef(null)
  const processorNodeRef = useRef(null)
  const isCapturingRef = useRef(false)
  const wsClientRef = useRef(null)
  const audioConfigRef = useRef({
    sampleRate: 16000, // Target sample rate
    channels: 1, // Mono
    bufferSize: 4096, // Buffer size for processing
  })
  
  const setWsClient = useCallback((wsClient) => {
    wsClientRef.current = wsClient
  }, [])

  const startCapture = useCallback(async () => {
    try {
      setError(null)
      
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })

      streamRef.current = stream
      setPermissionStatus('granted')
      setIsCapturing(true)
      isCapturingRef.current = true

      // Create AudioContext for audio processing
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      
      // Create ScriptProcessorNode for audio chunk processing
      // Note: ScriptProcessorNode is deprecated but widely supported
      // AudioWorklet would be preferred but requires separate file
      const bufferSize = audioConfigRef.current.bufferSize
      processorNodeRef.current = audioContextRef.current.createScriptProcessor(
        bufferSize,
        1, // Input channels
        1  // Output channels
      )

      // Process audio chunks
      processorNodeRef.current.onaudioprocess = (event) => {
        if (!isCapturingRef.current) return

        const inputBuffer = event.inputBuffer
        const inputData = inputBuffer.getChannelData(0) // Get mono channel

        // Convert Float32Array to Int16Array (PCM format)
        const int16Array = new Int16Array(inputData.length)
        for (let i = 0; i < inputData.length; i++) {
          // Clamp and convert to 16-bit integer
          const s = Math.max(-1, Math.min(1, inputData[i]))
          int16Array[i] = s < 0 ? s * 0x8000 : s * 0x7FFF
        }

        // Send audio chunk via WebSocket if connected
        if (wsClientRef.current && wsClientRef.current.isConnected()) {
          wsClientRef.current.send(int16Array.buffer) // Send as ArrayBuffer (binary)
        }
      }

      // Connect audio nodes
      source.connect(processorNodeRef.current)
      processorNodeRef.current.connect(audioContextRef.current.destination)
      
      console.log('Audio capture started')
      console.log('Audio settings:', {
        sampleRate: audioContextRef.current.sampleRate,
        channels: stream.getAudioTracks()[0]?.getSettings(),
        bufferSize: bufferSize,
      })

      return stream
    } catch (err) {
      console.error('Error accessing microphone:', err)
      setError(err.message)
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setPermissionStatus('denied')
        setError('Microphone permission denied. Please allow microphone access in your browser settings.')
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setPermissionStatus('error')
        setError('No microphone found. Please connect a microphone and try again.')
      } else {
        setPermissionStatus('error')
        setError(`Error accessing microphone: ${err.message}`)
      }
      
      setIsCapturing(false)
      throw err
    }
  }, [])

  const stopCapture = useCallback(() => {
    // Disconnect audio nodes
    if (processorNodeRef.current) {
      processorNodeRef.current.disconnect()
      processorNodeRef.current = null
    }

    if (streamRef.current) {
      // Stop all tracks
      streamRef.current.getTracks().forEach((track) => {
        track.stop()
      })
      streamRef.current = null
    }

    if (audioContextRef.current) {
      audioContextRef.current.close()
      audioContextRef.current = null
    }

    setIsCapturing(false)
    isCapturingRef.current = false
    console.log('Audio capture stopped')
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCapture()
    }
  }, [stopCapture])

  // Check permission status on mount
  useEffect(() => {
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions
        .query({ name: 'microphone' })
        .then((result) => {
          if (result.state === 'granted') {
            setPermissionStatus('granted')
          } else if (result.state === 'denied') {
            setPermissionStatus('denied')
          }
        })
        .catch((err) => {
          console.warn('Permission query not supported:', err)
        })
    }
  }, [])

  return {
    isCapturing,
    permissionStatus,
    error,
    startCapture,
    stopCapture,
    setWsClient,
    stream: streamRef.current,
    audioContext: audioContextRef.current,
  }
}

export default useAudioCapture

