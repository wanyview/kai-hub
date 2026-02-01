#!/usr/bin/env python3
"""
KaiDison 专业级数字科学家 - 批量运行脚本
"""

import json
import sys
import os
sys.path.insert(0, '/Users/wanyview/clawd/kai-hub/src')

from kai_dison_professional import KaiDisonProfessional


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              KaiDison 专业级数字科学家 v0.1.0                        ║
║                                                                      ║
║  功能:                                                               ║
║    🔗 跨域关联引擎 - 识别跨学科关联                                   ║
║    💥 突破检测算法 - 发现技术突破                                     ║
║    🤝 共识达成追踪 - 分析观点演化                                     ║
║    🔮 趋势预测 - 预测未来方向                                         ║
║    🧬 融合胶囊生成 - 批量产出知识胶囊                                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # 初始化 KaiDison
    kaiDison = KaiDisonProfessional()
    
    # 运行分析
    result = kaiDison.scan_and_analyze()
    
    # 输出摘要
    print("\n" + "="*60)
    print("📊 KaiDison 专业分析摘要")
    print("="*60)
    print(f"\n🤖 智能体: {result['kaiDison']['name']} ({result['kaiDison']['level']})")
    print(f"📡 状态: {result['kaiDison']['status']}")
    print(f"🕐 最后扫描: {result['kaiDison']['last_scan']}")
    
    print(f"\n📈 核心指标:")
    print(f"   🔗 跨域关联: {result['stats']['cross_domain_links']}")
    print(f"   💥 技术突破: {result['stats']['breakthroughs']}")
    print(f"   🤝 共识达成: {result['stats']['consensus']}")
    print(f"   🧬 融合胶囊: {result['stats']['fusion_capsules']}")
    
    print("\n💡 关键发现:")
    for b in result.get('breakthroughs', [])[:2]:
        print(f"   • {b['title'][:40]} (重要性: {b['significance']:.0f}%)")
    
    for a in result.get('associations', [])[:2]:
        print(f"   • {a['domains'][0]} ↔ {a['domains'][1]} (强度: {a['strength']:.1%})")
    
    print("\n" + "="*60)
    
    return result


if __name__ == "__main__":
    main()
