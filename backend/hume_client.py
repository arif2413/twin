"""
Hume AI client wrapper for emotion detection and transcription.
Uses EVI (Empathic Voice Interface) for streaming transcription.
Based on Hume AI documentation: https://dev.hume.ai/intro
"""

import os
import asyncio
from typing import Optional, Callable
from hume import AsyncHumeClient
from hume.empathic_voice.types.audio_input import AudioInput
from hume.empathic_voice.types.session_settings import SessionSettings
from hume.empathic_voice.types.audio_configuration import AudioConfiguration
import json
import base64


class HumeAIClient:
    """Wrapper for Hume AI streaming client using EVI."""
    
    def __init__(self, api_key: Optional[str] = None, on_transcription: Optional[Callable] = None):
        """
        Initialize Hume AI client.
        
        Args:
            api_key: Hume AI API key. If None, will try to get from environment.
            on_transcription: Callback function for transcription events.
        """
        if api_key is None:
            api_key = os.getenv("HUME_API_KEY")
        
        if not api_key:
            raise ValueError("Hume API key is required. Set HUME_API_KEY environment variable.")
        
        self.api_key = api_key
        self.client: Optional[AsyncHumeClient] = None
        self.stream = None
        self._stream_context = None  # Store context manager for cleanup
        self.is_connected = False
        self.on_transcription: Optional[Callable] = on_transcription
        self.on_emotion: Optional[Callable] = None
        self.receive_task = None
        
    async def connect(self):
        """Establish WebSocket connection to Hume AI EVI."""
        try:
            self.client = AsyncHumeClient(api_key=self.api_key)
            
            # Connect to EVI streaming API using chat.connect
            # connect() returns an async context manager, so we use async with
            try:
                # Enter the async context manager
                stream_context = self.client.empathic_voice.chat.connect()
                self.stream = await stream_context.__aenter__()
                self._stream_context = stream_context  # Store for cleanup
                print("✅ Connected to Hume AI EVI streaming API")
            except Exception as e:
                print(f"⚠️  Error connecting to EVI stream: {e}")
                # Try connect_with_callbacks as alternative
                try:
                    stream_context = self.client.empathic_voice.chat.connect_with_callbacks()
                    self.stream = await stream_context.__aenter__()
                    self._stream_context = stream_context
                    print("✅ Connected to Hume AI EVI using connect_with_callbacks")
                except Exception as e2:
                    print(f"⚠️  Alternative connection also failed: {e2}")
                    self.stream = None
                    self._stream_context = None
            
            self.is_connected = True
            print("✅ Hume AI client initialized successfully")
            
            # Configure session settings with audio format (16kHz, mono, linear16)
            if self.stream:
                try:
                    # Configure audio settings: 16kHz, mono, linear16 encoding
                    audio_config = AudioConfiguration(
                        channels=1,
                        encoding="linear16",
                        sample_rate=16000
                    )
                    
                    session_settings = SessionSettings(
                        type="session_settings",
                        audio=audio_config
                    )
                    
                    # Send session settings to configure the stream
                    if hasattr(self.stream, 'send_session_settings'):
                        await self.stream.send_session_settings(session_settings)
                        print("✅ Sent session settings (16kHz, mono, linear16)")
                    elif hasattr(self.stream, 'send'):
                        await self.stream.send(session_settings)
                        print("✅ Sent session settings via send()")
                    else:
                        print("⚠️  Could not find method to send session settings")
                except Exception as e:
                    print(f"⚠️  Could not send session settings: {e}")
                    # Continue anyway - some setups might not need explicit settings
            
            # Start receiving messages if stream is available
            if self.stream:
                # Use start_listening() to begin receiving messages (it's a coroutine)
                if hasattr(self.stream, 'start_listening'):
                    try:
                        # Check if it's a coroutine
                        if asyncio.iscoroutinefunction(self.stream.start_listening):
                            await self.stream.start_listening()
                        else:
                            self.stream.start_listening()
                        print("✅ Started listening on stream")
                    except Exception as e:
                        print(f"⚠️  Could not start_listening: {e}")
                # Also start the receive task
                self.receive_task = asyncio.create_task(self._receive_stream_messages())
            
            return True
            
        except Exception as e:
            print(f"❌ Error connecting to Hume AI: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            self.is_connected = False
            # Don't raise - allow connection to continue without Hume for now
            return False
    
    async def disconnect(self):
        """Close connection to Hume AI."""
        if self.receive_task:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                pass
        
        # Exit the async context manager properly
        if self._stream_context:
            try:
                await self._stream_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"Error exiting stream context: {e}")
        elif self.stream:
            try:
                if hasattr(self.stream, 'close'):
                    await self.stream.close()
            except Exception as e:
                print(f"Error closing stream: {e}")
        
        self.is_connected = False
        self.stream = None
        self._stream_context = None
        print("Disconnected from Hume AI")
    
    async def send_audio(self, audio_bytes: bytes):
        """
        Send audio chunk to Hume AI EVI stream.
        
        Args:
            audio_bytes: Audio data in bytes (PCM 16-bit format)
        """
        if not self.is_connected or not self.stream:
            return
        
        try:
            # Convert audio bytes to base64 string (as required by AudioInput)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Create AudioInput object with data field (base64 string) and type
            audio_input = AudioInput(
                data=audio_base64,
                type="audio_input"
            )
            
            # Send audio to EVI stream using send_audio_input method
            await self.stream.send_audio_input(audio_input)
            print(f"📤 Sent audio chunk to Hume: {len(audio_bytes)} bytes")
        except Exception as e:
            error_str = str(e).lower()
            
            # Check if connection was closed due to policy violation (too many chats)
            if "policy violation" in error_str or "too_many_active_chats" in error_str:
                print(f"⚠️  Hume AI connection closed: Account has reached the 5 concurrent chat limit")
                print(f"⚠️  Stopping audio transmission. Please wait 2-3 minutes for old sessions to timeout.")
                self.is_connected = False
                return  # Don't print full traceback for this expected error
            
            # Check if connection was closed for any reason
            if "connectionclosed" in error_str or "connection closed" in error_str:
                print(f"⚠️  Hume AI connection was closed. Marking as disconnected.")
                self.is_connected = False
                return
            
            # For other errors, log with traceback
            print(f"❌ Error sending audio to Hume AI: {e}")
            import traceback
            traceback.print_exc()
    
    async def _receive_stream_messages(self):
        """
        Receive and process messages from Hume AI EVI stream.
        This runs in a background task.
        """
        if not self.stream:
            print("⚠️  No stream available for receiving messages")
            return
        
        print("📥 Started listening for messages from Hume AI...")
        try:
            # Use recv method to receive messages from stream
            while self.is_connected:
                try:
                    response = await self.stream.recv()
                    print(f"📨 Received response from Hume AI stream")
                    await self._process_message(response)
                except asyncio.CancelledError:
                    print("📥 Message receiver cancelled")
                    break
                except Exception as e:
                    error_str = str(e).lower()
                    if "cancelled" not in error_str and "closed" not in error_str:
                        print(f"❌ Error receiving message: {e}")
                        import traceback
                        traceback.print_exc()
                    break
                
        except asyncio.CancelledError:
            print("📥 Stream message receiver cancelled")
        except Exception as e:
            print(f"❌ Error in message receiver loop: {e}")
            import traceback
            traceback.print_exc()
            self.is_connected = False
    
    async def _process_message(self, message):
        """
        Process message from Hume AI and trigger appropriate callbacks.
        
        Args:
            message: Message from Hume AI EVI stream
        """
        try:
            # Convert message to dict if it's not already
            if hasattr(message, 'model_dump'):
                message_dict = message.model_dump()
            elif hasattr(message, 'dict'):
                message_dict = message.dict()
            elif isinstance(message, dict):
                message_dict = message
            else:
                # Try to parse as JSON string
                try:
                    message_dict = json.loads(str(message))
                except:
                    message_dict = {"raw": str(message)}
            
            # Debug: Log message type and full structure (first few messages for debugging)
            msg_type = message_dict.get("type", "unknown")
            print(f"🔍 Received message type: {msg_type}")
            
            # Print full message structure for first few messages to debug
            if not hasattr(self, '_debug_message_count'):
                self._debug_message_count = 0
            if self._debug_message_count < 3:
                print(f"📋 Full message structure ({self._debug_message_count + 1}):")
                print(json.dumps(message_dict, indent=2, default=str))
                self._debug_message_count += 1
            
            # According to Hume AI EVI Chat API documentation:
            # UserMessage has structure:
            # {
            #   "type": "user_message",
            #   "message": {
            #     "content": "transcription text here",
            #     "role": "user"
            #   },
            #   "models": { ... emotion scores ... },
            #   "interim": false,
            #   "from_text": false,
            #   "time": { "begin": ..., "end": ... }
            # }
            
            # Check for error messages first
            if msg_type == "error":
                error_code = message_dict.get("code", "unknown")
                error_message = message_dict.get("message", "Unknown error")
                error_slug = message_dict.get("slug", "")
                
                print(f"❌ Hume AI Error ({error_code}): {error_message}")
                
                # Handle "too_many_active_chats" error
                if error_slug == "too_many_active_chats":
                    print("⚠️  Account has reached the maximum number of active chats (5).")
                    print("⚠️  Please close other active sessions or wait for them to timeout.")
                    # Mark as not connected so we don't try to send audio
                    self.is_connected = False
                
                return  # Don't process errors as transcriptions
            
            # Check for user_message type (transcriptions)
            if msg_type == "user_message":
                # Extract transcription from message.content
                if "message" in message_dict and isinstance(message_dict["message"], dict):
                    message_obj = message_dict["message"]
                    if "content" in message_obj and message_obj["content"]:
                        transcript = message_obj["content"]
                        is_interim = message_dict.get("interim", False)
                        
                        # Only process non-interim (final) transcriptions, or process both
                        # For now, process all transcriptions
                        print(f"📝 Transcript{' (interim)' if is_interim else ''}: {transcript}")
                        await self.process_transcription(transcript)
                
                # Extract emotion scores from models field
                if "models" in message_dict:
                    models = message_dict["models"]
                    # Models contain prosody/emotion data
                    if isinstance(models, dict):
                        # Look for prosody or emotion scores
                        for model_name, model_data in models.items():
                            if "emotions" in model_data or "scores" in model_data:
                                emotions = model_data.get("emotions") or model_data.get("scores", {})
                                print(f"😊 Emotions detected from {model_name}: {len(emotions) if isinstance(emotions, dict) else 0} emotion scores")
                                if self.on_emotion:
                                    if asyncio.iscoroutinefunction(self.on_emotion):
                                        await self.on_emotion(emotions)
                                    else:
                                        self.on_emotion(emotions)
            
            # Check for assistant_message (for completeness, though we focus on user transcriptions)
            elif msg_type == "assistant_message":
                if "message" in message_dict and isinstance(message_dict["message"], dict):
                    message_obj = message_dict["message"]
                    if "content" in message_obj:
                        print(f"🤖 Assistant message: {message_obj['content'][:100]}...")
                    
        except Exception as e:
            print(f"Error processing Hume AI message: {e}")
            import traceback
            traceback.print_exc()
    
    async def receive_messages(self):
        """
        Receive and process messages from Hume AI.
        This calls _receive_stream_messages which does the actual work.
        """
        # The actual message receiving is done by _receive_stream_messages
        # which is started as a task in connect(). This method is kept for compatibility.
        # If _receive_stream_messages wasn't started, start it here
        if self.stream and self.is_connected:
            if not self.receive_task or self.receive_task.done():
                print("📥 Starting message receiver task...")
                await self._receive_stream_messages()
        else:
            # Keep alive if no stream
            print("⚠️  No stream available, waiting...")
            while self.is_connected:
                await asyncio.sleep(0.1)
    
    async def process_transcription(self, transcript_text: str):
        """
        Process a transcription and trigger callback.
        
        Args:
            transcript_text: The transcribed text
        """
        if self.on_transcription:
            try:
                if asyncio.iscoroutinefunction(self.on_transcription):
                    await self.on_transcription(transcript_text)
                else:
                    self.on_transcription(transcript_text)
            except Exception as e:
                print(f"Error in transcription callback: {e}")
    
    def set_transcription_callback(self, callback: Callable):
        """Set callback function for transcription events."""
        self.on_transcription = callback
    
    def set_emotion_callback(self, callback: Callable):
        """Set callback function for emotion events."""
        self.on_emotion = callback
