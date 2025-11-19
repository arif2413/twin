"""Test message receiving from Hume AI."""
import asyncio
import os
from dotenv import load_dotenv
from hume_client import HumeAIClient

load_dotenv()

async def test():
    transcripts = []
    
    async def on_transcription(text):
        transcripts.append(text)
        print(f"✅ Received transcript: {text}")
    
    client = HumeAIClient(on_transcription=on_transcription)
    await client.connect()
    
    if not client.stream:
        print("❌ No stream available")
        return
    
    print("✅ Connected. Checking stream methods...")
    print(f"Stream has 'on': {hasattr(client.stream, 'on')}")
    print(f"Stream has 'start_listening': {hasattr(client.stream, 'start_listening')}")
    print(f"Stream has 'recv': {hasattr(client.stream, 'recv')}")
    
    # Try using 'on' method if available
    if hasattr(client.stream, 'on'):
        print("Using 'on' method for event handling...")
        # This would be the callback-based approach
    
    # Wait a bit to see if we get any messages
    print("Waiting 5 seconds for any messages...")
    await asyncio.sleep(5)
    
    await client.disconnect()
    print(f"Received {len(transcripts)} transcripts")

asyncio.run(test())

