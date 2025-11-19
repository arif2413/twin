from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Emotion-Aware Customer Service Assistant")

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket client connected")
    
    try:
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
                # For now, just log the audio chunk
                # In later steps, this will be forwarded to Hume AI
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected")

