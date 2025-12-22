// server.js
const WebSocket = require("ws");
const { WebSocketServer } = require("ws");
const osc = require("osc");

const WSPORT = 7438;

// WebSocket 서버 생성 (A HTML, C video.html이 연결)
const wss = new WebSocketServer({ port: WSPORT });
console.log("🌐 WebSocket 서버 실행 중");

// OSC 설정 (TouchDesigner로 보낼 포트)
const udpPort = new osc.UDPPort({
  localAddress: "0.0.0.0",
  localPort: 57125,
  remoteAddress: "192.168.0.3",   // 예: "192.168.0.15"
  remotePort: 7439               // TouchDesigner의 OSC In 포트
});
udpPort.open();

// WebSocket 메시지 수신 처리
wss.on("connection", (ws) => {
  console.log("💻 클라이언트 연결됨");

  ws.on("message", (msg) => {
    const data = JSON.parse(msg);
    console.log("📨 받은 메시지:", data);

    // 1) 슬라이더 → OSC
    if (data.type === "sliderData") {
      for (let key in data.data) {
        udpPort.send({
          address: `/slider/${key}`,
          args: [data.data[key]]
        });
      }
    }

    // 2) 모든 WebSocket 연결(C 노트북 video)에도 브로드캐스트
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(msg);
      }
    });
  });
});
