/**
 * EmergenceDetector: 涌现检测器
 * 检测跨沙龙的知识涌现并触发融合
 */

const { v4: uuidv4 } = require('uuid');

class EmergenceDetector {
    constructor(knowledgeGraph) {
        this.knowledgeGraph = knowledgeGraph;
        this.fusionSessions = new Map();
        this.emergence_patterns = [
            {
                name: 'cross_domain_insight',
                description: '跨领域洞察涌现',
                trigger: (data) => this._detect_cross_domain(data)
            },
            {
                name: 'consensus_emergence',
                description: '共识涌现',
                trigger: (data) => this._detect_consensus(data)
            },
            {
                name: 'divergence_emergence',
                description: '分歧涌现',
                trigger: (data) => this._detect_divergence(data)
            },
            {
                name: 'breakthrough_emergence',
                description: '突破涌现',
                trigger: (data) => this._detect_breakthrough(data)
            }
        ];
    }
    
    /**
     * 检查所有模式
     */
    check_all() {
        const emergences = [];
        const recentTopics = this.knowledgeGraph.query_topics({ limit: 50 });
        
        for (const pattern of this.emergence_patterns) {
            const result = pattern.trigger(recentTopics);
            if (result) {
                emergences.push({
                    pattern: pattern.name,
                    description: pattern.description,
                    ...result
                });
            }
        }
        
        return emergences;
    }
    
    /**
     * 检测跨领域涌现
     */
    _detect_cross_domain(topics) {
        // 找出跨领域关联的主题群
        const domainGroups = {};
        
        for (const topic of topics) {
            const domain = topic.domain || 'unknown';
            if (!domainGroups[domain]) {
                domainGroups[domain] = [];
            }
            domainGroups[domain].push(topic);
        }
        
        const domains = Object.keys(domainGroups);
        
        // 找到有共同关键词的跨领域主题
        const connections = [];
        
        for (let i = 0; i < domains.length; i++) {
            for (let j = i + 1; j < domains.length; j++) {
                const groupA = domainGroups[domains[i]];
                const groupB = domainGroups[domains[j]];
                
                // 检查共同关键词
                const keywordsA = new Set(groupA.flatMap(t => t.keywords || []));
                const keywordsB = new Set(groupB.flatMap(t => t.keywords || []));
                const common = [...keywordsA].filter(k => keywordsB.has(k));
                
                if (common.length >= 2) {
                    connections.push({
                        domain_a: domains[i],
                        domain_b: domains[j],
                        common_keywords: common.slice(0, 5),
                        strength: common.length / Math.max(keywordsA.size, keywordsB.size)
                    });
                }
            }
        }
        
        if (connections.length > 0) {
            return {
                type: 'cross_domain',
                connections,
                recommendation: '发现跨领域关键词关联，建议触发融合讨论'
            };
        }
        
        return null;
    }
    
    /**
     * 检测共识涌现
     */
    _detect_consensus(topics) {
        // 查找高度相似的主题（可能达成共识）
        const similarGroups = [];
        
        for (let i = 0; i < topics.length; i++) {
            const topicA = topics[i];
            const group = [topicA];
            
            for (let j = i + 1; j < topics.length; j++) {
                const topicB = topics[j];
                
                // 计算相似度
                const similarity = this._calculate_similarity(topicA, topicB);
                
                if (similarity > 0.8) {
                    group.push(topicB);
                }
            }
            
            if (group.length >= 2) {
                similarGroups.push(group);
                i += group.length - 1; // 跳过已分组的主题
            }
        }
        
        if (similarGroups.length > 0) {
            return {
                type: 'consensus',
                groups: similarGroups.map(g => ({
                    topics: g.map(t => t.id),
                    titles: g.map(t => t.title)
                })),
                recommendation: '发现多个相似主题，可能已形成共识'
            };
        }
        
        return null;
    }
    
    /**
     * 检测分歧涌现
     */
    _detect_divergence(topics) {
        // 查找在同一领域但关键词差异大的主题
        const divergentTopics = [];
        
        const domainGroups = {};
        for (const topic of topics) {
            const domain = topic.domain || 'unknown';
            if (!domainGroups[domain]) {
                domainGroups[domain] = [];
            }
            domainGroups[domain].push(topic);
        }
        
        for (const [domain, groupTopics] of Object.entries(domainGroups)) {
            if (groupTopics.length < 2) continue;
            
            // 计算组内关键词差异
            const allKeywords = groupTopics.flatMap(t => t.keywords || []);
            const keywordCounts = {};
            
            for (const kw of allKeywords) {
                keywordCounts[kw] = (keywordCounts[kw] || 0) + 1;
            }
            
            // 找出低频关键词（代表分歧）
            const divergentKeywords = Object.entries(keywordCounts)
                .filter(([_, count]) => count === 1)
                .map(([kw]) => kw);
            
            if (divergentKeywords.length > 3) {
                divergentTopics.push({
                    domain,
                    count: groupTopics.length,
                    divergent_keywords: divergentKeywords.slice(0, 10)
                });
            }
        }
        
        if (divergentTopics.length > 0) {
            return {
                type: 'divergence',
                areas: divergentTopics,
                recommendation: '发现多个分歧点，建议组织讨论澄清'
            };
        }
        
        return null;
    }
    
    /**
     * 检测突破涌现
     */
    _detect_breakthrough(topics) {
        // 查找具有高创新性关键词的主题
        const breakthroughKeywords = [
            '突破', '创新', '革命', '范式转换', '首次', '新发现', 
            'revolution', 'breakthrough', 'paradigm', 'innovation'
        ];
        
        const breakthroughs = topics.filter(topic => {
            const keywords = (topic.keywords || []).map(k => k.toLowerCase());
            return breakthroughKeywords.some(bk => 
                keywords.some(k => k.includes(bk.toLowerCase()))
            );
        });
        
        if (breakthroughs.length > 0) {
            return {
                type: 'breakthrough',
                count: breakthroughs.length,
                topics: breakthroughs.map(t => ({
                    id: t.id,
                    title: t.title
                })),
                recommendation: '发现突破性主题，建议重点关注和深入研究'
            };
        }
        
        return null;
    }
    
    /**
     * 触发融合会话
     */
    async create_fusion_session(config) {
        const session = {
            id: config.session_id || uuidv4(),
            type: 'cross_salon_fusion',
            source_updates: config.source_updates,
            related_salons: config.related_salons,
            status: 'pending',
            created_at: new Date().toISOString()
        };
        
        this.fusionSessions.set(session.id, session);
        
        // 保存到知识图谱
        await this.knowledgeGraph.add_insight({
            id: session.id,
            type: 'fusion_session',
            source_topics: config.source_updates?.map(u => u.topic_id) || [],
            summary: `融合会话：${config.related_salons?.length || 0} 个沙龙参与`,
            recommendations: []
        });
        
        return session;
    }
    
    /**
     * 触发跨领域融合
     */
    async trigger_fusion(topic_ids) {
        const topics = topic_ids.map(id => this.knowledgeGraph.get_topic(id)).filter(Boolean);
        
        if (topics.length < 2) {
            return { error: 'Need at least 2 topics' };
        }
        
        // 检测跨领域关联
        const crossDomain = this._detect_cross_domain(topics);
        
        if (crossDomain) {
            const session = await this.create_fusion_session({
                session_id: uuidv4(),
                source_updates: topics,
                related_salons: [...new Set(topics.map(t => t.salon_id))]
            });
            
            return {
                status: 'fusion_triggered',
                session_id: session.id,
                emergence: crossDomain
            };
        }
        
        return {
            status: 'no_emergence',
            message: '未检测到足够的关联性'
        };
    }
    
    /**
     * 计算主题相似度
     */
    _calculate_similarity(topicA, topicB) {
        // 标题相似度
        const titleSim = this._text_similarity(topicA.title, topicB.title);
        
        // 关键词相似度
        const keywordsA = new Set((topicA.keywords || []).map(k => k.toLowerCase()));
        const keywordsB = new Set((topicB.keywords || []).map(k => k.toLowerCase()));
        
        if (keywordsA.size === 0 || keywordsB.size === 0) {
            return titleSim;
        }
        
        const intersection = [...keywordsA].filter(k => keywordsB.has(k));
        const union = new Set([...keywordsA, ...keywordsB]);
        const keywordSim = intersection.length / union.size;
        
        // 领域相同加分
        const domainBonus = topicA.domain === topicB.domain ? 0.1 : 0;
        
        return titleSim * 0.3 + keywordSim * 0.6 + domainBonus;
    }
    
    /**
     * 计算文本相似度
     */
    _text_similarity(textA, textB) {
        const wordsA = new Set(textA.toLowerCase().split(/\s+/));
        const wordsB = new Set(textB.toLowerCase().split(/\s+/));
        
        if (wordsA.size === 0 || wordsB.size === 0) return 0;
        
        const intersection = [...wordsA].filter(w => wordsB.has(w));
        const union = new Set([...wordsA, ...wordsB]);
        
        return intersection.length / union.size;
    }
}

module.exports = { EmergenceDetector };
