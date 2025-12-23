from pythonosc.udp_client import SimpleUDPClient
import websocket
import json
import time

TD_IP = "127.0.0.1"
TD_PORT = 7439

client = SimpleUDPClient(TD_IP, TD_PORT)

# --------------------------
#   WebSocket 이벤트 함수
# --------------------------

def on_open(ws):
    print("🟢 [WebSocket] 연결 성공!")

def on_close(ws, close_status_code, close_msg):
    print(f"🔴 [WebSocket] 연결 종료됨 | 코드: {close_status_code}, 메시지: {close_msg}")

def on_error(ws, error):
    print(f"⚠️ [WebSocket] 오류 발생: {error}")

def on_message(ws, message):
    print("📩 받은 메시지:", message)
    try:
        msg = json.loads(message)

        # 실제 값은 msg["data"] 안에 있음
        slider_values = msg.get("data", {})

        for key, value in slider_values.items():
            client.send_message(f"/{key}", float(value))
            print(f"➡️ OSC 전송: /{key} = {value}")

    except Exception as e:
        print("JSON 처리 오류:", e)



# --------------------------
#   WebSocket 실행 함수
# --------------------------

def run_ws():
    websocket.enableTrace(True)   # 🔍 연결 과정 상세 로그 출력

    while True:
        print("🔵 [WebSocket] 서버 연결 시도 중...")

        try:
            ws = websocket.WebSocketApp(
                "ws://192.168.0.2:7438",   # 팀원 노트북 or 서버 IP
                on_open=on_open,
                on_message=on_message,
                on_close=on_close,
                on_error=on_error
            )

            ws.run_forever()
        except Exception as e:
            print("⚠️ [WebSocket] 예외 발생:", e)

        print("⏳ 3초 후 재연결 시도...")
        time.sleep(3)


# --------------------------
#   실행
# --------------------------

run_ws()
