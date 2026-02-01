#!/usr/bin/env python3
"""
Kai-Hub HTTP Server with KaiDison Integration
"""

import http.server
import socketserver
import json
import os
import threading
import time
from datetime import datetime

os.chdir('/Users/wanyview/clawd/kai-hub')
PORT = 3100

# 导入 KaiDison
sys.path.insert(0, 'src')
from kai_dison_professional import KaiDisonProfessional

kaiDison = KaiDisonProfessional()


class KaiHubHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # BCI Dashboard
        if self.path == '/bci':
            self.path = '/ui/bci-dashboard.html'
        
        # API: Hub Status
        elif self.path == '/api/hub/status':
            status = kaiDison.get_status()
            self.send_json_response({
                **status,
                "version": "0.1.0",
                "scenario": "BCI_脑机接口"
            })
        
        # API: KaiDison Analyze
        elif self.path == '/api/kai-dison/analyze':
            result = kaiDison.scan_and_analyze()
            self.send_json_response(result)
        
        # API: KaiDison Status
        elif self.path == '/api/kai-dison/status':
            self.send_json_response(kaiDison.get_status())
        
        # API: Cross-Domain Links
        elif self.path == '/api/kai-dison/associations':
            capsules = kaiDison._fetch_capsules()
            associations = kaiDison.cross_domain.find_associations(capsules)
            self.send_json_response({
                "count": len(associations),
                "associations": [
                    {
                        "domains": [a.domain_a, a.domain_b],
                        "strength": a.strength,
                        "topics": a.topics,
                        "recommendation": a.recommendation
                    }
                    for a in associations
                ]
            })
        
        # API: Breakthroughs
        elif self.path == '/api/kai-dison/breakthroughs':
            capsules = kaiDison._fetch_capsules()
            breakthroughs = kaiDison.breakthrough_detector.detect(capsules)
            self.send_json_response({
                "count": len(breakthroughs),
                "breakthroughs": [
                    {
                        "title": b.title,
                        "significance": b.significance,
                        "type": b.type,
                        "domains": b.domains
                    }
                    for b in breakthroughs
                ]
            })
        
        # API: Consensus
        elif self.path == '/api/kai-dison/consensus':
            capsules = kaiDison._fetch_capsules()
            consensuses = kaiDison.consensus_tracker.track(capsules)
            self.send_json_response({
                "count": len(consensuses),
                "consensus": [
                    {
                        "topic": c.topic,
                        "domains": c.domains,
                        "strength": c.strength
                    }
                    for c in consensuses
                ]
            })
        
        # API: Trends
        elif self.path == '/api/kai-dison/trends':
            capsules = kaiDison._fetch_capsules()
            trends = kaiDison.trend_predictor.predict(capsules)
            self.send_json_response(trends[0] if trends else {})
        
        # API: Capsules Count
        elif self.path == '/api/capsules/count':
            try:
                import urllib.request
                r = urllib.request.urlopen('http://localhost:8001/api/capsules?limit=1', timeout=3)
                data = json.loads(r.read().decode())
                self.send_json_response({"total": data.get("total", 0)})
            except Exception as e:
                self.send_json_response({"error": str(e)})
        
        # Static files
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())


# 启动服务
server = socketserver.TCPServer(("", PORT), KaiHubHandler)

print(f'''
╔═══════════════════════════════════════════════════════════════════╗
║          Kai-Hub 知识枢纽 + KaiDison v0.1.0                      ║
╠═══════════════════════════════════════════════════════════════════╣
║  🚀 服务已启动: http://localhost:{PORT}                           ║
║  📊 BCI仪表盘:  http://localhost:{PORT}/bci                      ║
║  🤖 KaiDison:   http://localhost:{PORT}/api/kai-dison/analyze    ║
╠═══════════════════════════════════════════════════════════════════╣
║  KaiDison 专业功能:                                               ║
║    🔗 跨域关联  💥 突破检测  🤝 共识追踪  🔮 趋势预测             ║
╚═══════════════════════════════════════════════════════════════════╝
''')

server.serve_forever()
