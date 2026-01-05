import asyncio
import websockets
import json
import socket
import os
from datetime import datetime

# Store connected clients
clients = set()

async def handler(websocket, path):
    """Handle new WebSocket connections"""
    clients.add(websocket)
    print(f"✅ Client connected. Total: {len(clients)}")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                # Broadcast to all connected clients
                for client in clients:
                    if client != websocket:
                        try:
                            await client.send(message)
                        except:
                            pass
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)
        print(f"❌ Client disconnected. Total: {len(clients)}")

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"🚀 WebSocket server running on ws://0.0.0.0:{port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
