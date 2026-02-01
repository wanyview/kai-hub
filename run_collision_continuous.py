#!/usr/bin/env python3
"""
胶囊碰撞系统 - 持续运行脚本

功能:
1. 持续运行碰撞检测
2. 自动发布高质量涌现胶囊到 Moltbook
3. 定期执行（默认每小时）
"""

import sys
import os

sys.path.insert(0, '/Users/wanyview/clawd/kai-hub/src')
os.chdir('/Users/wanyview/clawd/kai-hub')

from capsule_collision_v2 import CollisionSystem


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       💥 胶囊碰撞系统 - 持续运行模式                                      ║
║                                                                               ║
║  功能:                                                                   ║
║    • 自动检测胶囊碰撞                                                     ║
║    • 生成涌现胶囊                                                         ║
║    • 自动发布到 Moltbook (可选)                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # 初始化系统
    system = CollisionSystem(
        capsulehub_url="http://localhost:8001",
        embedding_provider="simple",
        similarity_threshold=0.2,
        min_emergence_score=50.0
    )
    
    # 检查参数
    publish = "--publish" in sys.argv or "-p" in sys.argv
    interval = 3600  # 默认1小时
    
    for arg in sys.argv:
        if arg.startswith("--interval=") or arg.startswith("-i="):
            try:
                interval = int(arg.split("=")[1])
            except:
                pass
    
    # 启动持续模式
    print(f"\n🚀 启动持续碰撞模式")
    print(f"   碰撞间隔: {interval} 秒 ({interval//60} 分钟)")
    print(f"   自动发布: {'开启' if publish else '关闭'}")
    print(f"\n💡 使用 Ctrl+C 停止")
    print(f"   或: python3 run_collision_continous.py --publish -i=1800")
    print(f"   (每30分钟碰撞，自动发布到 Moltbook)")
    
    system.run_continuous(interval=interval, publish=publish)


if __name__ == "__main__":
    main()
