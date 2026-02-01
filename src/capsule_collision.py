#!/usr/bin/env python3
"""
Capsule Collision Engine - 知识胶囊自涌现系统

让知识胶囊之间直接碰撞，在语义空间中产生新的知识火花！
"""

import json
import os
import math
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import urllib.request


# ========== 配置 ==========

@dataclass
class CapsuleVector:
    """胶囊向量"""
    id: str
    title: str
    domain: str
    topics: List[str]
    insight: str
    evidence: List[str]
    action_items: List[str]
    embedding: List[float] = field(default_factory=list)
    vector_id: str = ""


@dataclass  
class CollisionPair:
    """碰撞对"""
    capsule_a: CapsuleVector
    capsule_b: CapsuleVector
    similarity: float
    collision_type: str  # "cross_domain", "same_domain", "complementary"
    shared_topics: List[str]


@dataclass
class EmergedCapsule:
    """涌现的新胶囊"""
    title: str
    domain: str
    topics: List[str]
    insight: str
    evidence: List[str]
    action_items: List[str]
    parent_capsules: List[str]
    collision_type: str
    emergence_score: float
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class CapsuleVectorizer:
    """胶囊向量化器"""
    
    # 领域关键词（简化版，实际可用预训练模型）
    DOMAIN_KEYWORDS = {
        'neuroscience': ['神经', '大脑', '皮层', '神经元', '信号', '运动', '感觉', '可塑性'],
        'ai': ['AI', '机器学习', '深度学习', '算法', '解码', '模型', '神经网络', '端到端'],
        'ethics': ['伦理', '隐私', '公平', '权利', '增强', '边界', '认知'],
        'materials': ['材料', '电极', '柔性', '生物相容', '纳米', '导电'],
        'medical': ['临床', '康复', '治疗', '患者', '运动障碍'],
        'physics': ['重力', '物理', '力学', '量子', '运动'],
        'technology': ['技术', '发明', '创新', '设备', '系统'],
        'biotech': ['生物', '合成', '遗传', '基因', '生命']
    }
    
    def vectorize(self, capsule: Dict) -> CapsuleVector:
        """将胶囊转换为向量"""
        text = f"{capsule.get('title', '')} {capsule.get('insight', '')} {' '.join(capsule.get('topics', []))}"
        
        # 简化版向量化：基于词频的向量
        embedding = self._text_to_vector(text)
        
        return CapsuleVector(
            id=capsule.get('id', ''),
            title=capsule.get('title', ''),
            domain=capsule.get('domain', ''),
            topics=capsule.get('topics', []),
            insight=capsule.get('insight', ''),
            evidence=capsule.get('evidence', []),
            action_items=capsule.get('action_items', []),
            embedding=embedding,
            vector_id=f"vec_{capsule.get('id', '')}"
        )
    
    def _text_to_vector(self, text: str) -> List[float]:
        """文本转向量（简化版 TF-IDF）"""
        words = set(text.lower().split())
        vector = []
        
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if any(w in text.lower() for w in kw.split()))
            vector.append(score / max(len(keywords), 1))
        
        # 添加话题向量
        for topic in ['BCI', '解码', '隐私', '伦理', '融合', '突破']:
            vector.append(1 if topic in text else 0)
        
        # L2 归一化
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
        
        return vector


class CapsuleCollisionEngine:
    """胶囊碰撞引擎"""
    
    def __init__(self, capsulehub_url: str = "http://localhost:8001"):
        self.capsulehub_url = capsulehub_url
        self.vectorizer = CapsuleVectorizer()
        self.capsules: List[CapsuleVector] = []
        self.emerged_capsules: List[EmergedCapsule] = []
    
    def load_capsules(self, limit: int = 100) -> int:
        """从 CapsuleHub 加载胶囊"""
        try:
            url = f"{self.capsulehub_url}/api/capsules?limit={limit}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                self.capsules = []
                for c in data.get('capsules', []):
                    vector = self.vectorizer.vectorize(c)
                    self.capsules.append(vector)
                
                print(f"📦 加载了 {len(self.capsules)} 个胶囊")
                return len(self.capsules)
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return 0
    
    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦相似度"""
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        
        dot = sum(a*b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a*a for a in v1))
        norm2 = math.sqrt(sum(b*b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot / (norm1 * norm2)
    
    def find_collision_pairs(self, 
                            similarity_threshold: float = 0.3,
                            max_pairs: int = 50) -> List[CollisionPair]:
        """查找可能的碰撞对"""
        pairs = []
        seen: Set[Tuple[str, str]] = set()
        
        for i, cap_a in enumerate(self.capsules):
            for j, cap_b in enumerate(self.capsules[i+1:], i+1):
                # 避免重复（同一个胶囊）
                if cap_a.id == cap_b.id:
                    continue
                
                # 避免标题太相似（去重）
                if self._is_similar_title(cap_a.title, cap_b.title):
                    continue
                
                pair_key = tuple(sorted([cap_a.id, cap_b.id]))
                if pair_key in seen:
                    continue
                
                similarity = self.cosine_similarity(cap_a.embedding, cap_b.embedding)
                
                if similarity >= similarity_threshold:
                    seen.add(pair_key)
                    
                    # 确定碰撞类型
                    collision_type = self._get_collision_type(cap_a, cap_b)
                    
                    # 查找共同话题
                    shared_topics = list(set(cap_a.topics) & set(cap_b.topics))
                    
                    pair = CollisionPair(
                        capsule_a=cap_a,
                        capsule_b=cap_b,
                        similarity=similarity,
                        collision_type=collision_type,
                        shared_topics=shared_topics
                    )
                    pairs.append(pair)
        
        # 按相似度排序，保留前 max_pairs
        pairs.sort(key=lambda x: -x.similarity)
        pairs = pairs[:max_pairs]
        
        print(f"💥 找到 {len(pairs)} 个有效碰撞对 (去重后)")
        return pairs
    
    def _is_similar_title(self, title1: str, title2: str) -> bool:
        """检查标题是否太相似（用于去重）"""
        # 提取关键词
        kw1 = set(title1.lower().split())
        kw2 = set(title2.lower().split())
        
        if not kw1 or not kw2:
            return False
        
        # 计算交集
        intersection = kw1 & kw2
        union = kw1 | kw2
        
        # 如果交集/并集 > 0.5，认为太相似
        return len(intersection) / len(union) > 0.5
    
    def _get_collision_type(self, cap_a: CapsuleVector, cap_b: CapsuleVector) -> str:
        """确定碰撞类型"""
        if cap_a.domain != cap_b.domain:
            return "cross_domain"  # 跨域碰撞
        elif len(self._find_shared_topics(cap_a, cap_b)) > 0:
            return "complementary"  # 互补碰撞
        else:
            return "same_domain"  # 同域碰撞
    
    def _find_shared_topics(self, cap_a: CapsuleVector, cap_b: CapsuleVector) -> Set[str]:
        """查找共同话题"""
        return set(cap_a.topics) & set(cap_b.topics)
    
    def collide(self, pair: CollisionPair) -> Optional[EmergedCapsule]:
        """执行胶囊碰撞，生成新胶囊"""
        a = pair.capsule_a
        b = pair.capsule_b
        
        # 生成新标题
        if pair.collision_type == "cross_domain":
            title = f"跨域融合: {a.domain} + {b.domain}"
        else:
            title = f"知识融合: {a.title[:20]} + {b.title[:20]}"
        
        # 融合洞见
        insight = self._merge_insights(a, b, pair)
        
        # 交叉验证证据
        evidence = self._merge_evidence(a, b)
        
        # 结合行动建议
        action_items = self._merge_actions(a, b)
        
        # 合并话题
        topics = list(set(a.topics) | set(b.topics))[:10]
        
        # 计算涌现评分
        emergence_score = self._calculate_emergence_score(a, b, pair)
        
        # 质量检查
        if emergence_score < 40:  # 阈值
            return None
        
        return EmergedCapsule(
            title=title,
            domain=f"{a.domain}+{b.domain}",
            topics=topics,
            insight=insight,
            evidence=evidence,
            action_items=action_items,
            parent_capsules=[a.id, b.id],
            collision_type=pair.collision_type,
            emergence_score=emergence_score
        )
    
    def _merge_insights(self, a: CapsuleVector, b: CapsuleVector, pair: CollisionPair) -> str:
        """融合洞见"""
        parts = []
        
        # 从两个胶囊提取核心
        if pair.collision_type == "cross_domain":
            parts.append(f"通过跨域分析发现，{a.domain} 与 {b.domain} 存在深层关联：")
            parts.append(f"• {a.domain}视角: {a.insight[:100]}...")
            parts.append(f"• {b.domain}视角: {b.insight[:100]}...")
            parts.append(f"共同关注: {', '.join(pair.shared_topics[:3])}")
        else:
            parts.append(f"知识融合分析：")
            parts.append(f"• {a.title}: {a.insight[:150]}...")
            parts.append(f"• {b.title}: {b.insight[:150]}...")
        
        return "\n".join(parts)
    
    def _merge_evidence(self, a: CapsuleVector, b: CapsuleVector) -> List[str]:
        """合并证据"""
        evidence = []
        evidence.extend([f"[A] {e}" for e in a.evidence[:2]])
        evidence.extend([f"[B] {e}" for e in b.evidence[:2]])
        evidence.append(f"来源: {a.title[:30]} + {b.title[:30]}")
        return evidence[:5]
    
    def _merge_actions(self, a: CapsuleVector, b: CapsuleVector) -> List[str]:
        """合并行动建议"""
        actions = []
        actions.extend(a.action_items[:2])
        actions.extend(b.action_items[:2])
        actions.append("基于融合分析制定下一步计划")
        return actions[:5]
    
    def _calculate_emergence_score(self, a: CapsuleVector, b: CapsuleVector, pair: CollisionPair) -> float:
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
        score += min(len(pair.shared_topics) * 10, 20)
        
        # 证据充分性
        score += min((len(a.evidence) + len(b.evidence)) * 5, 20)
        
        return min(score, 100)
    
    def run_collision(self, save_to_hub: bool = False) -> List[EmergedCapsule]:
        """运行完整的碰撞流程"""
        print(f"\n{'='*60}")
        print(f"💥 Capsule Collision Engine")
        print(f"{'='*60}\n")
        
        # 1. 加载胶囊
        count = self.load_capsules()
        if count == 0:
            print("❌ 没有胶囊可碰撞")
            return []
        
        # 2. 查找碰撞对
        pairs = self.find_collision_pairs()
        
        # 3. 执行碰撞
        emerged = []
        print(f"\n🧬 执行碰撞...")
        for i, pair in enumerate(pairs, 1):
            new_cap = self.collide(pair)
            if new_cap:
                emerged.append(new_cap)
                print(f"  [{i}] {new_cap.title[:45]} (评分: {new_cap.emergence_score:.0f})")
        
        self.emerged_capsules = emerged
        
        # 4. 统计
        print(f"\n📊 碰撞结果:")
        print(f"   碰撞对: {len(pairs)}")
        print(f"   涌现胶囊: {len(emerged)}")
        print(f"   平均评分: {sum(e.emergence_score for e in emerged)/max(len(emerged),1):.1f}")
        
        if save_to_hub:
            self._save_to_capsulehub()
        
        return emerged
    
    def _save_to_capsulehub(self):
        """保存涌现胶囊到 CapsuleHub"""
        print(f"\n💾 保存到 CapsuleHub...")
        saved = 0
        
        for capsule in self.emerged_capsules:
            try:
                data = {
                    "title": capsule.title,
                    "domain": capsule.domain,
                    "topics": capsule.topics,
                    "insight": capsule.insight,
                    "evidence": capsule.evidence,
                    "action_items": capsule.action_items,
                    "authors": ["CapsuleCollisionEngine"],
                    "is_emergent": True,
                    "parent_capsules": capsule.parent_capsules
                }
                
                url = f"{self.capsulehub_url}/api/capsules"
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                
                with urllib.request.urlopen(req) as response:
                    saved += 1
                    print(f"  ✅ {capsule.title[:40]}")
            except Exception as e:
                print(f"  ❌ {capsule.title[:40]}: {e}")
        
        print(f"\n✅ 成功保存 {saved} 个涌现胶囊到 CapsuleHub")
    
    def get_report(self) -> Dict:
        """生成报告"""
        return {
            "total_capsules": len(self.capsules),
            "collision_pairs": len(self.find_collision_pairs()),
            "emerged_capsules": len(self.emerged_capsules),
            "average_score": sum(e.emergence_score for e in self.emerged_capsules)/max(len(self.emerged_capsules),1),
            "by_type": {
                pair.collision_type: len([e for e in self.emerged_capsules if e.collision_type == pair.collision_type])
                for pair in self.emerged_capsules
            }
        }


def main():
    """主函数"""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║       💥 Capsule Collision Engine - 知识胶囊自涌现系统               ║
║                                                                      ║
║  胶囊之间直接碰撞，在语义空间中产生新的知识火花！                    ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    engine = CapsuleCollisionEngine()
    
    # 运行碰撞
    emerged = engine.run_collision(save_to_hub=False)
    
    # 显示涌现的胶囊
    if emerged:
        print(f"\n🌟 涌现的新知识:")
        for i, cap in enumerate(emerged[:5], 1):
            print(f"\n{i}. {cap.title}")
            print(f"   领域: {cap.domain}")
            print(f"   评分: {cap.emergence_score:.0f}")
            print(f"   洞见: {cap.insight[:80]}...")
    
    return engine


if __name__ == "__main__":
    main()
