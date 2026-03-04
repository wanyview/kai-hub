#!/usr/bin/env python3
"""
KaiDison 专业级数字科学家 (v2.0)
跨域关联引擎 + 突破检测 + 共识追踪 + 趋势预测
支持: 个人 + 团队 + 组织

核心理念: AI科学家 = 个人 + 团队 + 组织
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import urllib.request


@dataclass
class Capsule:
    """知识胶囊"""
    title: str
    domain: str
    topics: List[str]
    insight: str
    evidence: List[str]
    authors: List[str]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ============ v2.0 新增: 多类型 AI 科学家 ============

@dataclass
class IndividualScientist:
    """个人科学家"""
    id: str = field(default_factory=lambda: f"ind_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name: str = ""
    name_en: str = ""
    type: str = "individual"
    
    # 基本信息
    research_field: str = ""
    era: str = ""
    nationality: str = ""
    
    # 学术贡献
    contributions: List[str] = field(default_factory=list)
    publications: List[str] = field(default_factory=list)
    awards: List[str] = field(default_factory=list)
    
    # 思想风格
    thinking_style: str = ""
    personality: str = ""
    famous_quotes: List[str] = field(default_factory=list)
    
    # 关联
    mentors: List[str] = field(default_factory=list)
    collaborators: List[str] = field(default_factory=list)
    followers: List[str] = field(default_factory=list)


@dataclass
class ResearchTeam:
    """研究团队"""
    id: str = field(default_factory=lambda: f"team_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name: str = ""
    type: str = "team"
    
    # 基本信息
    organization: str = ""
    research_field: str = ""
    founded: str = ""
    
    # 成员
    leader: str = ""
    members: List[str] = field(default_factory=list)
    alumni: List[str] = field(default_factory=list)
    
    # 产出
    projects: List[str] = field(default_factory=list)
    publications: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    
    # 协作风格
    collaboration_style: str = ""
    culture: str = ""
    
    # 方法论
    methodology: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)


@dataclass
class ResearchOrganization:
    """研究组织"""
    id: str = field(default_factory=lambda: f"org_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    name: str = ""
    type: str = "organization"
    
    # 基本信息
    research_field: str = ""
    founded: str = ""
    location: str = ""
    
    # 结构
    structure: str = ""
    scale: str = ""
    
    # 领导层
    founders: List[str] = field(default_factory=list)
    leadership: List[str] = field(default_factory=list)
    
    # 历史
    milestones: List[str] = field(default_factory=list)
    spin_offs: List[str] = field(default_factory=list)
    
    # 产出
    labs: List[str] = field(default_factory=list)
    research_areas: List[str] = field(default_factory=list)
    
    # 文化
    mission: str = ""
    values: List[str] = field(default_factory=list)
    culture: str = ""
    research_philosophy: str = ""


@dataclass
class Association:
    """跨域关联"""
    domain_a: str
    domain_b: str
    strength: float  # 0-1
    topics: List[str]
    description: str
    recommendation: str


@dataclass
class Breakthrough:
    """技术突破"""
    title: str
    domains: List[str]
    significance: float  # 0-100
    evidence: List[str]
    type: str  # method/data/concept
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Consensus:
    """共识达成"""
    topic: str
    domains: List[str]
    strength: float  # 0-1
    positions: Dict[str, str]  # domain -> position
    evolution: List[Dict]  # 观点演化历史
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class CrossDomainEngine:
    """跨域关联引擎"""
    
    # 领域关键词映射（英文关键词）
    DOMAIN_KEYWORDS = {
        'neuroscience': ['neural', 'brain', 'cortex', 'neuron', 'synaptic', 'motor', 'sensory', 'neuroplasticity', 'brain'],
        'ai': ['ai', 'ml', 'deep learning', 'algorithm', 'neural network', 'model', 'decoding', 'end-to-end', 'personalized'],
        'ethics': ['ethics', 'privacy', 'fairness', 'rights', 'enhancement', 'privacy', 'access'],
        'materials': ['material', 'electrode', 'flexible', 'biocompatible', 'nano', 'polymer', 'conductive'],
        'medical': ['clinical', 'rehabilitation', 'therapy', 'patient', 'medical', 'treatment'],
        'physics': ['gravity', 'physics', 'force', 'quantum', 'mechanics'],
        'technology': ['technology', 'invention', 'device', 'innovation'],
        'climate': ['climate', 'environment', 'temperature', 'agriculture'],
        'biotech': ['synthetic biology', 'biology', 'genetic', 'bio']
    }
    
    # 中文关键词
    DOMAIN_KEYWORDS_CN = {
        'neuroscience': ['神经', '大脑', '皮层', '突触', '运动皮层', '感觉反馈', '神经可塑性'],
        'ai': ['AI', '机器学习', '深度学习', '解码', '算法', '神经网络', '端到端', '个性化'],
        'ethics': ['伦理', '隐私', '公平', '权利', '增强', '边界'],
        'materials': ['材料', '电极', '柔性', '生物相容', '纳米', '聚合物', '导电'],
        'medical': ['临床', '康复', '治疗', '患者', '医疗', '运动障碍'],
        'physics': ['重力', '物理', '力学', '量子'],
        'technology': ['技术', '发明', '创新', '设备'],
        'biotech': ['合成生物', '生物', '遗传']
    }
    
    def __init__(self):
        self.associations: List[Association] = []
    
    def extract_keywords(self, text: str) -> List[Tuple[str, str]]:
        """提取文本关键词（支持中英文）"""
        keywords = []
        text_lower = text.lower()
        
        for domain, words in self.DOMAIN_KEYWORDS.items():
            for word in words:
                if word.lower() in text_lower:
                    keywords.append((domain, word))
        
        for domain, words in self.DOMAIN_KEYWORDS_CN.items():
            for word in words:
                if word in text:
                    keywords.append((domain, word))
        
        return keywords
    
    def find_associations(self, capsules: List[Capsule]) -> List[Association]:
        """发现跨域关联"""
        associations = []
        
        # 按领域分组（标准化领域名称）
        by_domain = defaultdict(list)
        for capsule in capsules:
            domain = capsule.domain.lower().strip()
            # 标准化领域名称
            if domain in ['neuroscience', '神经科学']:
                domain = 'neuroscience'
            elif domain in ['ai', '人工智能']:
                domain = 'ai'
            elif domain in ['ethics', '伦理']:
                domain = 'ethics'
            elif domain in ['materials', '材料科学']:
                domain = 'materials'
            elif domain in ['medical', '医学']:
                domain = 'medical'
            elif domain in ['physics', '物理']:
                domain = 'physics'
            elif domain in ['technology', '技术']:
                domain = 'technology'
            elif domain in ['biotech', '合成生物']:
                domain = 'biotech'
            else:
                domain = domain  # 保持原样
            by_domain[domain].append(capsule)
        
        # 检查所有领域对
        domains = list(by_domain.keys())
        
        for i, d1 in enumerate(domains):
            for d2 in domains[i+1:]:
                # 计算关联强度
                strength = self._calculate_association_strength(
                    by_domain[d1], by_domain[d2]
                )
                
                if strength > 0.1:  # 降低阈值以检测更多关联
                    topics = self._find_common_topics(
                        by_domain[d1], by_domain[d2]
                    )
                    
                    assoc = Association(
                        domain_a=d1,
                        domain_b=d2,
                        strength=strength,
                        topics=topics,
                        description=f"{d1} 与 {d2} 在以下方面存在关联",
                        recommendation=self._generate_recommendation(d1, d2, topics)
                    )
                    associations.append(assoc)
        
        # 按强度排序
        associations.sort(key=lambda x: -x.strength)
        self.associations = associations[:10]  # 最多10个
        return self.associations
    
    def _calculate_association_strength(self, caps1: List[Capsule], caps2: List[Capsule]) -> float:
        """计算两个领域之间的关联强度"""
        if not caps1 or not caps2:
            return 0.0
        
        # 提取所有关键词
        keywords1 = set()
        keywords2 = set()
        
        for cap in caps1:
            kw = self.extract_keywords(cap.insight + ' ' + ' '.join(cap.topics))
            keywords1.update([w for _, w in kw])
        
        for cap in caps2:
            kw = self.extract_keywords(cap.insight + ' ' + ' '.join(cap.topics))
            keywords2.update([w for _, w in kw])
        
        # Jaccard 相似度
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _find_common_topics(self, caps1: List[Capsule], caps2: List[Capsule]) -> List[str]:
        """查找共同话题"""
        topics = set()
        for cap in caps1 + caps2:
            for t in cap.topics:
                topics.add(t)
        return list(topics)[:5]
    
    def _generate_recommendation(self, d1: str, d2: str, topics: List[str]) -> str:
        """生成建议"""
        return f"建议组织 {d1} 与 {d2} 领域的联合讨论会，重点探讨: {', '.join(topics[:3])}"


class BreakthroughDetector:
    """突破检测算法"""
    
    # 突破特征词
    BREAKTHROUGH_PATTERNS = {
        'method': [r'新方法', r'突破', r'创新', r'首次', r'端到端', r'革命性'],
        'data': [r'大规模', r'新数据', r'数据集', r'高分辨率', r'实时'],
        'concept': [r'新范式', r'理论', r'概念', r'框架', r'模型重构']
    }
    
    def __init__(self):
        self.breakthroughs: List[Breakthrough] = []
    
    def detect(self, capsules: List[Capsule]) -> List[Breakthrough]:
        """检测技术突破"""
        breakthroughs = []
        
        for capsule in capsules:
            # 分析每个胶囊
            text = capsule.insight + ' ' + ' '.join(capsule.topics)
            
            # 检测突破类型
            btype = self._detect_type(text)
            significance = self._calculate_significance(text, capsule.evidence)
            
            if significance > 60:  # 阈值
                bt = Breakthrough(
                    title=capsule.title,
                    domains=[capsule.domain],
                    significance=significance,
                    evidence=capsule.evidence,
                    type=btype
                )
                breakthroughs.append(bt)
        
        self.breakthroughs = breakthroughs
        return breakthroughs
    
    def _detect_type(self, text: str) -> str:
        """检测突破类型"""
        for btype, patterns in self.BREAKTHROUGH_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return btype
        return 'concept'  # 默认
    
    def _calculate_significance(self, text: str, evidence: List[str]) -> float:
        """计算突破重要性"""
        score = 0.0
        
        # 特征词匹配
        for patterns in self.BREAKTHROUGH_PATTERNS.values():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 15
        
        # 证据数量
        score += min(len(evidence) * 10, 30)
        
        # 领域交叉
        if len(set(text.split()) & {'跨学科', '融合', '结合', '集成'}):
            score += 20
        
        return min(score, 100)


class ConsensusTracker:
    """共识达成追踪"""
    
    def __init__(self):
        self.consensuses: List[Consensus] = []
        self.positions_history: Dict[str, List[Dict]] = defaultdict(list)
    
    def track(self, capsules: List[Capsule]) -> List[Consensus]:
        """追踪共识达成"""
        # 按话题分组
        by_topic = defaultdict(list)
        for capsule in capsules:
            for topic in capsule.topics:
                by_topic[topic].append(capsule)
        
        # 分析每个话题
        for topic, caps in by_topic.items():
            if len(caps) >= 2:  # 至少两个胶囊讨论同一话题
                consensus = self._analyze_consensus(topic, caps)
                if consensus:
                    self.consensuses.append(consensus)
        
        return self.consensuses
    
    def _analyze_consensus(self, topic: str, capsules: List[Capsule]) -> Optional[Consensus]:
        """分析共识"""
        # 收集各方观点
        positions = {}
        for cap in capsules:
            positions[cap.domain] = cap.insight[:200]
        
        # 计算一致性
        strength = self._calculate_agreement(positions)
        
        if strength > 0.6:  # 阈值
            return Consensus(
                topic=topic,
                domains=list(positions.keys()),
                strength=strength,
                positions=positions,
                evolution=self.positions_history.get(topic, [])
            )
        return None
    
    def _calculate_agreement(self, positions: Dict[str, str]) -> float:
        """计算观点一致性"""
        if len(positions) < 2:
            return 0.0
        
        # 简化的相似度计算
        texts = list(positions.values())
        
        # 检查关键词重叠
        keywords = [set(t.split()) for t in texts]
        intersection = keywords[0]
        for k in keywords[1:]:
            intersection = intersection & k
        
        union = keywords[0]
        for k in keywords[1:]:
            union = union | k
        
        return len(intersection) / len(union) if union else 0.0


class TrendPredictor:
    """趋势预测"""
    
    def __init__(self):
        self.trends: List[Dict] = []
    
    def predict(self, capsules: List[Capsule]) -> List[Dict]:
        """预测趋势"""
        # 统计话题频率
        topic_freq = defaultdict(int)
        domain_freq = defaultdict(int)
        
        for capsule in capsules:
            for topic in capsule.topics:
                topic_freq[topic] += 1
            domain_freq[capsule.domain] += 1
        
        # 识别上升趋势
        rising = []
        for topic, freq in sorted(topic_freq.items(), key=lambda x: -x[1])[:5]:
            rising.append({
                'topic': topic,
                'frequency': freq,
                'trend': 'rising' if freq > 3 else 'stable'
            })
        
        # 识别热门领域
        hot_domains = []
        for domain, freq in sorted(domain_freq.items(), key=lambda x: -x[1]):
            hot_domains.append({
                'domain': domain,
                'count': freq,
                'growth': 'high' if freq > 3 else 'medium'
            })
        
        self.trends = {
            'rising_topics': rising,
            'hot_domains': hot_domains,
            'prediction_period': 'next_3_months'
        }
        
        return [self.trends]


class KaiDisonProfessional:
    """KaiDison 专业级数字科学家"""
    
    def __init__(self, capsulehub_url: str = "http://localhost:8005"):
        self.name = "KaiDison"
        self.level = "Professional (L5)"
        self.capsulehub_url = capsulehub_url
        
        # 核心引擎
        self.cross_domain = CrossDomainEngine()
        self.breakthrough_detector = BreakthroughDetector()
        self.consensus_tracker = ConsensusTracker()
        self.trend_predictor = TrendPredictor()
        
        # 状态
        self.status = "active"
        self.last_scan = None
        self.stats = {
            "cross_domain_links": 0,
            "fusion_capsules": 0,
            "breakthroughs": 0,
            "consensus": 0
        }
    
    def scan_and_analyze(self) -> Dict:
        """扫描并分析所有胶囊"""
        print(f"\n{'='*60}")
        print(f"🔬 KaiDison 专业分析报告")
        print(f"{'='*60}\n")
        
        # 1. 获取胶囊
        print("📥 正在获取知识胶囊...")
        capsules = self._fetch_capsules()
        print(f"   获取到 {len(capsules)} 个胶囊\n")
        
        # 2. 跨域关联
        print("🔗 跨域关联分析...")
        associations = self.cross_domain.find_associations(capsules)
        self.stats["cross_domain_links"] = len(associations)
        for assoc in associations:
            print(f"   • {assoc.domain_a} ↔ {assoc.domain_b}: {assoc.strength:.1%}")
        print()
        
        # 3. 突破检测
        print("💥 技术突破检测...")
        breakthroughs = self.breakthrough_detector.detect(capsules)
        self.stats["breakthroughs"] = len(breakthroughs)
        for bt in breakthroughs:
            print(f"   • {bt.title[:35]}: {bt.significance:.0f}% ({bt.type})")
        print()
        
        # 4. 共识追踪
        print("🤝 共识达成追踪...")
        consensuses = self.consensus_tracker.track(capsules)
        self.stats["consensus"] = len(consensuses)
        for cs in consensuses:
            print(f"   • {cs.topic}: {cs.strength:.1%} ({len(cs.domains)}方)")
        print()
        
        # 5. 趋势预测
        print("🔮 趋势预测...")
        trends = self.trend_predictor.predict(capsules)
        if trends:
            t = trends[0]
            print(f"   上升话题: {', '.join([x['topic'] for x in t.get('rising_topics', [])[:3]])}")
            print(f"   热门领域: {', '.join([x['domain'] for x in t.get('hot_domains', [])[:3]])}")
        print()
        
        # 6. 生成融合胶囊
        print("🧬 生成融合胶囊...")
        fusion_capsules = self._generate_fusion_capsules(associations, breakthroughs, capsules)
        self.stats["fusion_capsules"] = len(fusion_capsules)
        for fc in fusion_capsules:
            print(f"   • {fc.title[:40]}")
        print()
        
        self.last_scan = datetime.utcnow().isoformat()
        
        return {
            "status": "success",
            "kaiDison": {
                "name": self.name,
                "level": self.level,
                "status": self.status,
                "last_scan": self.last_scan
            },
            "stats": self.stats,
            "associations": [
                {
                    "domains": [a.domain_a, a.domain_b],
                    "strength": a.strength,
                    "topics": a.topics,
                    "recommendation": a.recommendation
                }
                for a in associations
            ],
            "breakthroughs": [
                {
                    "title": b.title,
                    "significance": b.significance,
                    "type": b.type
                }
                for b in breakthroughs
            ],
            "consensus": [
                {
                    "topic": c.topic,
                    "domains": c.domains,
                    "strength": c.strength
                }
                for c in consensuses
            ],
            "trends": trends,
            "fusion_capsules": [
                {
                    "title": fc.title,
                    "domain": fc.domain,
                    "topics": fc.topics,
                    "insight": fc.insight
                }
                for fc in fusion_capsules
            ]
        }
    
    def _fetch_capsules(self) -> List[Capsule]:
        """从 CapsuleHub 获取胶囊"""
        capsules = []
        
        try:
            url = f"{self.capsulehub_url}/capsules?limit=100"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                for c in data.get("capsules", []):
                    # 解析 tags 作为 topics，content 片段作为 evidence
                    topics = c.get("tags", []) or []
                    # 从 content 中提取前200字符作为 evidence
                    evidence = [c.get("content", "")[:200]] if c.get("content") else []
                    authors = [c.get("author", "")] if c.get("author") else []
                    
                    capsules.append(Capsule(
                        title=c.get("title", ""),
                        domain=c.get("domain", ""),
                        topics=topics,
                        insight=c.get("content", "")[:300],
                        evidence=evidence,
                        authors=authors
                    ))
        except Exception as e:
            print(f"   ⚠️ 获取胶囊失败: {e}")
        
        return capsules
    
    def _generate_fusion_capsules(self, associations: List[Association], 
                                  breakthroughs: List[Breakthrough],
                                  capsules: List[Capsule]) -> List[Capsule]:
        """生成跨域融合胶囊"""
        fusion_capsules = []
        
        # 基于强关联生成融合胶囊（降低阈值）
        for assoc in associations:
            if assoc.strength > 0.05:  # 降低到5%
                fc = Capsule(
                    title=f"跨域融合: {assoc.domain_a} + {assoc.domain_b}",
                    domain=f"{assoc.domain_a}+{assoc.domain_b}",
                    topics=assoc.topics[:3] if assoc.topics else ['跨域融合'],
                    insight=f"通过跨域关联分析发现，{assoc.domain_a} 与 {assoc.domain_b} 存在 {assoc.strength:.1%} 的关联强度。建议两个领域的专家进行联合讨论，以促进知识融合和创新突破。",
                    evidence=[f"关联强度: {assoc.strength:.1%}", assoc.recommendation],
                    authors=["KaiDison"]
                )
                fusion_capsules.append(fc)
        
        # 基于突破生成融合胶囊
        for bt in breakthroughs:
            if bt.significance > 50:  # 降低到50%
                fc = Capsule(
                    title=f"突破融合: {bt.title}",
                    domain="+".join(bt.domains),
                    topics=bt.domains,
                    insight=f"技术突破检测发现: {bt.title} 具有 {bt.significance:.0f}% 的重要性评分。类型: {bt.type}。建议相关领域重点关注并跟进研究。",
                    evidence=bt.evidence,
                    authors=["KaiDison"]
                )
                fusion_capsules.append(fc)
        
        return fusion_capsules[:10]  # 最多10个
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "name": self.name,
            "level": self.level,
            "status": self.status,
            "last_scan": self.last_scan,
            "stats": self.stats
        }


def main():
    """主函数 - 运行 KaiDison 分析"""
    kaiDison = KaiDisonProfessional()
    
    # 运行分析
    result = kaiDison.scan_and_analyze()
    
    # 输出报告
    print(f"\n{'='*60}")
    print(f"📊 KaiDison 分析完成")
    print(f"{'='*60}")
    print(f"\n🔗 跨域关联: {result['stats']['cross_domain_links']}")
    print(f"💥 技术突破: {result['stats']['breakthroughs']}")
    print(f"🤝 共识达成: {result['stats']['consensus']}")
    print(f"🧬 融合胶囊: {result['stats']['fusion_capsules']}")
    
    # 保存报告
    report_path = "/Users/wanyview/clawd/kai-hub/reports/kai_dison_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存: {report_path}")
    
    return result


if __name__ == "__main__":
    import os
    main()


# ============ v2.0 新增: 多类型 AI 科学家预设 ============

# 团队预设
TEAM_PRESETS = {
    "OpenAI Safety Team": {
        "name": "OpenAI 安全团队",
        "organization": "OpenAI",
        "field": "AI Safety",
        "founded": "2020",
        "leader": "Ilya Sutskever",
        "members": ["Dario Amodei", "Jan Leike", "Paul Christiano"],
        "projects": ["GPT-4 Alignment", "Constitutional AI", "RLHF"],
        "collaboration_style": "跨学科协作",
        "culture": "安全优先",
        "methodology": ["RLHF", "Constitutional AI", "Scalable Oversight"]
    },
    "Apple Vision Pro Team": {
        "name": "Apple Vision Pro 团队",
        "organization": "Apple",
        "field": "AR/VR",
        "founded": "2018",
        "leader": "Mike Rockwell",
        "members": ["John Ternus", "Alan Dye"],
        "products": ["Apple Vision Pro", "visionOS"],
        "collaboration_style": "保密协作",
        "culture": "完美主义",
        "methodology": ["人机交互", "显示技术", "传感器融合"]
    },
    "DeepMind AlphaFold": {
        "name": "DeepMind AlphaFold 团队",
        "organization": "DeepMind",
        "field": "Computational Biology",
        "founded": "2016",
        "leader": "Demis Hassabis",
        "members": ["John Jumper", "David Baker"],
        "projects": ["AlphaFold 1", "AlphaFold 2", "AlphaFold 3"],
        "collaboration_style": "AI + 生物学家",
        "culture": "科学突破",
        "methodology": ["深度学习", "蛋白质结构预测", "生物信息学"]
    }
}

# 组织预设
ORG_PRESETS = {
    "Harvard University": {
        "name": "哈佛大学",
        "field": "综合性大学",
        "founded": "1636",
        "location": "马萨诸塞州剑桥市",
        "structure": "学院制",
        "scale": "20000+ 学生",
        "founders": ["John Harvard"],
        "leadership": ["Claudine Gay"],
        "milestones": ["建立美国第一所大学", "拉德克利夫学院合并"],
        "labs": ["哈佛医学院", "哈佛法学院", "哈佛商学院"],
        "research_areas": ["医学", "法学", "经济学", "计算机科学"],
        "mission": "追求真理，服务社会",
        "culture": "学术自由，精英教育",
        "research_philosophy": "基础研究与应用并重"
    },
    "Bell Labs": {
        "name": "贝尔实验室",
        "field": "通信与计算",
        "founded": "1925",
        "location": "新泽西州默里山",
        "structure": "企业研究院",
        "scale": "3000+ 研究员",
        "founders": ["AT&T", "Western Electric"],
        "milestones": ["晶体管发明", "激光理论", "Unix操作系统", "C语言"],
        "spin_offs": ["朗讯科技"],
        "labs": ["计算科学中心", "物理实验室"],
        "research_areas": ["通信", "计算机", "物理", "材料"],
        "mission": "发明促进人类进步的技术",
        "culture": "基础研究导向，长期投入",
        "research_philosophy": "好奇心驱动，自由探索"
    },
    "MIT Media Lab": {
        "name": "MIT 媒体实验室",
        "field": "媒体技术与设计",
        "founded": "1985",
        "location": "马萨诸塞州剑桥市",
        "structure": "跨学科实验室",
        "scale": "500+ 成员",
        "founders": ["Nicholas Negroponte", "Jerome Wiesner"],
        "leadership": ["Dava Newman"],
        "milestones": ["电子墨水", "可穿戴计算", "One Laptop per Child"],
        "research_areas": ["人机交互", "人工智能", "设计", "生物工程"],
        "mission": "创造有前景的突破性技术",
        "culture": "反传统，跨学科，开放",
        "research_philosophy": "反学科，逆向设计"
    },
    "DeepMind": {
        "name": "DeepMind",
        "field": "人工智能",
        "founded": "2010",
        "location": "伦敦",
        "structure": "企业研究院",
        "scale": "1000+ 员工",
        "founders": ["Demis Hassabis", "Mustafa Suleyman", "Shane Legg"],
        "leadership": ["Demis Hassabis (CEO)"],
        "milestones": ["AlphaGo", "AlphaFold", "AlphaCode"],
        "spin_offs": ["Isomorphic Labs"],
        "research_areas": ["深度学习", "强化学习", "蛋白质结构", "游戏AI"],
        "mission": "解决智能问题，推动科学突破",
        "culture": "科学优先，开放研究",
        "research_philosophy": "通用人工智能"
    }
}


# ============ v2.0 新增: 扩展分析方法 ============

def analyze_entity_interaction(
    entity_a: Dict,
    entity_b: Dict,
    context: str = ""
) -> Dict:
    """分析两个实体的交互"""
    
    type_a = entity_a.get('type', 'individual')
    type_b = entity_b.get('type', 'individual')
    
    # 分析类型组合
    analysis = {
        "entity_a": entity_a,
        "entity_b": entity_b,
        "type_pair": (type_a, type_b),
        "context": context,
        "insights": []
    }
    
    # 个人 vs 个人
    if type_a == 'individual' and type_b == 'individual':
        analysis["insights"].append("两位个人科学家的思想碰撞")
        if entity_a.get('field') != entity_b.get('field'):
            analysis["insights"].append(f"跨领域关联: {entity_a['field']} ↔ {entity_b['field']}")
    
    # 团队 vs 组织
    elif type_a == 'team' and type_b == 'organization':
        analysis["insights"].append(f"团队 {entity_a['name']} 在 {entity_b['name']} 中的角色")
        analysis["insights"].append(f"团队文化: {entity_a['culture']}")
        analysis["insights"].append(f"组织使命: {entity_b['mission']}")
    
    # 组织 vs 组织
    elif type_a == 'organization' and type_b == 'organization':
        analysis["insights"].append(f"两家研究机构的比较分析")
        analysis["insights"].append(f"{entity_a['name']} 文化: {entity_a['culture']}")
        analysis["insights"].append(f"{entity_b['name']} 文化: {entity_b['culture']}")
        if entity_a.get('research_philosophy') != entity_b.get('research_philosophy'):
            analysis["insights"].append("研究哲学差异: 可产生新的研究范式")
    
    # 混合类型
    else:
        analysis["insights"].append(f"混合类型分析: {type_a} + {type_b}")
        analysis["insights"].append("可产生跨尺度的创新洞见")
    
    return analysis


# ============ v2.0 便捷函数 ============

def create_entity(entity_type: str, name: str, **kwargs) -> Dict:
    """创建实体快捷函数"""
    entity = {
        "type": entity_type,
        "name": name,
        **kwargs
    }
    return entity


def run_v2_analysis(
    entities: List[Dict],
    topic: str
) -> Dict:
    """运行 v2.0 分析"""
    results = {
        "topic": topic,
        "entities": entities,
        "interactions": [],
        "summary": ""
    }
    
    # 分析所有配对
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            interaction = analyze_entity_interaction(
                entities[i],
                entities[j],
                topic
            )
            results["interactions"].append(interaction)
    
    # 生成总结
    entity_types = [e['type'] for e in entities]
    unique_types = set(entity_types)
    
    if len(unique_types) == 1:
        results["summary"] = f"同类型实体分析: {list(unique_types)[0]}"
    else:
        results["summary"] = f"多类型混合分析: {' + '.join(sorted(unique_types))}"
    
    return results
