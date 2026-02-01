#!/usr/bin/env python3
"""
Capsule Collision System - Enhanced Version
知识胶囊自涌现系统 - 增强版

功能:
1. 使用预训练模型向量化
2. 多种碰撞策略
3. 实时碰撞检测
4. 高质量涌现胶囊自动发布
"""

import json
import os
import math
import time
from typing import Dict, List, Tuple, Optional, Set, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict

import urllib.request
import threading
import hashlib


# ========== 配置 ==========

@dataclass
class CapsuleData:
    """胶囊数据"""
    id: str
    title: str
    domain: str
    topics: List[str]
    insight: str
    evidence: List[str]
    action_items: List[str]
    authors: List[str]
    datm_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class CapsuleVector:
    """胶囊向量"""
    id: str
    title: str
    domain: str
    topics: List[str]
    insight: str
    embedding: List[float]
    metadata: Dict = field(default_factory=dict)


@dataclass
class CollisionPair:
    """碰撞对"""
    capsule_a: CapsuleVector
    capsule_b: CapsuleVector
    similarity: float
    collision_type: str
    shared_topics: List[str]
    collision_id: str = ""


@dataclass
class EmergedCapsule:
    """涌现胶囊"""
    title: str
    domain: str
    topics: List[str]
    insight: str
    evidence: List[str]
    action_items: List[str]
    parent_ids: List[str]
    collision_type: str
    emergence_score: float
    embedding: List[float] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class EmbeddingProvider:
    """向量化提供者 - 支持多种模型"""
    
    def __init__(self, provider: str = "simple"):
        self.provider = provider
        self._model = None
        self._initialize()
    
    def _initialize(self):
        """初始化模型"""
        if self.provider == "simple":
            # 使用简单的词向量
            self._load_simple_model()
        elif self.provider == "sentence-transformers":
            # 使用 sentence-transformers
            self._load_st_model()
        elif self.provider == "openai":
            # OpenAI embedding
            pass
    
    def _load_simple_model(self):
        """加载简单模型"""
        self.DOMAIN_KEYWORDS = {
            'neuroscience': ['神经', '大脑', '皮层', '神经元', '信号', '运动', '感觉', '可塑性', 
                            'neural', 'brain', 'cortex', 'neuron', 'motor', 'sensory'],
            'ai': ['AI', '机器学习', '深度学习', '算法', '解码', '模型', '神经网络', '端到端',
                   'ai', 'ml', 'deep learning', 'algorithm', 'decoding', 'neural network'],
            'ethics': ['伦理', '隐私', '公平', '权利', '增强', '边界', '认知',
                      'ethics', 'privacy', 'fairness', 'rights', 'enhancement'],
            'materials': ['材料', '电极', '柔性', '生物相容', '纳米', '导电',
                         'material', 'electrode', 'flexible', 'biocompatible'],
            'medical': ['临床', '康复', '治疗', '患者', '运动障碍',
                       'clinical', 'rehabilitation', 'therapy', 'patient'],
            'physics': ['重力', '物理', '力学', '量子', '运动',
                       'gravity', 'physics', 'quantum', 'mechanics'],
            'technology': ['技术', '发明', '创新', '设备', '系统',
                          'technology', 'invention', 'innovation', 'device'],
            'biotech': ['生物', '合成', '遗传', '基因', '生命',
                       'biology', 'synthetic', 'genetic', 'gene']
        }
        
        # 所有关键词列表
        self.all_keywords = set()
        for keywords in self.DOMAIN_KEYWORDS.values():
            self.all_keywords.update(keywords)
    
    def _load_st_model(self):
        """加载 sentence-transformers 模型"""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ 使用 sentence-transformers 向量化")
        except ImportError:
            print("⚠️ sentence-transformers 未安装，回退到简单模型")
            self.provider = "simple"
            self._load_simple_model()
    
    def get_embedding(self, text: str) -> List[float]:
        """获取文本向量"""
        if self.provider == "simple":
            return self._simple_embedding(text)
        elif self.provider == "sentence-transformers" and self._model:
            return self._st_embedding(text)
        else:
            return self._simple_embedding(text)
    
    def _simple_embedding(self, text: str) -> List[float]:
        """简单向量化"""
        text_lower = text.lower()
        vector = []
        
        # 领域向量 (8维)
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            vector.append(score / max(len(keywords), 1))
        
        # 话题向量 (16维)
        for topic in ['BCI', '解码', '隐私', '伦理', '融合', '突破', 
                      '学习', '反馈', '信号', '控制', '接口', '脑',
                      'AI', 'ML', '深度学习', '实时']:
            vector.append(1 if topic in text else 0)
        
        # 归一化
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
        
        return vector
    
    def _st_embedding(self, text: str) -> List[float]:
        """Sentence-transformers 向量化"""
        return self._model.encode(text).tolist()


class CapsuleVectorizer:
    """胶囊向量化器"""
    
    def __init__(self, embedding_provider: EmbeddingProvider):
        self.provider = embedding_provider
    
    def vectorize(self, capsule: CapsuleData) -> CapsuleVector:
        """将胶囊转换为向量"""
        # 组合文本
        text = f"{capsule.title} {capsule.insight} {' '.join(capsule.topics)}"
        
        embedding = self.provider.get_embedding(text)
        
        return CapsuleVector(
            id=capsule.id,
            title=capsule.title,
            domain=capsule.domain,
            topics=capsule.topics,
            insight=capsule.insight,
            embedding=embedding,
            metadata={
                "domains": [capsule.domain],
                "topics": capsule.topics,
                "datm_score": capsule.datm_score,
                "evidence": capsule.evidence,
                "action_items": capsule.action_items
            }
        )


class CollisionDetector:
    """碰撞检测器"""
    
    def __init__(self, similarity_threshold: float = 0.3):
        self.similarity_threshold = similarity_threshold
    
    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """余弦相似度"""
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        
        dot = sum(a*b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a*a for a in v1))
        norm2 = math.sqrt(sum(b*b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    def find_pairs(self, 
                   capsules: List[CapsuleVector],
                   max_pairs: int = 100) -> List[CollisionPair]:
        """查找碰撞对"""
        pairs = []
        seen: Set[Tuple[str, str]] = set()
        
        n = len(capsules)
        for i in range(n):
            for j in range(i+1, n):
                cap_a, cap_b = capsules[i], capsules[j]
                
                # 跳过同一胶囊
                if cap_a.id == cap_b.id:
                    continue
                
                # 跳过太相似的标题
                if self._is_similar_title(cap_a.title, cap_b.title):
                    continue
                
                pair_key = tuple(sorted([cap_a.id, cap_b.id]))
                if pair_key in seen:
                    continue
                
                similarity = self.cosine_similarity(cap_a.embedding, cap_b.embedding)
                
                if similarity >= self.similarity_threshold:
                    seen.add(pair_key)
                    
                    collision_type = self._get_collision_type(cap_a, cap_b)
                    shared_topics = list(set(cap_a.topics) & set(cap_b.topics))
                    
                    pair = CollisionPair(
                        capsule_a=cap_a,
                        capsule_b=cap_b,
                        similarity=similarity,
                        collision_type=collision_type,
                        shared_topics=shared_topics,
                        collision_id=hashlib.md5(f"{cap_a.id}:{cap_b.id}".encode()).hexdigest()[:8]
                    )
                    pairs.append(pair)
        
        # 按相似度排序
        pairs.sort(key=lambda x: -x.similarity)
        return pairs[:max_pairs]
    
    def _is_similar_title(self, title1: str, title2: str) -> bool:
        """检查标题是否太相似"""
        kw1 = set(title1.lower().split())
        kw2 = set(title2.lower().split())
        
        if not kw1 or not kw2:
            return False
        
        intersection = kw1 & kw2
        union = kw1 | kw2
        
        return len(intersection) / len(union) > 0.5 if union else False
    
    def _get_collision_type(self, a: CapsuleVector, b: CapsuleVector) -> str:
        """确定碰撞类型"""
        if a.domain != b.domain:
            return "cross_domain"
        elif len(set(a.topics) & set(b.topics)) > 0:
            return "complementary"
        else:
            return "same_domain"


class CapsuleFusionEngine:
    """胶囊融合引擎"""
    
    def __init__(self, min_score: float = 60.0):
        self.min_score = min_score
    
    def fuse(self, pair: CollisionPair) -> Optional[EmergedCapsule]:
        """融合两个胶囊"""
        a, b = pair.capsule_a, pair.capsule_b
        
        # 生成新标题
        title = self._generate_title(a, b, pair)
        
        # 融合洞见
        insight = self._merge_insights(a, b, pair)
        
        # 合并证据
        evidence = self._merge_evidence(a, b)
        
        # 合并行动
        actions = self._merge_actions(a, b)
        
        # 合并话题
        topics = list(set(a.topics) | set(b.topics))[:10]
        
        # 计算涌现评分
        score = self._calculate_score(a, b, pair)
        
        if score < self.min_score:
            return None
        
        # 融合向量
        embedding = self._fuse_embedding(a.embedding, b.embedding, pair.similarity)
        
        return EmergedCapsule(
            title=title,
            domain=f"{a.domain}+{b.domain}",
            topics=topics,
            insight=insight,
            evidence=evidence,
            action_items=actions,
            parent_ids=[a.id, b.id],
            collision_type=pair.collision_type,
            emergence_score=score,
            embedding=embedding
        )
    
    def _generate_title(self, a: CapsuleVector, b: CapsuleVector, pair: CollisionPair) -> str:
        """生成新标题"""
        if pair.collision_type == "cross_domain":
            return f"跨域融合: {a.domain} + {b.domain}"
        elif pair.collision_type == "complementary":
            return f"融合: {a.title[:25]} + {b.title[:25]}"
        else:
            return f"深化: {a.title[:30]} + {b.title[:30]}"
    
    def _merge_insights(self, a: CapsuleVector, b: CapsuleVector, pair: CollisionPair) -> str:
        """融合洞见"""
        parts = []
        
        if pair.collision_type == "cross_domain":
            parts.append(f"【跨域分析】{a.domain} 与 {b.domain} 的关联探索：")
            parts.append(f"\n📌 {a.domain}视角：{a.insight[:200]}...")
            parts.append(f"\n📌 {b.domain}视角：{b.insight[:200]}...")
            if pair.shared_topics:
                parts.append(f"\n🔗 共同关注：{', '.join(pair.shared_topics[:5])}")
            parts.append(f"\n💡 融合洞察：通过跨域分析发现，两个领域在 {pair.shared_topics[0] if pair.shared_topics else '多个方面'} 存在深层关联，建议进一步研究。")
        else:
            parts.append(f"【知识融合】基于两个胶囊的综合分析：")
            parts.append(f"\n• {a.title}：{a.insight[:150]}...")
            parts.append(f"\n• {b.title}：{b.insight[:150]}...")
            parts.append(f"\n💡 融合洞察：两个胶囊相互补充，形成更完整的知识图景。")
        
        return "\n".join(parts)
    
    def _merge_evidence(self, a: CapsuleVector, b: CapsuleVector) -> List[str]:
        """合并证据"""
        evidence = []
        evidence.extend([f"[来自 {a.title[:20]}] {e}" for e in a.metadata.get('evidence', [])[:2]])
        evidence.extend([f"[来自 {b.title[:20]}] {e}" for e in b.metadata.get('evidence', [])[:2]])
        evidence.append("💡 证据来源：跨胶囊融合分析")
        return evidence[:5]
    
    def _merge_actions(self, a: CapsuleVector, b: CapsuleVector) -> List[str]:
        """合并行动"""
        actions = []
        actions.extend(a.metadata.get('action_items', [])[:2])
        actions.extend(b.metadata.get('action_items', [])[:2])
        actions.append("📋 基于融合分析制定下一步研究计划")
        return actions[:5]
    
    def _calculate_score(self, a: CapsuleVector, b: CapsuleVector, pair: CollisionPair) -> float:
        """计算涌现评分"""
        score = 0.0
        
        # 跨域加分
        if pair.collision_type == "cross_domain":
            score += 30
        elif pair.collision_type == "complementary":
            score += 20
        
        # 相似度加分
        score += pair.similarity * 30
        
        # 共同话题加分
        score += min(len(pair.shared_topics) * 8, 20)
        
        # DATM 加权
        datm_a = a.metadata.get('datm_score', 0)
        datm_b = b.metadata.get('datm_score', 0)
        # 确保是数值（可能是个 dict）
        if isinstance(datm_a, dict):
            datm_a = (datm_a.get('truth', 0) + datm_a.get('goodness', 0) + 
                     datm_a.get('beauty', 0) + datm_a.get('intelligence', 0)) / 4
        if isinstance(datm_b, dict):
            datm_b = (datm_b.get('truth', 0) + datm_b.get('goodness', 0) + 
                     datm_b.get('beauty', 0) + datm_b.get('intelligence', 0)) / 4
        
        score += min((float(datm_a) + float(datm_b)) * 0.3, 20)
        
        return min(score, 100)
    
    def _fuse_embedding(self, e1: List[float], e2: List[float], ratio: float) -> List[float]:
        """融合向量"""
        if not e1:
            return e2
        if not e2:
            return e1
        
        # 加权平均
        fused = [e1[i] * (1 - ratio) + e2[i] * ratio for i in range(len(e1))]
        
        # 归一化
        norm = math.sqrt(sum(x*x for x in fused))
        if norm > 0:
            fused = [x/norm for x in fused]
        
        return fused


class CollisionSystem:
    """胶囊碰撞系统 - 主类"""
    
    def __init__(self, 
                 capsulehub_url: str = "http://localhost:8001",
                 embedding_provider: str = "simple",
                 similarity_threshold: float = 0.2,
                 min_emergence_score: float = 50.0):
        
        self.capsulehub_url = capsulehub_url
        
        # 初始化组件
        self.embedding_provider = EmbeddingProvider(embedding_provider)
        self.vectorizer = CapsuleVectorizer(self.embedding_provider)
        self.detector = CollisionDetector(similarity_threshold)
        self.fuser = CapsuleFusionEngine(min_emergence_score)
        
        # 状态
        self.capsules: List[CapsuleData] = []
        self.vectors: List[CapsuleVector] = []
        self.emerged: List[EmergedCapsule] = []
        self.last_run: Optional[str] = None
        self.stats = {
            "total_runs": 0,
            "total_collisions": 0,
            "total_emerged": 0
        }
    
    def load_capsules(self, limit: int = 100) -> int:
        """从 CapsuleHub 加载胶囊"""
        try:
            url = f"{self.capsulehub_url}/api/capsules?limit={limit}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                self.capsules = []
                for c in data.get('capsules', []):
                    capsule = CapsuleData(
                        id=c.get('id', ''),
                        title=c.get('title', ''),
                        domain=c.get('domain', ''),
                        topics=c.get('topics', []),
                        insight=c.get('insight', ''),
                        evidence=c.get('evidence', []),
                        action_items=c.get('action_items', []),
                        authors=c.get('authors', []),
                        datm_score=c.get('datm_score', 0.0),
                        created_at=c.get('created_at', '')
                    )
                    self.capsules.append(capsule)
                
                # 向量化
                self.vectors = [self.vectorizer.vectorize(c) for c in self.capsules]
                
                print(f"📦 加载了 {len(self.capsules)} 个胶囊")
                return len(self.capsules)
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return 0
    
    def run(self, save_emerged: bool = False, publish_to_moltbook: bool = False) -> Dict:
        """运行碰撞系统"""
        print(f"\n{'='*60}")
        print(f"💥 Capsule Collision System v2.0")
        print(f"{'='*60}\n")
        
        # 加载
        count = self.load_capsules()
        if count == 0:
            return {"error": "No capsules loaded"}
        
        # 检测碰撞
        print("🔍 检测碰撞...")
        pairs = self.detector.find_pairs(self.vectors)
        print(f"   找到 {len(pairs)} 个碰撞对\n")
        
        # 执行融合
        print("🧬 执行融合...")
        emerged = []
        for i, pair in enumerate(pairs, 1):
            new_cap = self.fuser.fuse(pair)
            if new_cap:
                emerged.append(new_cap)
                status = "🌟" if new_cap.emergence_score >= 70 else "✓"
                print(f"   {status} [{i}] {new_cap.title[:40]} (评分: {new_cap.emergence_score:.0f})")
        
        self.emerged = emerged
        self.last_run = datetime.utcnow().isoformat()
        self.stats["total_runs"] += 1
        self.stats["total_collisions"] += len(pairs)
        self.stats["total_emerged"] += len(emerged)
        
        # 保存
        if save_emerged and emerged:
            self._save_emerged()
        
        # 发布到 Moltbook
        if publish_to_moltbook and emerged:
            published = self._publish_to_moltbook(emerged)
            print(f"\n📤 已发布 {published} 个胶囊到 Moltbook")
        
        # 统计
        print(f"\n📊 碰撞统计:")
        print(f"   源胶囊: {len(self.capsules)}")
        print(f"   碰撞对: {len(pairs)}")
        print(f"   涌现胶囊: {len(emerged)}")
        print(f"   高质量 (≥70): {len([e for e in emerged if e.emergence_score >= 70])}")
        
        # 按类型统计
        by_type = defaultdict(int)
        for e in emerged:
            by_type[e.collision_type] += 1
        
        print(f"   跨域融合: {by_type['cross_domain']}")
        print(f"   互补融合: {by_type['complementary']}")
        print(f"   同域深化: {by_type['same_domain']}")
        
        return {
            "run_time": self.last_run,
            "source_capsules": count,
            "collision_pairs": len(pairs),
            "emerged_capsules": len(emerged),
            "high_quality": len([e for e in emerged if e.emergence_score >= 70]),
            "by_type": dict(by_type)
        }
    
    def _save_emerged(self):
        """保存涌现胶囊"""
        output = {
            "generated_at": self.last_run,
            "total": len(self.emerged),
            "capsules": [
                {
                    "title": e.title,
                    "domain": e.domain,
                    "topics": e.topics,
                    "insight": e.insight[:300],
                    "evidence": e.evidence,
                    "action_items": e.action_items,
                    "parents": e.parent_ids,
                    "collision_type": e.collision_type,
                    "score": e.emergence_score
                }
                for e in self.emerged[:20]  # 保存前20个
            ]
        }
        
        os.makedirs('/Users/wanyview/clawd/kai-hub/reports', exist_ok=True)
        with open('/Users/wanyview/clawd/kai-hub/reports/collision_v2_report.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 报告已保存: reports/collision_v2_report.json")
    
    def _publish_to_moltbook(self, capsules: List[EmergedCapsule]) -> int:
        """发布涌现胶囊到 Moltbook"""
        # 加载凭证
        cred_path = "/Users/wanyview/.moltbook/credentials.json"
        if not os.path.exists(cred_path):
            print(f"   ⚠️ 未找到 Moltbook 凭证")
            return 0
        
        with open(cred_path, 'r') as f:
            creds = json.load(f)
        
        api_key = creds.get("api_key")
        if not api_key:
            print(f"   ⚠️ API Key 缺失")
            return 0
        
        # 检查 claim 状态
        try:
            status_req = urllib.request.Request(
                "https://www.moltbook.com/api/v1/agents/status",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            with urllib.request.urlopen(status_req) as resp:
                status = json.loads(resp.read().decode())
                if status.get("status") != "claimed":
                    print(f"   ⚠️ Moltbook 未 Claim，无法发布")
                    return 0
        except Exception as e:
            print(f"   ⚠️ 无法检查 Moltbook 状态: {e}")
            return 0
        
        # 发布胶囊
        published = 0
        url = "https://www.moltbook.com/api/v1/posts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        for cap in capsules[:10]:  # 最多发布10个
            try:
                # 生成帖子内容
                content = f"""💥 **知识涌现**

{cap.insight}

**碰撞类型**: {cap.collision_type}
**涌现评分**: {cap.emergence_score:.0f}/100

{chr(10).join(['• ' + e for e in cap.evidence[:3]])}
{chr(10).join(['• ' + a for a in cap.action_items[:3]])}

#知识胶囊 #碰撞系统 #涌现"""

                data = json.dumps({
                    "submolt": "knowledge",
                    "title": f"💥 {cap.title[:100]}",
                    "content": content[:2000]
                }).encode()
                
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req) as resp:
                    result = json.loads(resp.read().decode())
                    if result.get("success"):
                        published += 1
                        print(f"   ✅ {cap.title[:40]}...")
            except Exception as e:
                print(f"   ❌ {cap.title[:40]}... ({str(e)[:50]})")
        
        return published
    
    def run_continuous(self, interval: int = 3600, publish: bool = False):
        """持续运行（定时碰撞）
        
        Args:
            interval: 碰撞间隔（秒）
            publish: 是否自动发布到 Moltbook
        """
        print(f"\n🚀 启动持续碰撞模式 (间隔 {interval} 秒)")
        
        def worker():
            while True:
                try:
                    self.run(save_emerged=True, publish_to_moltbook=publish)
                    time.sleep(interval)
                except Exception as e:
                    print(f"❌ 碰撞失败: {e}")
                    time.sleep(60)  # 失败后等待1分钟重试
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        if publish:
            print("   📤 自动发布到 Moltbook: 开启")
        print("✅ 持续碰撞已启动")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Capsule Collision System v2.0")
    parser.add_argument("--continuous", "-c", action="store_true", help="持续运行模式")
    parser.add_argument("--publish", "-p", action="store_true", help="自动发布到 Moltbook")
    parser.add_argument("--interval", "-i", type=int, default=3600, help="碰撞间隔（秒）")
    parser.add_argument("--save", "-s", action="store_true", default=True, help="保存报告")
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║       💥 Capsule Collision System v2.0 - 增强版                       ║
║                                                                      ║
║  功能: 预训练向量化 | 多种碰撞策略 | 实时检测 | 自动发布             ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    system = CollisionSystem(
        capsulehub_url="http://localhost:8001",
        embedding_provider="simple",
        similarity_threshold=0.2,
        min_emergence_score=50.0
    )
    
    if args.continuous:
        system.run_continuous(interval=args.interval, publish=args.publish)
    else:
        system.run(save_emerged=args.save, publish_to_moltbook=args.publish)
    
    return system


if __name__ == "__main__":
    main()
