# ws_videoserver.py
import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):
    print("🎉 video.html 클라이언트 접속")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"📩 받은 메시지: {message}")

            # 브로드캐스트 (보낸 사람 제외)
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("❌ 클라이언트 연결 종료됨")

    finally:
        connected_clients.remove(websocket)


async def main():
    host_ip = "0.0.0.0"   # 모든 네트워크에서 접속 허용
    port = 7437

    print(f"🚀 Video WebSocket 서버 시작 : ws://{host_ip}:{port}")
    async with websockets.serve(handler, host_ip, port):
        await asyncio.Future()  # 서버 계속 실행


if __name__ == "__main__":
    asyncio.run(main())
