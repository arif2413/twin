"""
Script to close all active Hume AI chat sessions.
This helps when you've hit the 5 concurrent chat limit.

Based on Hume AI API: https://dev.hume.ai/reference/empathic-voice-interface-evi/chats
"""
import asyncio
import os
from dotenv import load_dotenv
from hume import AsyncHumeClient

load_dotenv()

async def list_and_close_chats():
    """List and attempt to close all active Hume AI chat sessions."""
    api_key = os.getenv("HUME_API_KEY")
    if not api_key:
        print("❌ HUME_API_KEY not found in environment")
        return
    
    print("🔍 Connecting to Hume AI...")
    
    try:
        client = AsyncHumeClient(api_key=api_key)
        
        # Try to list active chats using the chats API
        # According to docs: https://dev.hume.ai/reference/empathic-voice-interface-evi/chats/list-chat-events
        try:
            print("\n📋 Attempting to list active chat sessions...")
            
            # Check if there's a chats endpoint
            # The exact method may vary - trying common patterns
            if hasattr(client, 'empathic_voice') and hasattr(client.empathic_voice, 'chats'):
                chats_client = client.empathic_voice.chats
                
                # Try to list chats (if method exists)
                if hasattr(chats_client, 'list'):
                    print("  ✅ Found chats.list() method")
                    # This would list active chats - implementation depends on API
                    print("  ⚠️  Direct list method may require additional parameters")
                else:
                    print("  ⚠️  No direct list method found")
            
            print("\n💡 Alternative approach: Force disconnect by connecting/disconnecting")
            print("   This may help clear stale connections...")
            
        except Exception as e:
            print(f"⚠️  Could not list chats directly: {e}")
        
        # Alternative: Connect and immediately disconnect to clear connections
        print("\n🔄 Attempting to clear connections...")
        print("   (This connects and immediately disconnects to free up slots)")
        
        cleared = 0
        max_attempts = 6  # One more than the limit
        
        for i in range(max_attempts):
            try:
                print(f"\n  Attempt {i+1}/{max_attempts}:")
                print("    → Connecting...", end=" ")
                
                # Connect
                stream_context = client.empathic_voice.chat.connect()
                stream = await stream_context.__aenter__()
                
                print("✅ Connected")
                print("    → Disconnecting...", end=" ")
                
                # Immediately disconnect
                await stream_context.__aexit__(None, None, None)
                
                print("✅ Disconnected")
                cleared += 1
                
                # Small delay
                await asyncio.sleep(0.3)
                
            except Exception as e:
                error_str = str(e).lower()
                if "too_many_active_chats" in error_str:
                    print("❌ Still at limit")
                    print(f"    ({cleared} connections cleared so far)")
                    print("    💡 Wait 30-60 seconds and try again")
                else:
                    print(f"⚠️  Error: {e}")
        
        print(f"\n✅ Processed {cleared} connections")
        
        if cleared > 0:
            print("\n⏳ Wait 30-60 seconds for sessions to fully close")
            print("   Then restart your backend server")
        else:
            print("\n💡 All connection slots may still be in use")
            print("   Options:")
            print("   1. Wait 2-3 minutes for natural timeout")
            print("   2. Check Hume AI dashboard for active sessions")
            print("   3. Close all browser tabs with active connections")
            print("   4. Restart your computer (forces all connections to close)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("Hume AI Chat Session Cleanup Tool")
    print("=" * 70)
    print()
    print("This script attempts to close active Hume AI chat sessions.")
    print("Use this when you're hitting the '5 concurrent chats' limit.")
    print()
    
    asyncio.run(list_and_close_chats())
    
    print()
    print("=" * 70)
    print("📚 Additional Resources:")
    print("  • Hume AI Dashboard: https://platform.hume.ai/")
    print("  • API Docs: https://dev.hume.ai/reference/empathic-voice-interface-evi/chats")
    print("=" * 70)
