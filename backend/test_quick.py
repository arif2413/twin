"""Quick test to identify errors."""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    try:
        print("1. Testing imports...")
        from hume import AsyncHumeClient
        from hume.empathic_voice.types.audio_input import AudioInput
        print("   ✅ Imports successful")
        
        print("2. Testing API key...")
        api_key = os.getenv("HUME_API_KEY")
        if not api_key:
            print("   ❌ HUME_API_KEY not found")
            return
        print(f"   ✅ API key found: {api_key[:10]}...")
        
        print("3. Testing client creation...")
        client = AsyncHumeClient(api_key=api_key)
        print("   ✅ Client created")
        
        print("4. Testing connection...")
        stream_context = client.empathic_voice.chat.connect()
        stream = await stream_context.__aenter__()
        print("   ✅ Stream connected")
        
        await stream_context.__aexit__(None, None, None)
        print("   ✅ Stream closed")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())

