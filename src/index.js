/**
 * Kai-Hub: 知识枢纽
 * 连接多个知识沙龙，形成大规模知识交换
 * 
 * 核心功能：
 * 1. 时空路由层 - 根据主题关联路由知识
 * 2. KaiDison 数字科学家 - 智能中枢
 * 3. 知识涌现合成器 - 跨域融合
 */

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

// 配置
const PORT = process.env.PORT || 3100;
const DATA_DIR = path.join(__dirname, 'data');

// 初始化数据目录
const fs = require('fs');
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 导入模块
const { KaiDison } = require('./orchestrator/kai-dison');
const { SpacetimeRouter } = require('./orchestrator/spacetime-router');
const { SalonManager } = require('./salons/salon-manager');
const { KnowledgeGraph } = require('./analytics/knowledge-graph');
const { EmergenceDetector } = require('./analytics/emergence-detector');

// 创建应用
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// 中间件
app.use(express.json());
app.use(express.static(path.join(__dirname, '../ui')));

// 初始化核心组件
const knowledgeGraph = new KnowledgeGraph();
const emergenceDetector = new EmergenceDetector(knowledgeGraph);
const router = new SpacetimeRouter();
const salonManager = new SalonManager(knowledgeGraph, router);
const kaiDison = new KaiDison({
    salonManager,
    knowledgeGraph,
    emergenceDetector,
    router,
    io
});

// ========== API 路由 ==========

// 获取枢纽状态
app.get('/api/hub/status', (req, res) => {
    res.json({
        status: 'running',
        version: '0.1.0',
        salons: salonManager.get_stats(),
        kaiDison: kaiDison.get_status(),
        uptime: process.uptime()
    });
});

// 沙龙管理
app.get('/api/salons', (req, res) => {
    res.json(salonManager.list_salons());
});

app.post('/api/salons/connect', async (req, res) => {
    try {
        const { type, config } = req.body;
        const salon = await salonManager.connect_salon(type, config);
        res.json({ status: 'success', salon });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/salons/:id/disconnect', (req, res) => {
    const { id } = req.params;
    salonManager.disconnect_salon(id);
    res.json({ status: 'success' });
});

// 主题管理
app.get('/api/topics', (req, res) => {
    const { domain, time_range, limit } = req.query;
    const topics = knowledgeGraph.query_topics({
        domain,
        time_range,
        limit: parseInt(limit) || 20
    });
    res.json({ topics });
});

app.get('/api/topics/:id', (req, res) => {
    const topic = knowledgeGraph.get_topic(req.params.id);
    if (!topic) {
        return res.status(404).json({ error: 'Topic not found' });
    }
    res.json(topic);
});

// 关系图谱
app.get('/api/graph/overview', (req, res) => {
    res.json(knowledgeGraph.get_overview());
});

app.get('/api/graph/domain/:domain', (req, res) => {
    const subgraph = knowledgeGraph.get_domain_subgraph(req.params.domain);
    res.json(subgraph);
});

// 涌现检测
app.get('/api/emergence/check', (req, res) => {
    const emergences = emergenceDetector.check_all();
    res.json({ emergences });
});

app.post('/api/emergence/trigger', async (req, res) => {
    const { topic_ids } = req.body;
    const result = await emergenceDetector.trigger_fusion(topic_ids);
    res.json({ status: 'success', result });
});

// 胶囊管理
app.get('/api/capsules', (req, res) => {
    const { domain, source, limit } = req.query;
    const capsules = knowledgeGraph.query_capsules({
        domain,
        source,
        limit: parseInt(limit) || 20
    });
    res.json({ capsules });
});

app.get('/api/capsules/:id', (req, res) => {
    const capsule = knowledgeGraph.get_capsule(req.params.id);
    if (!capsule) {
        return res.status(404).json({ error: 'Capsule not found' });
    }
    res.json(capsule);
});

// KaiDison 控制
app.post('/api/kaidison/analyze', async (req, res) => {
    const { target } = req.body;
    const analysis = await kaiDison.analyze(target);
    res.json({ analysis });
});

app.post('/api/kaidison/generate-insight', async (req, res) => {
    const { topics } = req.body;
    const insight = await kaiDison.generate_insight(topics);
    res.json({ insight });
});

// ========== Socket.IO 事件 ==========

io.on('connection', (socket) => {
    console.log(`Client connected: ${socket.id}`);
    
    // 订阅主题更新
    socket.on('subscribe:topic', (topicId) => {
        socket.join(`topic:${topicId}`);
    });
    
    // 订阅沙龙更新
    socket.on('subscribe:salon', (salonId) => {
        socket.join(`salon:${salonId}`);
    });
    
    // 订阅涌现检测
    socket.on('subscribe:emergence', () => {
        socket.join('emergence');
    });
    
    socket.on('disconnect', () => {
        console.log(`Client disconnected: ${socket.id}`);
    });
});

// ========== 启动 ==========

async function start() {
    try {
        // 初始化知识图谱
        await knowledgeGraph.init();
        
        // 连接 SuiLight（如果可用）
        try {
            await salonManager.connect_salon('suilight', {
                url: 'http://localhost:8000',
                api_key: process.env.SUILIGHT_API_KEY
            });
            console.log('✅ 已连接 SuiLight');
        } catch (e) {
            console.log('⚠️ SuiLight 未连接，将稍后重试');
        }
        
        // 启动 KaiDison 监控
        kaiDison.start_monitoring();
        
        // 启动服务器
        server.listen(PORT, () => {
            console.log(`
╔═══════════════════════════════════════════════════╗
║          Kai-Hub 知识枢纽 v0.1.0                  ║
╠═══════════════════════════════════════════════════╣
║  🚀 服务启动: http://localhost:${PORT}              ║
║  📊 仪表盘:   http://localhost:${PORT}/             ║
║  📚 API:      http://localhost:${PORT}/api          ║
╠═══════════════════════════════════════════════════╣
║  KaiDison 数字科学家已上线                         ║
║  监控沙龙: ${salonManager.get_stats().active || 0} 个                              ║
╚═══════════════════════════════════════════════════╝
            `);
        });
    } catch (error) {
        console.error('启动失败:', error);
        process.exit(1);
    }
}

start();

module.exports = { app, server, io };

// ========== BCI 场景 API ==========

// BCI 场景状态
app.get('/api/bci/status', async (req, res) => {
    try {
        const bciMetrics = new (require('./bci_scenario/metrics/bci-metrics'))();
        const status = bciMetrics.get_status();
        
        res.json({
            status: 'running',
            scenario: 'BCI_脑机接口',
            metrics: status,
            domains: ['neuroscience', 'ai_algorithm', 'materials_science', 'medical_application', 'ethics_society']
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// BCI 沙龙配置
app.get('/api/bci/salons', (req, res) => {
    try {
        const { BCI_SALONS } = require('./bci_scenario/salons/bci-salons');
        res.json(BCI_SALONS);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// BCI KaiDison 洞察
app.get('/api/bci/insights', async (req, res) => {
    try {
        // 返回模拟的洞察数据
        res.json({
            correlations: [
                {
                    type: 'neuroscience_ai',
                    strength: 0.9,
                    description: '神经科学与AI算法高度关联',
                    recommendation: '建议组织神经科学家与AI专家的联合讨论'
                }
            ],
            breakthroughs: [
                {
                    type: 'technical_breakthrough',
                    title: '端到端学习架构',
                    significance: 85
                }
            ],
            consensus: [
                {
                    topic: '认知隐私定义',
                    strength: 0.82,
                    recommendation: '已形成初步共识'
                }
            ]
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// BCI 评估报告
app.get('/api/bci/report', (req, res) => {
    try {
        const bciMetrics = new (require('./bci_scenario/metrics/bci-metrics'))();
        const report = bciMetrics.generate_report();
        res.json(report);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 更新 BCI 指标
app.post('/api/bci/metrics', (req, res) => {
    try {
        const { metric_name, value } = req.body;
        const bciMetrics = new (require('./bci_scenario/metrics/bci-metrics'))();
        bciMetrics.update(metric_name, value);
        res.json({ status: 'success' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// BCI 仪表盘页面
app.get('/bci', (req, res) => {
    res.sendFile(path.join(__dirname, '../../ui/bci-dashboard.html'));
});

