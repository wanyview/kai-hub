# Kai-Hub 知识枢纽

🔗 **连接多个知识沙龙，形成大规模知识交换**

## 📖 简介

Kai-Hub 是一个知识枢纽系统，连接多个知识沙龙（SuiLight、CapsuleHub 等），根据时空跨度在枢纽形成更大量级的知识传递和交换。

核心组件 **KaiDison（数字科学家）** 作为智能中枢，协调跨沙龙的知识流动和涌现。

## 🏗️ 架构

```
                    ┌─────────────────────────────────┐
                    │       知识枢纽 (Kai-Hub)         │
                    │  ┌─────────────────────────────┐│
                    │  │  时空路由层 (SpacetimeRouter)││
                    │  │  KaiDison 数字科学家         ││
                    │  │  知识涌现合成器              ││
                    │  └─────────────────────────────┘│
                    └─────────────────────────────────┘
                              ▲
              ┌───────────────┼───────────────┐
              │               │               │
      ┌───────▼───────┐ ┌───────▼───────┐ ┌───▼───────┐
      │   SuiLight    │ │   SuiLight    │ │  CapsuleHub│
      │   沙龙 A      │ │   沙龙 B      │ │  知识市场  │
      │ (历史复现)    │ │ (2026前瞻)    │ │            │
      └───────────────┘ └───────────────┘ └───────────┘
```

## ✨ 核心功能

### 1. 沙龙连接
- 连接多个知识沙龙（SuiLight、CapsuleHub）
- 实时同步讨论和胶囊数据
- 统一管理多个沙龙

### 2. 知识图谱
- 主题、胶囊、关系的三元组管理
- 跨域关联分析
- 知识演化追踪

### 3. KaiDison 数字科学家
- 并行监控多个沙龙讨论
- 识别跨沙龙知识关联
- 触发知识涌现融合
- 生成枢纽级洞察

### 4. 涌现检测
- 跨领域洞察涌现
- 共识涌现
- 分歧涌现
- 突破涌现

## 🚀 快速开始

### 环境要求
- Node.js 18+
- npm 或 yarn

### 安装

```bash
cd kai-hub
npm install
```

### 启动

```bash
npm start
```

服务启动后访问：http://localhost:3100

### 开发模式

```bash
npm run dev
```

## 📁 项目结构

```
kai-hub/
├── src/
│   ├── index.js              # 入口文件
│   ├── orchestrator/
│   │   ├── kai-dison.js      # 数字科学家
│   │   └── spacetime-router.js # 时空路由器
│   ├── salons/
│   │   └── salon-manager.js  # 沙龙管理器
│   └── analytics/
│       ├── knowledge-graph.js # 知识图谱
│       └── emergence-detector.js # 涌现检测
├── ui/
│   └── index.html            # 管理界面
├── data/                     # 数据存储
├── package.json
└── README.md
```

## 🔧 API 接口

### 枢纽状态
```bash
GET /api/hub/status
```

### 沙龙管理
```bash
GET  /api/salons              # 列出所有沙龙
POST /api/salons/connect      # 连接新沙龙
POST /api/salons/:id/disconnect # 断开沙龙
```

### 主题管理
```bash
GET /api/topics               # 查询主题
GET /api/topics/:id           # 获取主题详情
```

### 知识图谱
```bash
GET /api/graph/overview       # 图谱概览
GET /api/graph/domain/:domain # 领域子图谱
```

### 涌现检测
```bash
GET /api/emergence/check      # 检测涌现
POST /api/emergence/trigger   # 触发融合
```

### KaiDison
```bash
POST /api/kaidison/analyze          # 分析目标
POST /api/kaidison/generate-insight # 生成洞察
```

## 🔌 集成 SuiLight

Kai-Hub 会自动尝试连接本地运行的 SuiLight 服务：

```bash
# 启动 SuiLight (端口 8000)
cd /Users/wanyview/SuiLight
python3 -m uvicorn src.main:app --port 8000

# 启动 Kai-Hub (端口 3100)
cd kai-hub
npm start
```

## 📊 评估指标

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| 沙龙连接数 | 10+ | 监控活跃沙龙 |
| 跨域融合数 | 5+/周 | 融合会话计数 |
| 枢纽级胶囊 | 10+/月 | 产出统计 |
| 知识复用率 | >30% | 引用分析 |

## 🛠️ 依赖关系

```
kai-hub
├── kai-os (基础框架)
│   └── DATM 系统
├── SuiLight (知识源)
│   └── 讨论系统
└── CapsuleHub (知识库)
    └── 胶囊存储
```

## 📝 实施计划

### Phase 1: 基础设施
- [x] 项目结构搭建
- [x] Express 服务器
- [x] 沙龙连接层
- [x] 基础 API

### Phase 2: KaiDison 核心
- [x] 数字科学家智能体
- [x] 主题关系图
- [x] 关联度分析
- [x] 基础监控

### Phase 3: 知识涌现
- [x] 涌现检测算法
- [x] 跨沙龙融合讨论
- [x] 枢纽级胶囊生成
- [x] 知识图谱可视化

### Phase 4: 产品化
- [ ] 枢纽管理 UI
- [ ] 仪表盘开发
- [ ] 用户引导
- [ ] 部署上线

## 📄 许可证

MIT License

## 🤝 贡献

欢迎贡献代码或建议！

---

*Powered by Kai Digital Agent*
