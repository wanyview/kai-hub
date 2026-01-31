/**
 * BCI KaiDison: 脑机接口场景专门化
 * 
 * 继承基础 KaiDison，添加 BCI 专业能力
 */

const { KaiDison } = require('../orchestrator/kai-dison');
const { v4: uuidv4 } = require('uuid');

class BCIKaiDison extends KaiDison {
    constructor(config) {
        super(config);
        
        // BCI 专业配置
        this.bci_domains = [
            'neuroscience',
            'ai_algorithm',
            'materials_science',
            'medical_application',
            'ethics_society'
        ];
        
        // 关键技术指标
        this.bci_metrics = {
            'signal_accuracy': { target: 0.95, unit: '%' },
            'latency': { target: 50, unit: 'ms' },
            'stability': { target: 365, unit: 'days' },
            'bandwidth': { target: 1000, unit: 'channels' }
        };
        
        // 跨域关联映射
        this.cross_domain_mappings = {
            'neuroscience': ['ai_algorithm', 'medical_application'],
            'ai_algorithm': ['neuroscience', 'materials_science'],
            'materials_science': ['medical_application', 'ethics_society'],
            'medical_application': ['neuroscience', 'ethics_society'],
            'ethics_society': ['medical_application', 'materials_science']
        };
    }
    
    /**
     * BCI 场景监控
     */
    async monitor_bci_discussions() {
        const updates = {
            neuroscience: [],
            ai_algorithm: [],
            ethics_society: []
        };
        
        // 获取各沙龙更新
        const salons = this.salonManager.get_active_salons();
        
        for (const salon of salons) {
            const recent = await salon.adapter.get_recent_updates(salon.config);
            
            // 分类到 BCI 子领域
            for (const update of recent) {
                const domain = this._classify_bci_domain(update);
                if (updates[domain]) {
                    updates[domain].push(update);
                }
            }
        }
        
        // 检测跨域关联
        const correlations = await this._detect_bci_correlations(updates);
        
        // 检测技术突破
        const breakthroughs = await this._detect_bci_breakthroughs(updates);
        
        // 检测共识
        const consensus = await this._detect_bci_consensus(updates);
        
        return {
            correlations,
            breakthroughs,
            consensus,
            timestamp: new Date().toISOString()
        };
    }
    
    /**
     * 分类到 BCI 子领域
     */
    _classify_bci_domain(update) {
        const keywords = (update.keywords || []).map(k => k.toLowerCase());
        
        if (keywords.some(k => ['neuron', 'brain', 'cortex', 'synapse'].some(t => k.includes(t)))) {
            return 'neuroscience';
        }
        if (keywords.some(k => ['algorithm', 'decode', 'signal', 'model'].some(t => k.includes(t)))) {
            return 'ai_algorithm';
        }
        if (keywords.some(k => ['ethic', 'privacy', 'consent', 'society'].some(t => k.includes(t)))) {
            return 'ethics_society';
        }
        
        return 'general';
    }
    
    /**
     * 检测 BCI 跨域关联
     */
    async _detect_bci_correlations(updates) {
        const correlations = [];
        
        // 检查神经科学 <-> AI 关联
        if (updates.neuroscience.length > 0 && updates.ai_algorithm.length > 0) {
            const neuro_topics = updates.neuroscience.map(u => u.title).join(' ');
            const ai_topics = updates.ai_algorithm.map(u => u.title).join(' ');
            
            if (this._has_common_keywords(neuro_topics, ai_topics)) {
                correlations.push({
                    type: 'neuroscience_ai',
                    strength: 0.9,
                    description: '神经科学与AI算法高度关联',
                    recommendation: '建议组织神经科学家与AI专家的联合讨论'
                });
            }
        }
        
        // 检查 AI <-> 伦理关联
        if (updates.ai_algorithm.length > 0 && updates.ethics_society.length > 0) {
            correlations.push({
                type: 'ai_ethics',
                strength: 0.75,
                description: 'AI算法发展引发伦理讨论',
                recommendation: '建议将伦理考量纳入算法设计阶段'
            });
        }
        
        return correlations;
    }
    
    /**
     * 检测 BCI 技术突破
     */
    async _detect_bci_breakthroughs(updates) {
        const breakthroughs = [];
        const breakthrough_keywords = [
            '突破', '首次', '革命', '创新', 'record',
            'breakthrough', 'first', 'revolution', 'innovation'
        ];
        
        const allUpdates = [
            ...updates.neuroscience,
            ...updates.ai_algorithm
        ];
        
        for (const update of allUpdates) {
            const content = (update.title + ' ' + update.content).toLowerCase();
            
            if (breakthrough_keywords.some(kw => content.includes(kw.toLowerCase()))) {
                breakthroughs.push({
                    type: 'technical_breakthrough',
                    title: update.title,
                    domain: this._classify_bci_domain(update),
                    timestamp: update.timestamp,
                    significance: this._calculate_breakthrough_significance(update)
                });
            }
        }
        
        return breakthroughs;
    }
    
    /**
     * 检测 BCI 共识
     */
    async _detect_bci_consensus(updates) {
        // 检查是否有关于同一技术问题的一致结论
        const topics = {};
        
        [...updates.neuroscience, ...updates.ai_algorithm].forEach(update => {
            const key = this._extract_topic_key(update);
            if (!topics[key]) {
                topics[key] = [];
            }
            topics[key].push(update);
        });
        
        const consensus = [];
        
        for (const [key, topicUpdates] of Object.entries(topics)) {
            if (topicUpdates.length >= 2) {
                // 检查结论一致性
                const conclusions = topicUpdates.map(u => u.conclusion || u.insight);
                const similarity = this._calculate_text_similarity(conclusions);
                
                if (similarity > 0.8) {
                    consensus.push({
                        topic: key,
                        strength: similarity,
                        domains: [...new Set(topicUpdates.map(u => this._classify_bci_domain(u)))],
                        recommendation: `关于"${key}"已形成跨域共识`
                    });
                }
            }
        }
        
        return consensus;
    }
    
    /**
     * 生成 BCI 综合洞察
     */
    async generate_bci_insight(correlations, breakthroughs, consensus) {
        const sections = [];
        
        // 技术突破总结
        if (breakthroughs.length > 0) {
            sections.push(`🚀 **技术突破**\n${breakthroughs.map(b => `- ${b.title}`).join('\n')}`);
        }
        
        // 跨域关联
        if (correlations.length > 0) {
            sections.push(`🔗 **跨域关联**\n${correlations.map(c => `- ${c.description}`).join('\n')}`);
        }
        
        // 共识
        if (consensus.length > 0) {
            sections.push(`✅ **已达成共识**\n${consensus.map(c => `- ${c.topic}: ${c.recommendation}`).join('\n')}`);
        }
        
        // 建议下一步
        const next_steps = this._generate_bci_next_steps(correlations, breakthroughs, consensus);
        sections.push(`📋 **下一步行动**\n${next_steps.map(s => `- ${s}`).join('\n')}`);
        
        return {
            id: uuidv4(),
            type: 'bci_comprehensive_insight',
            title: '脑机接口跨学科综合洞察',
            content: sections.join('\n\n'),
            generated_at: new Date().toISOString(),
            metrics: {
                correlations: correlations.length,
                breakthroughs: breakthroughs.length,
                consensus: consensus.length
            }
        };
    }
    
    /**
     * 生成 BCI 下一步行动建议
     */
    _generate_bci_next_steps(correlations, breakthroughs, consensus) {
        const steps = [];
        
        // 基于突破建议
        if (breakthroughs.length > 0) {
            steps.push('组织技术验证实验，验证突破性成果');
        }
        
        // 基于关联建议
        if (correlations.some(c => c.type === 'neuroscience_ai')) {
            steps.push('安排神经科学家与AI专家的联合研讨会');
        }
        
        // 基于共识建议
        if (consensus.length > 0) {
            steps.push('将共识纳入BCI技术路线图');
        }
        
        // 通用建议
        steps.push('更新BCI知识图谱');
        steps.push('生成新的知识胶囊');
        
        return steps;
    }
    
    /**
     * 辅助方法：关键词检测
     */
    _has_common_keywords(text1, text2) {
        const words1 = new Set(text1.toLowerCase().split(/\s+/));
        const words2 = new Set(text2.toLowerCase().split(/\s+/));
        const common = [...words1].filter(w => words2.has(w));
        return common.length >= 2;
    }
    
    /**
     * 辅助方法：文本相似度
     */
    _calculate_text_similarity(texts) {
        if (texts.length < 2) return 0;
        
        const allWords = new Set(texts.flatMap(t => t.toLowerCase().split(/\s+/)));
        let totalSimilarity = 0;
        let comparisons = 0;
        
        for (let i = 0; i < texts.length; i++) {
            for (let j = i + 1; j < texts.length; j++) {
                const set1 = new Set(texts[i].toLowerCase().split(/\s+/));
                const set2 = new Set(texts[j].toLowerCase().split(/\s+/));
                const intersection = [...set1].filter(w => set2.has(w));
                const union = new Set([...set1, ...set2]);
                totalSimilarity += intersection.length / union.size;
                comparisons++;
            }
        }
        
        return comparisons > 0 ? totalSimilarity / comparisons : 0;
    }
    
    /**
     * 辅助方法：提取主题关键词
     */
    _extract_topic_key(update) {
        const keywords = (update.keywords || []).join(' ');
        return keywords.substring(0, 50) || update.title.substring(0, 50);
    }
    
    /**
     * 计算突破显著性
     */
    _calculate_breakthrough_significance(update) {
        let score = 50;
        
        // 基于关键词
        if (update.keywords?.some(k => ['首次', 'record', 'first'].includes(k))) {
            score += 30;
        }
        if (update.keywords?.some(k => ['革命', 'revolution'].includes(k))) {
            score += 20;
        }
        
        return Math.min(score, 100);
    }
    
    /**
     * 获取 BCI 状态
     */
    get_bci_status() {
        return {
            ...this.get_status(),
            bci_domains: this.bci_domains,
            metrics: this.bci_metrics
        };
    }
}

module.exports = { BCIKaiDison };
