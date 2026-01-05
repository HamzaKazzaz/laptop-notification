import websockets
import json
import socket
import time
import asyncio
import sys
from datetime import datetime

WEBSOCKET_SERVER_URL = "wss://laptop-notification-prod.railway.app"

async def send_notification():
    """Send laptop startup notification via WebSocket"""
    try:
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
        except:
            ip_address = "N/A"
        
        timestamp = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
        
        notification = {
            "type": "notification",
            "title": "💻 Laptop Açıldı",
            "computer": hostname,
            "ip": ip_address,
            "timestamp": timestamp,
            "message": f"Bilgisayarınız {hostname} başlatıldı"
        }
        
        async with websockets.connect(WEBSOCKET_SERVER_URL, ssl=True) as websocket:
            await websocket.send(json.dumps(notification))
            print("✅ Bildirim gönderildi!")
            print(f"   Bilgisayar: {hostname}")
            print(f"   IP: {ip_address}")
            print(f"   Saat: {timestamp}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_notification())
