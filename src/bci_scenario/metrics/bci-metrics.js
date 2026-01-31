/**
 * BCI Metrics: 脑机接口场景评估指标
 */

class BCIMetrics {
    constructor() {
        // 核心指标定义
        this.metrics = {
            // 技术指标
            signal_accuracy: {
                name: '信号解码准确率',
                unit: '%',
                target: 95,
                current: 0,
                history: []
            },
            decoding_latency: {
                name: '解码延迟',
                unit: 'ms',
                target: 50,
                current: 0,
                history: []
            },
            
            // 知识关联指标
            cross_domain_links: {
                name: '跨域关联数',
                unit: '个',
                target: 20,
                current: 0,
                history: []
            },
            fusion_capsules: {
                name: '融合知识胶囊',
                unit: '个',
                target: 10,
                current: 0,
                history: []
            },
            
            // 涌现指标
            breakthroughs: {
                name: '技术突破检测',
                unit: '个',
                target: 5,
                current: 0,
                history: []
            },
            consensus: {
                name: '跨域共识达成',
                unit: '个',
                target: 5,
                current: 0,
                history: []
            },
            
            // 参与指标
            active_agents: {
                name: '活跃Agent数',
                unit: '个',
                target: 12,
                current: 0,
                history: []
            },
            discussion_rounds: {
                name: '讨论轮次',
                unit: '轮',
                target: 50,
                current: 0,
                history: []
            }
        };
    }
    
    /**
     * 更新指标
     */
    update(metric_name, value) {
        if (!this.metrics[metric_name]) {
            console.warn(`Unknown metric: ${metric_name}`);
            return;
        }
        
        const metric = this.metrics[metric_name];
        metric.current = value;
        metric.history.push({
            value,
            timestamp: new Date().toISOString()
        });
        
        // 保留最近100条历史
        if (metric.history.length > 100) {
            metric.history.shift();
        }
    }
    
    /**
     * 获取指标状态
     */
    get_status() {
        const status = {};
        
        for (const [name, metric] of Object.entries(this.metrics)) {
            const progress = metric.target > 0 
                ? Math.min(100, (metric.current / metric.target) * 100)
                : 0;
            
            status[name] = {
                ...metric,
                progress: Math.round(progress),
                status: progress >= 100 ? 'completed' : 
                       progress >= 70 ? 'on_track' :
                       progress >= 40 ? 'in_progress' : 'needs_attention'
            };
        }
        
        return status;
    }
    
    /**
     * 生成评估报告
     */
    generate_report() {
        const status = this.get_status();
        const sections = [];
        
        // 技术进展
        const techMetrics = ['signal_accuracy', 'decoding_latency'];
        const techStatus = techMetrics.map(m => status[m]);
        sections.push(this._format_section('🔬 技术进展', techStatus));
        
        // 知识协同
        const knowledgeMetrics = ['cross_domain_links', 'fusion_capsules'];
        const knowledgeStatus = knowledgeMetrics.map(m => status[m]);
        sections.push(this._format_section('🔗 知识协同', knowledgeStatus));
        
        // 涌现检测
        const emergenceMetrics = ['breakthroughs', 'consensus'];
        const emergenceStatus = emergenceMetrics.map(m => status[m]);
        sections.push(this._format_section('💡 涌现检测', emergenceStatus));
        
        // 参与度
        const participationMetrics = ['active_agents', 'discussion_rounds'];
        const participationStatus = participationMetrics.map(m => status[m]);
        sections.push(this._format_section('👥 参与度', participationStatus));
        
        // 总体评估
        const overallScore = this._calculate_overall_score(status);
        sections.unshift(this._format_overall(overallScore));
        
        return {
            report: sections.join('\n\n'),
            score: overallScore,
            status,
            generated_at: new Date().toISOString()
        };
    }
    
    /**
     * 格式化章节
     */
    _format_section(title, metrics) {
        const lines = [`**${title}**`];
        
        for (const metric of metrics) {
            const emoji = metric.status === 'completed' ? '✅' :
                         metric.status === 'on_track' ? '🟢' :
                         metric.status === 'in_progress' ? '🟡' : '🔴';
            
            lines.push(`${emoji} ${metric.name}: ${metric.current}${metric.unit} / ${metric.target}${metric.unit} (${metric.progress}%)`);
        }
        
        return lines.join('\n');
    }
    
    /**
     * 格式化总体评估
     */
    _format_overall(score) {
        let assessment = '📊 BCI 场景评估';
        
        if (score >= 80) {
            assessment += '\n\n🌟 **优秀**：各项指标达到预期，跨域协同效果显著';
        } else if (score >= 60) {
            assessment += '\n\n👍 **良好**：大部分指标进展顺利，需要关注薄弱环节';
        } else if (score >= 40) {
            assessment += '\n\n⚠️ **进行中**：部分指标滞后，需要加强投入';
        } else {
            assessment += '\n\n🚨 **需要关注**：多个指标未达预期，需要重新评估策略';
        }
        
        return assessment;
    }
    
    /**
     * 计算总体评分
     */
    _calculate_overall_score(status) {
        const metrics = Object.values(status);
        const weights = {
            signal_accuracy: 0.25,
            decoding_latency: 0.15,
            cross_domain_links: 0.2,
            fusion_capsules: 0.15,
            breakthroughs: 0.1,
            consensus: 0.1,
            active_agents: 0.025,
            discussion_rounds: 0.025
        };
        
        let weightedSum = 0;
        let totalWeight = 0;
        
        for (const [name, metric] of Object.entries(status)) {
            if (weights[name] !== undefined) {
                weightedSum += metric.progress * weights[name];
                totalWeight += weights[name];
            }
        }
        return Math.round(weightedSum / totalWeight);
    }
    
    /**
     * 导出指标数据
     */
    export() {
        return {
            metrics: this.metrics,
            exported_at: new Date().toISOString()
        };
    }
    
    /**
     * 导入指标数据
     */
    import(data) {
        if (data.metrics) {
            this.metrics = data.metrics;
        }
    }
}

module.exports = { BCIMetrics };
