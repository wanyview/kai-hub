#!/usr/bin/env python3
"""
胶囊碰撞系统 - 知识自涌现演示

运行胶囊碰撞，让知识胶囊之间直接对话产生新洞见！
"""

import sys
import json
import urllib.request
import os
from datetime import datetime

sys.path.insert(0, '/Users/wanyview/clawd/kai-hub/src')
os.chdir('/Users/wanyview/clawd/kai-hub')

from capsule_collision import CapsuleCollisionEngine


def run_demo():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       💥 胶囊碰撞系统 - 知识自涌现引擎 DEMO                                 ║
║                                                                               ║
║  "让知识胶囊作为独立主体，在语义空间中直接碰撞产生新火花"                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    engine = CapsuleCollisionEngine()
    
    # 运行碰撞
    emerged = engine.run_collision(save_to_hub=False)
    
    # 筛选高质量的涌现胶囊
    high_quality = [e for e in emerged if e.emergence_score >= 70]
    cross_domain = [e for e in emerged if e.collision_type == "cross_domain"]
    
    print(f"\n{'='*60}")
    print("🌟 高质量涌现胶囊 (评分 >= 70)")
    print("="*60)
    
    for i, cap in enumerate(high_quality[:10], 1):
        print(f"\n{i}. {cap.title}")
        print(f"   碰撞类型: {cap.collision_type}")
        print(f"   涌现评分: {cap.emergence_score:.0f}")
        print(f"   父胶囊: {', '.join([p[:20] for p in cap.parent_capsules])}")
        print(f"   核心洞见: {cap.insight[:100]}...")
    
    print(f"\n{'='*60}")
    print("🔗 跨域融合亮点")
    print("="*60)
    
    for i, cap in enumerate(cross_domain[:5], 1):
        print(f"\n{i}. {cap.title}")
        print(f"   领域: {cap.domain}")
        print(f"   评分: {cap.emergence_score:.0f}")
    
    # 保存涌现胶囊到文件
    output = {
        "generated_at": str(datetime.utcnow()),
        "total_capsules": len(engine.capsules),
        "collision_pairs": len(emerged),
        "emerged_capsules": len(high_quality),
        "cross_domain_fusions": len(cross_domain),
        "high_quality_emergent": [
            {
                "title": e.title,
                "domain": e.domain,
                "collision_type": e.collision_type,
                "score": e.emergence_score,
                "insight": e.insight[:200],
                "topics": e.topics
            }
            for e in high_quality[:10]
        ]
    }
    
    with open('/Users/wanyview/clawd/kai-hub/reports/emergent_capsules.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存: reports/emergent_capsules.json")
    
    return output


if __name__ == "__main__":
    run_demo()
