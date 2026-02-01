#!/usr/bin/env python3
"""
Kai-Hub HTTP Server (轻量级 Python 实现)
提供 BCI 场景仪表盘和 API
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime

PORT = 3100

class KaiHubHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/ui/index.html'
        elif self.path == '/bci':
            self.path = '/ui/bci-dashboard.html'
        elif self.path == '/api/hub/status':
            self.send_json_response({
                "status": "running",
                "version": "0.1.0",
                "scenario": "BCI_脑机接口",
                "kaiDison": {
                    "active": True,
                    "monitoring_count": 3,
                    "fusion_sessions": 5
                },
                "salons": {
                    "neuroscience": {"status": "active", "topics": 3, "agents": 4},
                    "ai_algorithm": {"status": "active", "topics": 3, "agents": 4},
                    "ethics_society": {"status": "active", "topics": 3, "agents": 4}
                },
                "metrics": {
                    "cross_domain_links": {"current": 8, "target": 20, "progress": 40},
                    "fusion_capsules": {"current": 3, "target": 10, "progress": 30},
                    "breakthroughs": {"current": 2, "target": 5, "progress": 40},
                    "consensus": {"current": 1, "target": 5, "progress": 20}
                },
                "uptime": 3600
            })
        elif self.path == '/api/bci/salons':
            self.send_json_response({
                "salons": {
                    "neuroscience": {
                        "name": "神经科学基础",
                        "topics": ["运动皮层信号特征", "感觉反馈机制", "神经可塑性"],
                        "agents": ["神经科学家", "计算神经科学家", "临床神经科医生"]
                    },
                    "ai_algorithm": {
                        "name": "AI算法突破", 
                        "topics": ["低延迟解码", "个性化模型", "端到端学习"],
                        "agents": ["AI研究员", "信号处理专家", "嵌入式系统工程师"]
                    },
                    "ethics_society": {
                        "name": "伦理与社会",
                        "topics": ["认知隐私", "增强边界", "公平获取"],
                        "agents": ["科技哲学家", "生物伦理学家", "法律学者"]
                    }
                }
            })
        elif self.path == '/api/bci/insights':
            self.send_json_response({
                "insights": [
                    {
                        "type": "cross_domain",
                        "title": "神经科学与AI算法关联",
                        "description": "运动意图解码是连接两个沙龙的核心话题",
                        "recommendation": "建议组织联合讨论会"
                    },
                    {
                        "type": "breakthrough",
                        "title": "端到端学习架构突破",
                        "description": "直接神经信号到控制指令的映射",
                        "significance": 85
                    },
                    {
                        "type": "consensus",
                        "title": "认知隐私定义共识",
                        "description": "已形成初步共识：神经信号需要特殊保护"
                    }
                ],
                "generated_at": datetime.utcnow().isoformat()
            })
        elif self.path == '/api/capsules/summary':
            # 从 CapsuleHub 获取摘要
            try:
                import urllib.request
                req = urllib.request.urlopen('http://localhost:8001/api/capsules/?limit=10', timeout=5)
                data = json.loads(req.read().decode())
                self.send_json_response({
                    "total": data.get("total", 0),
                    "capsules": [c.get("title", "") for c in data.get("capsules", [])[-5:]]
                })
            except:
                self.send_json_response({"error": "CapsuleHub unavailable"})
            return
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def send_json_response(self, data):
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # 禁用日志

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    server = HTTPServer(('0.0.0.0', PORT), KaiHubHandler)
    print(f'''
╔═══════════════════════════════════════════════════════════╗
║          Kai-Hub BCI 知识枢纽 v0.1.0               ║
╠═══════════════════════════════════════════════════════════╣
║  🚀 服务已启动: http://localhost:{PORT}                 ║
║  📊 仪表盘:     http://localhost:{PORT}/bci            ║
║  📚 API:        http://localhost:{PORT}/api/            ║
╠═══════════════════════════════════════════════════════════╣
║  BCI 场景: 脑机接口                               ║
║  胶囊数量: 10 (已生成并推送到 CapsuleHub)           ║
╚═══════════════════════════════════════════════════════════╝
    ''')
    server.serve_forever()

if __name__ == '__main__':
    run()
