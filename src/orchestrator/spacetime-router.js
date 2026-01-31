/**
 * SpacetimeRouter: 时空路由器
 * 根据主题的时空属性路由知识
 * 
 * 空间维度：主题领域、参与者背景
 * 时间维度：讨论阶段、历史积累
 */

class SpacetimeRouter {
    constructor(config = {}) {
        this.threshold = config.threshold || 0.7;
        this.weights = config.weights || {
            domain: 0.3,
            keyword: 0.3,
            temporal: 0.2,
            spatial: 0.2
        };
    }
    
    /**
     * 计算两个胶囊之间的关联度
     */
    calculate_relevance(capsuleA, capsuleB) {
        const scores = {
            domain: this._domain_similarity(capsuleA.domain, capsuleB.domain),
            keyword: this._keyword_overlap(capsuleA.keywords, capsuleB.keywords),
            temporal: this._temporal_proximity(capsuleA.created_at, capsuleB.created_at),
            spatial: this._spatial_proximity(capsuleA, capsuleB)
        };
        
        const total = 
            scores.domain * this.weights.domain +
            scores.keyword * this.weights.keyword +
            scores.temporal * this.weights.temporal +
            scores.spatial * this.weights.spatial;
        
        return {
            score: total,
            breakdown: scores,
            related: total >= this.threshold
        };
    }
    
    /**
     * 域相似度计算
     */
    _domain_similarity(domainA, domainB) {
        if (!domainA || !domainB) return 0;
        
        // 精确匹配
        if (domainA === domainB) return 1.0;
        
        // 相似领域（需要领域映射表）
        const similar_domains = {
            'AI': ['technology', 'science', 'computer-science'],
            'physics': ['science', 'astronomy', 'mathematics'],
            'biology': ['science', 'medicine', 'chemistry'],
            'technology': ['AI', 'engineering', 'science'],
            'philosophy': ['humanities', 'social-science', 'ethics']
        };
        
        const similar = similar_domains[domainA] || [];
        return similar.includes(domainB) ? 0.8 : 0;
    }
    
    /**
     * 关键词重叠度
     */
    _keyword_overlap(keywordsA, keywordsB) {
        if (!keywordsA || !keywordsB || keywordsA.length === 0 || keywordsB.length === 0) {
            return 0;
        }
        
        const setA = new Set(keywordsA.map(k => k.toLowerCase()));
        const setB = new Set(keywordsB.map(k => k.toLowerCase()));
        
        const intersection = [...setA].filter(k => setB.has(k));
        const union = new Set([...setA, ...setB]);
        
        return intersection.length / union.size;
    }
    
    /**
     * 时间邻近度
     */
    _temporal_proximity(timeA, timeB) {
        if (!timeA || !timeB) return 0.5;
        
        const dateA = new Date(timeA);
        const dateB = new Date(timeB);
        
        const diffMs = Math.abs(dateA - dateB);
        const diffDays = diffMs / (1000 * 60 * 60 * 24);
        
        // 7天内为高邻近度
        if (diffDays <= 7) return 1.0;
        // 30天内为中等
        if (diffDays <= 30) return 0.7;
        // 90天内为低
        if (diffDays <= 90) return 0.4;
        return 0.2;
    }
    
    /**
     * 空间邻近度（基于领域和参与者）
     */
    _spatial_proximity(capsuleA, capsuleB) {
        let score = 0;
        
        // 同一作者或团队
        if (capsuleA.authors && capsuleB.authors) {
            const intersection = capsuleA.authors.filter(a => 
                capsuleB.authors.includes(a)
            );
            if (intersection.length > 0) {
                score += 0.5;
            }
        }
        
        // 同一来源沙龙
        if (capsuleA.source_salon === capsuleB.source_salon) {
            score += 0.3;
        }
        
        // 同一讨论主题
        if (capsuleA.topic_id === capsuleB.topic_id) {
            score += 0.2;
        }
        
        return Math.min(score, 1.0);
    }
    
    /**
     * 路由决策
     */
    route(capsule, context = {}) {
        const { recent_capsules = [] } = context;
        
        // 计算与最近胶囊的关联度
        const relevances = recent_capsules.map(recent => ({
            capsule: recent,
            relevance: this.calculate_relevance(capsule, recent)
        }));
        
        // 找到最相关的胶囊
        const sorted = relevances.sort((a, b) => b.relevance.score - a.relevance.score);
        const best = sorted[0];
        
        if (best && best.relevance.related) {
            return {
                action: 'fuse',
                target: best.capsule.id,
                confidence: best.relevance.score,
                reason: `与"${best.capsule.title}"高度相关`
            };
        }
        
        return {
            action: 'archive',
            confidence: 0.8,
            reason: '未发现强关联，建议独立存储'
        };
    }
    
    /**
     * 批量路由
     */
    batch_route(capsules, context = {}) {
        return capsules.map(capsule => ({
            capsule: capsule.id,
            route: this.route(capsule, context)
        }));
    }
    
    /**
     * 聚类
     */
    cluster(capsules) {
        const clusters = [];
        const unclustered = [...capsules];
        
        while (unclustered.length > 0) {
            const capsule = unclustered.shift();
            const cluster = {
                id: `cluster_${clusters.length}`,
                capsules: [capsule],
                centroid: {
                    domain: capsule.domain,
                    keywords: capsule.keywords || []
                },
                size: 1
            };
            
            // 找到所有相关的胶囊
            const remaining = [];
            for (const other of unclustered) {
                const relevance = this.calculate_relevance(capsule, other);
                if (relevance.related) {
                    cluster.capsules.push(other);
                    cluster.size++;
                } else {
                    remaining.push(other);
                }
            }
            
            unclustered.length = 0;
            unclustered.push(...remaining);
            
            if (cluster.size > 0) {
                clusters.push(cluster);
            }
        }
        
        return clusters;
    }
}

module.exports = { SpacetimeRouter };
