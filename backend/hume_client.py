"""
Hume AI client wrapper for emotion detection and transcription.
This is a simplified version that will be refined based on actual SDK behavior.
"""

import os
import asyncio
from typing import Optional, Callable
from hume import AsyncHumeClient
import json


class HumeAIClient:
    """Wrapper for Hume AI streaming client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Hume AI client.
        
        Args:
            api_key: Hume AI API key. If None, will try to get from environment.
        """
        if api_key is None:
            api_key = os.getenv("HUME_API_KEY")
        
        if not api_key:
            raise ValueError("Hume API key is required. Set HUME_API_KEY environment variable.")
        
        self.api_key = api_key
        self.client: Optional[AsyncHumeClient] = None
        self.websocket: Optional[any] = None
        self.is_connected = False
        self.on_transcription: Optional[Callable] = None
        self.on_emotion: Optional[Callable] = None
        
    async def connect(self):
        """Establish connection to Hume AI."""
        try:
            self.client = AsyncHumeClient(api_key=self.api_key)
            
            # For now, just verify the client was created
            # The actual streaming connection will be implemented based on SDK documentation
            self.is_connected = True
            print("✅ Hume AI client initialized successfully")
            print("⚠️  Note: Full streaming connection will be implemented in Step 6")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing Hume AI client: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            self.is_connected = False
            raise
    
    async def disconnect(self):
        """Close connection to Hume AI."""
        if self.websocket:
            try:
                await self.websocket.close()
                print("Disconnected from Hume AI")
            except Exception as e:
                print(f"Error disconnecting from Hume AI: {e}")
        self.is_connected = False
        self.websocket = None
    
    async def send_audio(self, audio_bytes: bytes):
        """
        Send audio chunk to Hume AI.
        
        Args:
            audio_bytes: Audio data in bytes (PCM 16-bit format)
        """
        if not self.is_connected:
            print("Warning: Not connected to Hume AI. Cannot send audio.")
            return
        
        # Placeholder - will be implemented in Step 6
        print(f"📤 Audio chunk ready to send: {len(audio_bytes)} bytes")
    
    async def receive_messages(self):
        """
        Receive and process messages from Hume AI.
        This should be run in a separate task/thread.
        """
        # Placeholder - will be implemented in Step 6
        print("📥 Message receiver ready (will be implemented in Step 6)")
        await asyncio.sleep(1)  # Prevent immediate return
    
    async def _process_message(self, message: dict):
        """
        Process message from Hume AI and trigger appropriate callbacks.
        
        Args:
            message: Message dictionary from Hume AI
        """
        try:
            # Check for transcription (user_message events)
            if "user_message" in message:
                user_msg = message["user_message"]
                if "text" in user_msg:
                    transcript = user_msg["text"]
                    print(f"📝 Transcript: {transcript}")
                    if self.on_transcription:
                        await self.on_transcription(transcript)
            
            # Check for emotion scores
            if "user_message" in message:
                user_msg = message["user_message"]
                if "emotions" in user_msg:
                    emotions = user_msg["emotions"]
                    print(f"😊 Emotions detected: {len(emotions)} emotion scores")
                    if self.on_emotion:
                        await self.on_emotion(emotions)
                        
        except Exception as e:
            print(f"Error processing Hume AI message: {e}")
    
    def set_transcription_callback(self, callback: Callable):
        """Set callback function for transcription events."""
        self.on_transcription = callback
    
    def set_emotion_callback(self, callback: Callable):
        """Set callback function for emotion events."""
        self.on_emotion = callback
