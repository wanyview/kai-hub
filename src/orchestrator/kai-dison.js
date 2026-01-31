/**
 * KaiDison: 数字科学家
 * 知识枢纽的智能中枢
 * 
 * 职责：
 * 1. 监控多个沙龙的讨论进展
 * 2. 识别跨沙龙的知识关联
 * 3. 触发知识涌现融合
 * 4. 生成枢纽级洞察
 */

const { v4: uuidv4 } = require('uuid');

class KaiDison {
    constructor(config) {
        this.salonManager = config.salonManager;
        this.knowledgeGraph = config.knowledgeGraph;
        this.emergenceDetector = config.emergenceDetector;
        this.router = config.router;
        this.io = config.io;
        
        this.active = false;
        this.monitorInterval = null;
        this.fusionSessions = new Map();
    }
    
    get_status() {
        return {
            active: this.active,
            monitoring_count: this.salonManager.get_stats().active || 0,
            fusion_sessions: this.fusionSessions.size,
            last_check: new Date().toISOString()
        };
    }
    
    start_monitoring() {
        if (this.active) return;
        
        this.active = true;
        console.log('🔬 KaiDison 开始监控...');
        
        // 每60秒检查一次沙龙更新
        this.monitorInterval = setInterval(async () => {
            await this._check_discussions();
        }, 60000);
        
        // 立即执行一次检查
        this._check_discussions();
    }
    
    stop_monitoring() {
        this.active = false;
        if (this.monitorInterval) {
            clearInterval(this.monitorInterval);
            this.monitorInterval = null;
        }
    }
    
    async _check_discussions() {
        try {
            const salons = this.salonManager.get_active_salons();
            
            for (const salon of salons) {
                // 获取最新讨论
                const updates = await salon.get_recent_updates();
                
                if (updates.length === 0) continue;
                
                // 更新知识图谱
                for (const update of updates) {
                    await this.knowledgeGraph.add_discussion_update(salon.id, update);
                }
                
                // 检测是否有关联话题
                const related = await this._find_related(updates, salons);
                
                if (related.length > 0) {
                    // 触发跨沙龙融合
                    await this._trigger_cross_salon_fusion(updates, related);
                }
                
                // 广播更新
                this.io?.to(`salon:${salon.id}`).emit('update', {
                    salon_id: salon.id,
                    updates: updates.length
                });
            }
        } catch (error) {
            console.error('监控检查失败:', error);
        }
    }
    
    async _find_related(updates, allSalons) {
        const related = [];
        const updateTopics = new Set(updates.map(u => u.topics || []).flat());
        
        for (const salon of allSalons) {
            if (updates.some(u => u.salon_id === salon.id)) continue;
            
            const salonTopics = await this.knowledgeGraph.get_salon_topics(salon.id);
            const intersection = salonTopics.filter(t => updateTopics.has(t));
            
            if (intersection.length > 0) {
                related.push({
                    salon: salon,
                    topics: intersection
                });
            }
        }
        
        return related;
    }
    
    async _trigger_cross_salon_fusion(sourceUpdates, related) {
        const sessionId = uuidv4();
        
        const session = {
            id: sessionId,
            source: sourceUpdates[0]?.salon_id,
            related: related.map(r => r.salon.id),
            topics: [...new Set(sourceUpdates.map(u => u.topics).flat())],
            status: 'pending',
            created_at: new Date().toISOString()
        };
        
        this.fusionSessions.set(sessionId, session);
        
        // 创建融合会话
        const fusion = await this.emergenceDetector.create_fusion_session({
            session_id: sessionId,
            source_updates: sourceUpdates,
            related_salons: related
        });
        
        // 广播融合事件
        this.io?.emit('emergence:detected', {
            type: 'cross_salon_fusion',
            session_id: sessionId,
            topics: session.topics
        });
        
        return fusion;
    }
    
    async analyze(target) {
        // 分析目标（主题、胶囊、沙龙）
        if (typeof target === 'string') {
            // 如果是 ID，尝试获取对应实体
            const topic = this.knowledgeGraph.get_topic(target);
            if (topic) {
                return this._analyze_topic(topic);
            }
        }
        
        return {
            type: 'unknown',
            target,
            error: 'Target not found'
        };
    }
    
    async _analyze_topic(topic) {
        // 获取关联主题
        const related = this.knowledgeGraph.get_related_topics(topic.id);
        
        // 获取历史讨论
        const history = this.knowledgeGraph.get_topic_history(topic.id);
        
        // 计算影响力
        const impact = this._calculate_impact(topic, related, history);
        
        return {
            type: 'topic',
            id: topic.id,
            title: topic.title,
            domain: topic.domain,
            related_count: related.length,
            history_length: history.length,
            impact_score: impact,
            recommendations: this._generate_recommendations(topic, related)
        };
    }
    
    _calculate_impact(topic, related, history) {
        let score = 50; // 基础分
        
        // 关联主题加分
        score += related.length * 5;
        
        // 历史讨论加分
        score += Math.min(history.length * 2, 30);
        
        // 跨领域加分
        const domains = new Set([topic.domain, ...related.map(r => r.domain)]);
        score += (domains.size - 1) * 10;
        
        return Math.min(score, 100);
    }
    
    _generate_recommendations(topic, related) {
        const recommendations = [];
        
        if (related.length === 0) {
            recommendations.push({
                type: 'expand',
                message: '当前主题缺乏关联，建议扩展关键词'
            });
        }
        
        if (related.length > 3) {
            recommendations.push({
                type: 'merge',
                message: '发现多个关联主题，建议触发跨域融合'
            });
        }
        
        return recommendations;
    }
    
    async generate_insight(topic_ids) {
        // 生成跨主题洞察
        const topics = topic_ids.map(id => this.knowledgeGraph.get_topic(id)).filter(Boolean);
        
        if (topics.length < 2) {
            return {
                error: 'Need at least 2 topics',
                topics: topics.length
            };
        }
        
        // 分析共同点
        const common_keywords = this._find_common_keywords(topics);
        const common_domain = this._find_common_domain(topics);
        
        // 生成洞察
        const insight = {
            id: uuidv4(),
            type: 'cross_domain_insight',
            source_topics: topics.map(t => t.id),
            common_keywords,
            common_domain,
            generated_at: new Date().toISOString(),
            summary: this._generate_summary(topics, common_keywords, common_domain),
            recommendations: this._generate_insight_recommendations(topics)
        };
        
        // 保存到知识图谱
        await this.knowledgeGraph.add_insight(insight);
        
        return insight;
    }
    
    _find_common_keywords(topics) {
        const allKeywords = topics.flatMap(t => t.keywords || []);
        const counts = {};
        
        for (const kw of allKeywords) {
            counts[kw] = (counts[kw] || 0) + 1;
        }
        
        return Object.entries(counts)
            .filter(([_, count]) => count > 1)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([keyword]) => keyword);
    }
    
    _find_common_domain(topics) {
        const domains = topics.map(t => t.domain);
        const counts = {};
        
        for (const d of domains) {
            counts[d] = (counts[d] || 0) + 1;
        }
        
        return Object.entries(counts)
            .sort((a, b) => b[1] - a[1])[0]?.[0];
    }
    
    _generate_summary(topics, keywords, domain) {
        const titles = topics.map(t => t.title).join(' / ');
        return `跨领域洞察：${titles} 在 ${keywords.slice(0, 3).join('、')} 等方面存在关联，可进行深入探讨。`;
    }
    
    _generate_insight_recommendations(topics) {
        return [
            {
                type: 'discussion',
                message: '建议组织跨领域讨论会'
            },
            {
                type: 'capsule',
                message: '建议生成跨领域知识胶囊'
            },
            {
                type: 'research',
                message: '建议进一步研究关联领域'
            }
        ];
    }
}

module.exports = { KaiDison };
