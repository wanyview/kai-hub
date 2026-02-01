#!/usr/bin/env python3
"""
Kai-Hub BCI 知识枢纽服务
连接 SuiLight → CapsuleHub → KaiDison
"""

import http.server
import socketserver
import json
import os
import threading
import time

os.chdir('/Users/wanyview/clawd/kai-hub')
PORT = 3100

class KaiHubHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/bci' or self.path == '/':
            self.path = '/ui/bci-dashboard.html'
        elif self.path == '/api/hub/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "running",
                "version": "0.1.0",
                "scenario": "BCI_脑机接口",
                "kaiDison": {"active": True, "monitoring_count": 3},
                "metrics": {
                    "cross_domain_links": 12,
                    "fusion_capsules": 5,
                    "breakthroughs": 2,
                    "consensus": 1
                },
                "uptime": time.time()
            }, ensure_ascii=False).encode())
            return
        elif self.path == '/api/capsules/count':
            try:
                import urllib.request
                r = urllib.request.urlopen('http://localhost:8001/api/capsules/?limit=1', timeout=3)
                data = json.loads(r.read().decode())
                self.send_json_response({"total": data.get("total", 0)})
            except Exception as e:
                self.send_json_response({"error": str(e)})
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

# 启动
server = socketserver.TCPServer(("", PORT), KaiHubHandler)
print(f'''
╔═══════════════════════════════════════════════════════════╗
║          Kai-Hub BCI 知识枢纽 v0.1.0                      ║
╠═══════════════════════════════════════════════════════════╣
║  🚀 服务已启动: http://localhost:{PORT}                   ║
║  📊 BCI仪表盘:  http://localhost:{PORT}/bci              ║
║  📚 API:       http://localhost:{PORT}/api/              ║
╠═══════════════════════════════════════════════════════════╣
║  胶囊统计: 10 个 BCI 知识胶囊                             ║
║  沙   龙: 3 个并行 (神经科学+AI+伦理)                     ║
╚═══════════════════════════════════════════════════════════╝
''')

server.serve_forever()
