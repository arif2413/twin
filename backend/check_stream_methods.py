"""Check what methods are available on the stream object."""
import asyncio
from hume import AsyncHumeClient

async def check():
    client = AsyncHumeClient(api_key='test')
    ctx = client.empathic_voice.chat.connect()
    stream = await ctx.__aenter__()
    
    print('Stream type:', type(stream).__name__)
    print('\nAll methods (non-private):')
    methods = [m for m in dir(stream) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")
    
    print('\nMethods that might be for sending/receiving:')
    relevant = [m for m in methods if any(keyword in m.lower() for keyword in ['send', 'receive', 'audio', 'message', 'write', 'put'])]
    for method in relevant:
        print(f"  - {method}")

asyncio.run(check())

