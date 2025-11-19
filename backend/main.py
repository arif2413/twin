from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio
from hume_client import HumeAIClient

# Load environment variables
load_dotenv()

app = FastAPI(title="Emotion-Aware Customer Service Assistant")

# Global Hume AI client instance (will be initialized per connection)
hume_clients = {}

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Emotion-Aware Customer Service Assistant API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "customer-service-assistant"}


@app.get("/test-hume")
async def test_hume_connection():
    """Test endpoint to verify Hume AI connection."""
    try:
        hume_client = HumeAIClient()
        await hume_client.connect()
        await hume_client.disconnect()
        return {
            "status": "success",
            "message": "Successfully connected to Hume AI"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect to Hume AI: {str(e)}"
        }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket client connected")
    
    # Initialize Hume AI client for this connection
    hume_client = None
    receive_task = None
    
    # Define callback to send transcriptions to frontend
    async def send_transcription_to_frontend(transcript_text: str):
        """Callback to send transcription to frontend via WebSocket."""
        try:
            transcript_message = {
                "type": "transcription",
                "text": transcript_text,
                "timestamp": asyncio.get_event_loop().time()
            }
            await websocket.send_json(transcript_message)
            print(f"📤 Sent transcript to frontend: {transcript_text}")
        except Exception as e:
            print(f"Error sending transcript to frontend: {e}")
    
    try:
        # Connect to Hume AI
        try:
            hume_client = HumeAIClient(on_transcription=send_transcription_to_frontend)
            await hume_client.connect()
            print("✅ Hume AI client connected")
            print(f"✅ Stream available: {hume_client.stream is not None}")
            print(f"✅ Is connected: {hume_client.is_connected}")
            
            # The receive task is already started in connect() as _receive_stream_messages
            # Get the task that was created
            receive_task = hume_client.receive_task
            if receive_task:
                print("✅ Message receiver task is running")
            else:
                print("⚠️  No receive task found, starting one...")
                receive_task = asyncio.create_task(hume_client.receive_messages())
            
        except Exception as e:
            print(f"⚠️ Warning: Could not connect to Hume AI: {e}")
            print("Continuing without Hume AI connection...")
        
        while True:
            try:
                # Receive message from client (can be text or bytes)
                message = await websocket.receive()
                
                if "text" in message:
                    # Handle text messages
                    data = message["text"]
                    print(f"Received text message: {data}")
                    # Echo the message back to the client
                    try:
                        await websocket.send_text(data)
                        print(f"Echoed text message: {data}")
                    except Exception as e:
                        print(f"Error sending echo: {e}")
                        break  # Connection likely closed
                    
                elif "bytes" in message:
                    # Handle binary audio data
                    audio_data = message["bytes"]
                    audio_size = len(audio_data)
                    
                    # Only log occasionally to avoid spam (every 50 chunks)
                    if not hasattr(websocket, '_audio_chunk_count'):
                        websocket._audio_chunk_count = 0
                    websocket._audio_chunk_count += 1
                    if websocket._audio_chunk_count % 50 == 0:
                        print(f"Received audio chunk #{websocket._audio_chunk_count}: {audio_size} bytes")
                    
                    # Forward audio to Hume AI if connected
                    if hume_client and hume_client.is_connected:
                        try:
                            await hume_client.send_audio(audio_data)
                        except Exception as e:
                            # Error is already handled in send_audio, just mark as disconnected
                            if hume_client:
                                hume_client.is_connected = False
                    else:
                        # Connection not available - log once
                        if not hasattr(websocket, '_connection_warned'):
                            print("⚠️  Hume AI not connected - audio chunks are being received but not processed")
                            websocket._connection_warned = True
                            
            except WebSocketDisconnect:
                print("WebSocket client disconnected")
                break  # Exit the loop when client disconnects
            except RuntimeError as e:
                # Handle "Cannot call receive once a disconnect message has been received"
                if "disconnect" in str(e).lower():
                    print("WebSocket connection closed")
                    break
                else:
                    raise  # Re-raise if it's a different RuntimeError
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected (outer handler)")
    finally:
        # Cleanup: disconnect from Hume AI
        print("🧹 Cleaning up Hume AI connection...")
        if receive_task:
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
        
        if hume_client:
            try:
                await hume_client.disconnect()
                print("✅ Hume AI connection closed")
            except Exception as e:
                print(f"⚠️  Error disconnecting from Hume AI: {e}")

