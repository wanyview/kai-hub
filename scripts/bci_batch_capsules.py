#!/usr/bin/env python3
"""
BCI 脑机接口 - 端到端知识胶囊生成流程

打 通 SuiLight → Kai-Hub → CapsuleHub 完整链路
"""

import sys
import os
import json
import requests
from datetime import datetime

sys.path.insert(0, '/Users/wanyview/SuiLight')
os.chdir('/Users/wanyview/SuiLight')

# 配置
SUI_LIGHT_URL = "http://localhost:8000"
CAPSULEHUB_URL = "http://localhost:8001"


# ========== BCI 胶囊模板 ==========

BCI_CAPSULES = [
    {
        "title": "脑机接口的运动意图神经解码",
        "domain": "neuroscience",
        "topics": ["BCI", "运动意图", "神经解码", "运动皮层"],
        "insight": "脑机接口通过解码运动皮层中的神经活动模式来获取用户的运动意图。研究发现，即使猴子和人类在执行不同方向的手部运动时，单个神经元的活动方向与运动方向高度一致，这为建立运动意图与神经信号之间的映射关系提供了基础。通过群体向量分析和机器学习方法，可以实现高精度的意图识别。",
        "evidence": [
            "Georgopoulos等人1986年发现运动皮层神经元的调谐方向",
            "多个神经元活动的群体向量可以预测运动方向",
            "深度学习解码器在离线分析中准确率可达95%以上"
        ],
        "action_items": [
            "优化实时解码算法以降低延迟",
            "开发个性化的神经信号模型以提高适应性",
            "建立标准化的BCI性能评估框架"
        ],
        "authors": ["神经科学家", "AI研究员", "临床医生"]
    },
    {
        "title": "闭环BCI的感觉反馈机制",
        "domain": "neuroscience",
        "topics": ["闭环BCI", "感觉反馈", "神经可塑性", "触觉体验"],
        "insight": "闭环脑机接口需要将感觉信息反馈给大脑，以完成感知-动作循环。电触觉刺激是常用的感觉反馈方式，通过在感觉皮层或外周神经施加电刺激，可以产生类似触觉的感觉。然而，如何产生自然、细腻的感觉体验仍是一个挑战，需要精确控制刺激参数以匹配用户的感知阈值。",
        "evidence": [
            "微刺激感觉皮层可以产生可辨别的触觉感觉",
            "闭环BCI中感觉反馈可以促进神经可塑性",
            "触觉反馈的时机和强度对用户体验有显著影响"
        ],
        "action_items": [
            "开发更精确的感觉反馈控制算法",
            "研究神经可塑性在长期BCI使用中的作用",
            "设计个性化的感觉反馈方案"
        ],
        "authors": ["神经科学家", "生物医学工程师"]
    },
    {
        "title": "BCI的神经可塑性与学习",
        "domain": "neuroscience",
        "topics": ["神经可塑性", "BCI学习", "皮层重映射", "适应"],
        "insight": "长期使用脑机接口会引发大脑的神经可塑性变化。研究表明，大脑可以学会直接控制BCI信号，就像控制自然肢体一样。这种学习过程涉及运动皮层的神经回路重组，使得原本与肢体运动相关的神经元逐渐适应直接产生BCI输出信号。理解这一过程对于优化BCI训练方案至关重要。",
        "evidence": [
            "猴子可以通过学习直接控制光标，无需肌肉运动",
            "BCI学习过程中运动皮层的神经活动模式发生变化",
            "神经反馈训练可以加速BCI学习过程"
        ],
        "action_items": [
            "设计有效的BCI训练协议以加速神经可塑性",
            "研究个体差异对BCI学习的影响",
            "开发基于神经可塑性的BCI适配技术"
        ],
        "authors": ["神经科学家", "康复医学专家"]
    },
    {
        "title": "深度学习在神经信号解码中的应用",
        "domain": "AI",
        "topics": ["深度学习", "神经信号解码", "LSTM", "CNN"],
        "insight": "深度学习技术已广泛应用于脑机接口的神经信号解码。与传统方法相比，深度学习模型能够自动学习神经信号中的复杂时空特征，显著提高了解码准确率。特别是LSTM网络适合处理时间序列数据，CNN可以提取局部空间特征，而Transformer架构能够捕获长程依赖关系。",
        "evidence": [
            "深度神经网络在运动意图解码任务中准确率超过传统方法",
            "迁移学习可以减少新用户所需的数据量和训练时间",
            "轻量化模型可以满足实时解码的延迟要求"
        ],
        "action_items": [
            "开发更高效的深度学习解码架构",
            "研究小样本学习方法以降低BCI校准负担",
            "探索自监督学习在神经信号分析中的应用"
        ],
        "authors": ["AI研究员", "神经科学家"]
    },
    {
        "title": "低延迟实时BCI系统设计",
        "domain": "AI",
        "topics": ["实时系统", "低延迟", "边缘计算", "嵌入式系统"],
        "insight": "脑机接口的实时性能对用户体验至关重要。系统延迟来源包括神经信号采集、信号处理、解码算法和设备输出等多个环节。为了实现自然流畅的交互体验，总延迟应控制在100毫秒以内。边缘计算和专用硬件加速是降低延迟的有效策略。",
        "evidence": [
            "人类感知延迟约100毫秒，运动响应延迟更短",
            "优化后的神经网络推理延迟可低于10毫秒",
            "专用神经形态芯片可实现微秒级处理"
        ],
        "action_items": [
            "设计端到端的低延迟处理流水线",
            "开发适用于嵌入式设备的轻量化模型",
            "探索硬件加速在BCI系统中的应用"
        ],
        "authors": ["嵌入式系统工程师", "AI研究员"]
    },
    {
        "title": "个性化BCI模型的自适应学习",
        "domain": "AI",
        "topics": ["个性化", "迁移学习", "在线学习", "域适应"],
        "insight": "不同用户之间的神经信号特征存在显著差异，因此需要个性化的解码模型。迁移学习和在线学习方法可以在少量数据的情况下快速适应新用户，显著降低BCI系统的初始校准负担。持续学习机制使模型能够随用户状态变化进行动态调整。",
        "evidence": [
            "基于预训练模型的迁移学习可减少80%的校准数据需求",
            "在线自适应算法可实时跟踪神经信号变化",
            "元学习方法可以在多个用户间快速泛化"
        ],
        "action_items": [
            "建立大规模神经信号数据集以支持迁移学习研究",
            "开发鲁棒的在线学习算法",
            "设计用户友好的个性化校准流程"
        ],
        "authors": ["机器学习研究员", "人机交互专家"]
    },
    {
        "title": "脑机接口的认知隐私问题",
        "domain": "ethics",
        "topics": ["认知隐私", "数据安全", "知情同意", "神经权利"],
        "insight": "脑机接口技术可能使个人的思维活动面临前所未有的暴露风险。与传统数据不同，神经信号可能包含用户的意图、情感甚至是无意识的想法，引发严重的隐私担忧。如何定义、保护和监管认知隐私成为BCI时代的重要伦理议题，需要建立新的法律框架和技术保护机制。",
        "evidence": [
            "神经信号可能泄露比用户主动表达更多的信息",
            "现有的数据保护法律难以充分涵盖神经数据",
            "公众对认知隐私的担忧正在增加"
        ],
        "action_items": [
            "制定专门的神经数据保护法规",
            "开发保护认知隐私的技术方案",
            "建立BCI使用的伦理审查机制"
        ],
        "authors": ["伦理学家", "法律学者", "技术专家"]
    },
    {
        "title": "认知增强的伦理边界",
        "domain": "ethics",
        "topics": ["认知增强", "公平性", "人类增强", "伦理极限"],
        "insight": "脑机接口技术不仅可能恢复丧失的功能，还可能增强正常认知能力，如记忆、注意力或信息处理速度。这种可能性引发了关于公平性、人类身份和伦理边界的深层讨论。增强技术是否应该被允许？在何种条件下允许？如何防止增强技术加剧社会不平等？这些问题需要跨学科的深入探讨。",
        "evidence": [
            "已有研究探索了记忆增强的神经刺激方法",
            "部分科技公司公开支持认知增强技术的发展",
            "公众对认知增强的态度因应用场景而异"
        ],
        "action_items": [
            "建立认知增强技术的分级分类管理框架",
            "开展公众参与的技术伦理讨论",
            "制定防止技术滥用的安全措施"
        ],
        "authors": ["生物伦理学家", "社会学家", "哲学家"]
    },
    {
        "title": "BCI技术的公平获取与社会影响",
        "domain": "ethics",
        "topics": ["技术获取", "数字鸿沟", "健康公平", "普惠技术"],
        "insight": "脑机接口技术目前主要服务于医疗康复领域，但其高昂的成本和技术门槛可能限制其在更广泛人群中的普及。如果BCI成为改善生活质量的重要手段，如何确保不同社会经济背景的人群都能公平获取这项技术，成为需要解决的社会问题。普惠性设计和开源生态可能有助于缩小这一差距。",
        "evidence": [
            "目前BCI设备价格高昂，限制了普及范围",
            "低收入群体获得先进医疗技术的机会较少",
            "开源BCI项目正在降低技术门槛"
        ],
        "action_items": [
            "开发低成本BCI解决方案",
            "建立BCI技术的公共资助和普惠机制",
            "推动BCI技术的开源和可及性"
        ],
        "authors": ["公共政策专家", "社会学家", "技术活动家"]
    },
    {
        "title": "材料科学与BCI电极创新",
        "domain": "materials_science",
        "topics": ["柔性电极", "生物相容性", "长期植入", "纳米材料"],
        "insight": "脑机接口的性能和安全性很大程度上取决于电极材料的选择。传统刚性金属电极会引起免疫反应和神经炎症，限制长期使用。柔性聚合物电极、导电水凝胶和纳米材料提供了更好的生物相容性和更稳定的神经接口，为长期植入式BCI开辟了新可能。",
        "evidence": [
            "柔性电极的免疫响应显著低于刚性电极",
            "导电聚合物可以在神经界面提供更稳定的记录",
            "纳米材料增强的电极具有更高的信噪比"
        ],
        "action_items": [
            "开发下一代生物相容性电极材料",
            "建立长期植入式BCI的安全评估标准",
            "探索可降解电极在临时BCI中的应用"
        ],
        "authors": ["材料科学家", "生物医学工程师"]
    }
]


def push_to_suilight(capsule):
    """推送到 SuiLight"""
    try:
        response = requests.post(
            f"{SUI_LIGHT_URL}/api/capsules/",
            json=capsule,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ SuiLight 失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ SuiLight 错误: {e}")
        return None


def push_to_capsulehub(capsule):
    """推送到 CapsuleHub"""
    try:
        capsule_data = {
            "title": capsule["title"],
            "domain": capsule["domain"].lower(),
            "topics": capsule["topics"],
            "insight": capsule["insight"],
            "evidence": capsule["evidence"],
            "action_items": capsule["action_items"],
            "authors": capsule["authors"]
        }
        
        response = requests.post(
            f"{CAPSULEHUB_URL}/api/capsules/",
            json=capsule_data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ CapsuleHub 失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ CapsuleHub 错误: {e}")
        return None


def main():
    print("\n" + "🚀" * 30)
    print("BCI 脑机接口知识胶囊 - 批量生成")
    print("打通 SuiLight → Kai-Hub → CapsuleHub 完整链路")
    print("🚀" * 30 + "\n")
    
    # 检查服务
    print("📡 检查服务状态...")
    try:
        r = requests.get(f"{SUI_LIGHT_URL}/api/", timeout=5)
        print(f"  ✅ SuiLight: {r.status_code}")
    except:
        print("  ❌ SuiLight 未运行")
        return
    
    try:
        r = requests.get(f"{CAPSULEHUB_URL}/api/capsules/", timeout=5)
        print(f"  ✅ CapsuleHub: {r.status_code}")
    except:
        print("  ❌ CapsuleHub 未运行")
        return
    
    print("\n" + "="*60)
    print("开始批量生成 BCI 知识胶囊...")
    print("="*60)
    
    suilight_count = 0
    capsulehub_count = 0
    
    for i, capsule in enumerate(BCI_CAPSULES, 1):
        print(f"\n[{i}/{len(BCI_CAPSULES)}] {capsule['title'][:40]}...")
        
        # 推送到 SuiLight
        result1 = push_to_suilight(capsule)
        if result1:
            suilight_count += 1
            print(f"  ✅ SuiLight")
        
        # 推送到 CapsuleHub
        result2 = push_to_capsulehub(capsule)
        if result2:
            capsulehub_count += 1
            print(f"  ✅ CapsuleHub")
    
    print("\n" + "="*60)
    print("✅ 批量生成完成！")
    print("="*60)
    print(f"\n📊 统计:")
    print(f"   SuiLight: {suilight_count} 个胶囊")
    print(f"   CapsuleHub: {capsulehub_count} 个胶囊")
    
    print("\n🔗 系统链路:")
    print(f"   SuiLight: {SUI_LIGHT_URL}")
    print(f"   CapsuleHub: {CAPSULEHUB_URL}")
    
    print("\n🎯 下一步:")
    print("   1. 访问 Kai-Hub (启动中): http://localhost:3100")
    print("   2. 查看 BCI 仪表盘: http://localhost:3100/bci")
    print("   3. 触发跨域融合")
    print("   4. 生成融合胶囊")
    
    print("\n" + "✨" * 20)


if __name__ == "__main__":
    main()
