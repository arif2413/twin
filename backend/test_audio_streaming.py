"""Test audio streaming to Hume AI."""
import asyncio
import os
from dotenv import load_dotenv
from hume_client import HumeAIClient

load_dotenv()

async def test_audio_streaming():
    """Test sending audio to Hume AI."""
    print("Testing audio streaming to Hume AI...")
    
    transcripts_received = []
    
    async def on_transcription(text):
        transcripts_received.append(text)
        print(f"📝 Received transcript: {text}")
    
    try:
        client = HumeAIClient(on_transcription=on_transcription)
        await client.connect()
        
        if not client.is_connected or not client.stream:
            print("❌ Not connected or stream not available")
            return False
        
        print("✅ Connected. Sending test audio chunk...")
        
        # Create a dummy audio chunk (PCM 16-bit, 16kHz, 1 second of silence)
        # This simulates what would come from the frontend
        sample_rate = 16000
        duration = 0.1  # 100ms
        num_samples = int(sample_rate * duration)
        # Generate silence (zeros) as Int16
        import struct
        audio_data = struct.pack(f'<{num_samples}h', *([0] * num_samples))
        
        # Send a few chunks
        for i in range(3):
            print(f"Sending audio chunk {i+1}/3...")
            await client.send_audio(audio_data)
            await asyncio.sleep(0.2)  # Wait between chunks
        
        # Wait a bit for responses
        print("Waiting for responses...")
        await asyncio.sleep(2)
        
        await client.disconnect()
        
        print(f"✅ Test complete. Received {len(transcripts_received)} transcriptions")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_audio_streaming())
    exit(0 if success else 1)

