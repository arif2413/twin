"""Test script for Hume AI connection."""
import asyncio
import os
from dotenv import load_dotenv
from hume_client import HumeAIClient

load_dotenv()

async def test_connection():
    """Test Hume AI connection."""
    print("Testing Hume AI connection...")
    
    try:
        client = HumeAIClient()
        print("✅ Client created successfully")
        
        result = await client.connect()
        print(f"✅ Connection result: {result}")
        print(f"✅ Is connected: {client.is_connected}")
        
        if client.is_connected:
            print("✅ Stream available:", client.stream is not None)
        
        await client.disconnect()
        print("✅ Disconnected successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)

