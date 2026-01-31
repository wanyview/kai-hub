/**
 * KnowledgeGraph: 知识图谱
 * 管理主题、胶囊和它们之间的关系
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

class KnowledgeGraph {
    constructor(config = {}) {
        this.dataDir = config.dataDir || path.join(__dirname, '../../data');
        this.dbPath = path.join(this.dataDir, 'knowledge_graph.db');
        
        if (!fs.existsSync(this.dataDir)) {
            fs.mkdirSync(this.dataDir, { recursive: true });
        }
        
        this.db = new Database(this.dbPath);
        this._init_db();
    }
    
    async init() {
        // 加载已存在的数据
        console.log('📊 知识图谱已初始化');
    }
    
    _init_db() {
        // 主题表
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                domain TEXT,
                keywords TEXT,
                salon_id TEXT,
                metadata TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        `);
        
        // 胶囊表
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS capsules (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                domain TEXT,
                keywords TEXT,
                insight TEXT,
                source_salon TEXT,
                source_topic TEXT,
                metadata TEXT,
                score REAL,
                created_at TEXT
            )
        `);
        
        // 关系表
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                source_type TEXT,
                source_id TEXT,
                target_type TEXT,
                target_id TEXT,
                relationship_type TEXT,
                strength REAL,
                created_at TEXT
            )
        `);
        
        // 洞察表
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS insights (
                id TEXT PRIMARY KEY,
                type TEXT,
                source_topics TEXT,
                common_keywords TEXT,
                common_domain TEXT,
                summary TEXT,
                recommendations TEXT,
                created_at TEXT
            )
        `);
        
        // 索引
        this.db.exec(`
            CREATE INDEX IF NOT EXISTS idx_topics_domain ON topics(domain);
            CREATE INDEX IF NOT EXISTS idx_capsules_domain ON capsules(domain);
            CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_type, source_id);
        `);
    }
    
    // ========== 主题管理 ==========
    
    async add_topic(topic) {
        const stmt = this.db.prepare(`
            INSERT INTO topics (id, title, domain, keywords, salon_id, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `);
        
        stmt.run(
            topic.id || uuidv4(),
            topic.title,
            topic.domain,
            JSON.stringify(topic.keywords || []),
            topic.salon_id,
            JSON.stringify(topic.metadata || {}),
            new Date().toISOString(),
            new Date().toISOString()
        );
        
        return topic;
    }
    
    get_topic(topicId) {
        const stmt = this.db.prepare('SELECT * FROM topics WHERE id = ?');
        const row = stmt.get(topicId);
        
        if (!row) return null;
        
        return this._row_to_topic(row);
    }
    
    query_topics({ domain, time_range, limit = 20 }) {
        let query = 'SELECT * FROM topics WHERE 1=1';
        const params = [];
        
        if (domain) {
            query += ' AND domain = ?';
            params.push(domain);
        }
        
        query += ' ORDER BY created_at DESC LIMIT ?';
        params.push(limit);
        
        const stmt = this.db.prepare(query);
        const rows = stmt.all(...params);
        
        return rows.map(row => this._row_to_topic(row));
    }
    
    async get_salon_topics(salonId) {
        const stmt = this.db.prepare('SELECT * FROM topics WHERE salon_id = ?');
        const rows = stmt.all(salonId);
        return rows.map(row => this._row_to_topic(row));
    }
    
    // ========== 胶囊管理 ==========
    
    async add_capsule(capsule) {
        const stmt = this.db.prepare(`
            INSERT INTO capsules (id, title, domain, keywords, insight, source_salon, source_topic, metadata, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `);
        
        stmt.run(
            capsule.id || uuidv4(),
            capsule.title,
            capsule.domain,
            JSON.stringify(capsule.keywords || []),
            capsule.insight,
            capsule.source_salon,
            capsule.source_topic,
            JSON.stringify(capsule.metadata || {}),
            capsule.score || 0,
            new Date().toISOString()
        );
        
        return capsule;
    }
    
    get_capsule(capsuleId) {
        const stmt = this.db.prepare('SELECT * FROM capsules WHERE id = ?');
        const row = stmt.get(capsuleId);
        
        if (!row) return null;
        
        return this._row_to_capsule(row);
    }
    
    query_capsules({ domain, source, limit = 20 }) {
        let query = 'SELECT * FROM capsules WHERE 1=1';
        const params = [];
        
        if (domain) {
            query += ' AND domain = ?';
            params.push(domain);
        }
        
        if (source) {
            query += ' AND source_salon = ?';
            params.push(source);
        }
        
        query += ' ORDER BY created_at DESC LIMIT ?';
        params.push(limit);
        
        const stmt = this.db.prepare(query);
        const rows = stmt.all(...params);
        
        return rows.map(row => this._row_to_capsule(row));
    }
    
    // ========== 关系管理 ==========
    
    async add_relationship(relationship) {
        const stmt = this.db.prepare(`
            INSERT INTO relationships (id, source_type, source_id, target_type, target_id, relationship_type, strength, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `);
        
        stmt.run(
            uuidv4(),
            relationship.sourceType,
            relationship.sourceId,
            relationship.targetType,
            relationship.targetId,
            relationship.relationshipType || 'related',
            relationship.strength || 0.5,
            new Date().toISOString()
        );
    }
    
    get_related_topics(topicId) {
        const stmt = this.db.prepare(`
            SELECT t.*, r.strength
            FROM topics t
            JOIN relationships r ON t.id = r.target_id
            WHERE r.source_type = 'topic' AND r.source_id = ?
            UNION
            SELECT t.*, r.strength
            FROM topics t
            JOIN relationships r ON t.id = r.source_id
            WHERE r.target_type = 'topic' AND r.target_id = ?
        `);
        
        const rows = stmt.all(topicId, topicId);
        return rows.map(row => this._row_to_topic(row));
    }
    
    // ========== 洞察管理 ==========
    
    async add_insight(insight) {
        const stmt = this.db.prepare(`
            INSERT INTO insights (id, type, source_topics, common_keywords, common_domain, summary, recommendations, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `);
        
        stmt.run(
            insight.id || uuidv4(),
            insight.type,
            JSON.stringify(insight.source_topics || []),
            JSON.stringify(insight.common_keywords || []),
            insight.common_domain,
            insight.summary,
            JSON.stringify(insight.recommendations || []),
            new Date().toISOString()
        );
    }
    
    // ========== 图谱操作 ==========
    
    async register_salon(salon) {
        // 沙龙注册逻辑
        console.log(`📍 沙龙已注册: ${salon.name}`);
    }
    
    async add_discussion_update(salonId, update) {
        // 添加讨论更新到图谱
        if (update.topics && update.topics.length > 0) {
            for (const topic of update.topics) {
                await this.add_topic({
                    id: topic.id || uuidv4(),
                    title: topic.title,
                    domain: topic.domain,
                    keywords: topic.keywords,
                    salon_id: salonId
                });
            }
        }
    }
    
    get_overview() {
        const topicsCount = this.db.prepare('SELECT COUNT(*) as count FROM topics').get().count;
        const capsulesCount = this.db.prepare('SELECT COUNT(*) as count FROM capsules').get().count;
        const relationsCount = this.db.prepare('SELECT COUNT(*) as count FROM relationships').get().count;
        
        // 领域分布
        const domainDist = this.db.prepare(`
            SELECT domain, COUNT(*) as count 
            FROM topics 
            GROUP BY domain 
            ORDER BY count DESC
        `).all();
        
        return {
            topics: topicsCount,
            capsules: capsulesCount,
            relationships: relationsCount,
            domain_distribution: domainDist
        };
    }
    
    get_domain_subgraph(domain) {
        const topics = this.query_topics({ domain, limit: 50 });
        const capsules = this.query_capsules({ domain, limit: 50 });
        
        const topicIds = topics.map(t => t.id);
        
        // 获取相关关系
        let relationships = [];
        if (topicIds.length > 0) {
            const placeholders = topicIds.map(() => '?').join(',');
            relationships = this.db.prepare(`
                SELECT * FROM relationships 
                WHERE source_id IN (${placeholders}) OR target_id IN (${placeholders})
            `).all(...topicIds, ...topicIds);
        }
        
        return {
            domain,
            topics,
            capsules,
            relationships
        };
    }
    
    get_topic_history(topicId) {
        // 获取主题的历史讨论
        return [];
    }
    
    // ========== 辅助方法 ==========
    
    _row_to_topic(row) {
        return {
            id: row.id,
            title: row.title,
            domain: row.domain,
            keywords: JSON.parse(row.keywords || '[]'),
            salon_id: row.salon_id,
            metadata: JSON.parse(row.metadata || '{}'),
            created_at: row.created_at,
            updated_at: row.updated_at
        };
    }
    
    _row_to_capsule(row) {
        return {
            id: row.id,
            title: row.title,
            domain: row.domain,
            keywords: JSON.parse(row.keywords || '[]'),
            insight: row.insight,
            source_salon: row.source_salon,
            source_topic: row.source_topic,
            metadata: JSON.parse(row.metadata || '{}'),
            score: row.score,
            created_at: row.created_at
        };
    }
}

module.exports = { KnowledgeGraph };
