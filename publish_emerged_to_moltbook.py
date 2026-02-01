#!/usr/bin/env python3
"""
发布涌现胶囊到 Moltbook

从碰撞报告中读取高质量胶囊，自动发布到 Moltbook
"""

import json
import urllib.request
import urllib.error
import os


def load_credentials():
    """加载 Moltbook 凭证"""
    cred_path = "/Users/wanyview/.moltbook/credentials.json"
    if os.path.exists(cred_path):
        with open(cred_path, 'r') as f:
            return json.load(f)
    return None


def check_claim_status(api_key):
    """检查 claim 状态"""
    try:
        req = urllib.request.Request(
            "https://www.moltbook.com/api/v1/agents/status",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        with urllib.request.urlopen(req) as resp:
            status = json.loads(resp.read().decode())
            return status.get("status") == "claimed"
    except:
        return False


def publish_to_moltbook(api_key, capsules, submolt="knowledge"):
    """发布胶囊到 Moltbook"""
    url = "https://www.moltbook.com/api/v1/posts"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    published = []
    
    for cap in capsules:
        try:
            content = f"""💥 **知识涌现**

{cap['insight']}

**碰撞类型**: {cap['collision_type']}
**涌现评分**: {cap['score']:.0f}/100

**证据**:
{chr(10).join(['• ' + e for e in cap['evidence'][:3]])}

**行动建议**:
{chr(10).join(['• ' + a for a in cap['action_items'][:3]])}

#知识胶囊 #碰撞系统 #涌现"""

            data = json.dumps({
                "submolt": submolt,
                "title": f"💥 {cap['title'][:100]}",
                "content": content[:2000]
            }).encode()
            
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                if result.get("success"):
                    published.append(cap['title'])
                    print(f"  ✅ {cap['title'][:40]}...")
                else:
                    print(f"  ❌ {cap['title'][:40]}... ({result.get('error', 'Error')})")
        except urllib.error.HTTPError as e:
            error = json.loads(e.read().decode())
            print(f"  ❌ {cap['title'][:40]}... ({error.get('error', str(e))})")
        except Exception as e:
            print(f"  ❌ {cap['title'][:40]}... ({str(e)[:50]})")
    
    return published


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║       📤 发布涌现胶囊到 Moltbook                                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # 加载凭证
    creds = load_credentials()
    if not creds:
        print("❌ 未找到 Moltbook 凭证")
        print("   请先注册: python3 promote_kai_to_moltbook.py")
        return
    
    api_key = creds.get("api_key")
    if not api_key:
        print("❌ API Key 缺失")
        return
    
    # 检查 claim
    print("🔗 检查 Moltbook 状态...")
    if not check_claim_status(api_key):
        print("❌ Moltbook 未 Claim，无法发布")
        print("   请访问 Claim URL 完成验证")
        return
    
    print("✅ Moltbook 已 Claim，可以发布\n")
    
    # 加载碰撞报告
    report_path = "/Users/wanyview/clawd/kai-hub/reports/collision_v2_report.json"
    if not os.path.exists(report_path):
        print("❌ 碰撞报告不存在")
        print("   请先运行: python3 src/capsule_collision_v2.py")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    capsules = report.get('capsules', [])
    if not capsules:
        print("❌ 没有涌现胶囊")
        return
    
    # 筛选高质量胶囊
    high_quality = [c for c in capsules if c.get('score', 0) >= 70]
    
    print(f"📦 加载了 {len(capsules)} 个涌现胶囊")
    print(f"🌟 高质量胶囊 (≥70分): {len(high_quality)} 个")
    print(f"\n📤 准备发布到 Moltbook...")
    
    # 发布
    published = publish_to_moltbook(api_key, high_quality[:10])  # 最多10个
    
    print(f"\n" + "="*60)
    if published:
        print(f"✅ 成功发布 {len(published)} 个胶囊到 Moltbook!")
    else:
        print("⚠️ 没有胶囊被发布")
    print("="*60)


if __name__ == "__main__":
    main()
