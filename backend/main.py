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
    
    try:
        # Connect to Hume AI
        try:
            hume_client = HumeAIClient()
            await hume_client.connect()
            print("✅ Hume AI client connected")
            
            # Start receiving messages from Hume AI in background
            receive_task = asyncio.create_task(hume_client.receive_messages())
            
        except Exception as e:
            print(f"⚠️ Warning: Could not connect to Hume AI: {e}")
            print("Continuing without Hume AI connection...")
        
        while True:
            # Receive message from client (can be text or bytes)
            message = await websocket.receive()
            
            if "text" in message:
                # Handle text messages
                data = message["text"]
                print(f"Received text message: {data}")
                # Echo the message back to the client
                await websocket.send_text(data)
                print(f"Echoed text message: {data}")
                
            elif "bytes" in message:
                # Handle binary audio data
                audio_data = message["bytes"]
                audio_size = len(audio_data)
                print(f"Received audio chunk: {audio_size} bytes")
                
                # Forward audio to Hume AI if connected
                if hume_client and hume_client.is_connected:
                    try:
                        await hume_client.send_audio(audio_data)
                    except Exception as e:
                        print(f"Error sending audio to Hume AI: {e}")
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    finally:
        # Cleanup: disconnect from Hume AI
        if receive_task:
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
        
        if hume_client:
            try:
                await hume_client.disconnect()
            except Exception as e:
                print(f"Error disconnecting from Hume AI: {e}")

