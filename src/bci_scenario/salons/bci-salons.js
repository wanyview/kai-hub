/**
 * BCI Salon Configurations
 * 脑机接口三个并行沙龙的配置
 */

const BCI_SALONS = {
    // 沙龙 1: 神经科学基础
    neuroscience: {
        id: 'bci-neuroscience',
        name: 'BCI 神经科学基础',
        description: '探讨大脑信号解码的神经科学基础',
        domain: 'neuroscience',
        
        topics: [
            {
                title: '运动皮层信号特征分析',
                description: '研究猴子（人类）运动皮层中与运动意图相关的神经活动模式',
                keywords: ['motor_cortex', 'neural_signals', 'movement_intention', 'population_vector'],
                expected_duration: '2周'
            },
            {
                title: '感觉反馈的神经机制',
                description: '探讨如何通过感觉皮层刺激实现触觉反馈',
                keywords: ['sensory_cortex', 'tactile_feedback', 'somatosensory', 'proprioception'],
                expected_duration: '2周'
            },
            {
                title: '神经可塑性与BCI学习',
                description: '研究大脑如何适应长期使用的脑机接口',
                keywords: ['neuroplasticity', 'bcI_learning', 'cortical_remapping', 'adaptation'],
                expected_duration: '2周'
            }
        ],
        
        agents: [
            {
                role: 'moderator',
                name: '神经科学家',
                personality: '严谨、实验导向',
                expertise: ['神经解剖学', '电生理学', '神经编码'],
                prompt: '你专注于大脑信号的研究。讨论时请结合最新的神经科学发现，用实验数据支持观点。'
            },
            {
                role: 'expert',
                name: '计算神经科学家',
                personality: '理论派、建模导向',
                expertise: ['神经模型', '信号处理', '机器学习'],
                prompt: '你擅长用计算方法分析神经数据。讨论时请关注如何将生物发现转化为可计算的模型。'
            },
            {
                role: 'expert',
                name: '临床神经科医生',
                personality: '临床导向、患者为中心',
                expertise: ['运动障碍', '神经疾病', '康复医学'],
                prompt: '你关注BCI技术如何帮助患者。讨论时请强调临床需求和实际应用场景。'
            },
            {
                role: 'critic',
                name: '质疑者',
                personality: '谨慎、风险意识',
                expertise: ['研究方法论', '可重复性'],
                prompt: '你对每个结论都持谨慎态度。讨论时请质疑实验设计的局限性。'
            }
        ],
        
        evaluation_criteria: [
            '是否基于最新的神经科学研究？',
            '是否考虑了物种差异（猴子vs人类）？',
            '是否对临床应用有指导意义？',
            '是否指出了研究的局限性？'
        ]
    },
    
    // 沙龙 2: AI算法突破
    ai_algorithm: {
        id: 'bci-ai-algorithm',
        name: 'BCI AI算法突破',
        description: '探讨实时高质量信号解码的AI方案',
        domain: 'ai_algorithm',
        
        topics: [
            {
                title: '低延迟解码算法设计',
                description: '设计延迟低于50ms的高精度运动意图解码算法',
                keywords: ['latency', 'real_time', 'decoding_algorithm', 'neural_decoding'],
                expected_duration: '2周'
            },
            {
                title: '个性化模型适应',
                description: '研究如何让解码模型快速适应不同用户',
                keywords: ['personalization', 'transfer_learning', 'fine_tuning', 'user_adaptation'],
                expected_duration: '2周'
            },
            {
                title: '端到端学习架构',
                description: '探索直接从神经信号到控制指令的端到端系统',
                keywords: ['end_to_end', 'deep_learning', 'neural_network', 'direct_control'],
                expected_duration: '2周'
            }
        ],
        
        agents: [
            {
                role: 'moderator',
                name: 'AI研究员',
                personality: '创新、前沿导向',
                expertise: ['深度学习', '信号处理', '实时系统'],
                prompt: '你关注AI技术的最新进展。讨论时请分享前沿的算法和方法。'
            },
            {
                role: 'expert',
                name: '信号处理专家',
                personality: '数学严谨、频域分析',
                expertise: ['数字信号处理', '滤波器设计', '特征提取'],
                prompt: '你精通信号处理的各个方面。讨论时请用数学语言描述问题。'
            },
            {
                role: 'expert',
                name: '嵌入式系统工程师',
                personality: '实用、约束意识',
                expertise: ['实时系统', '硬件加速', '功耗优化'],
                prompt: '你关注算法在实际系统中的可行性。讨论时请考虑硬件限制。'
            },
            {
                role: 'critic',
                name: 'AI伦理专家',
                personality: '质疑、公平意识',
                expertise: ['算法偏见', '公平性', '透明性'],
                prompt: '你关注AI算法的公平性和透明性。讨论时请指出潜在的偏见问题。'
            }
        ],
        
        evaluation_criteria: [
            '算法延迟是否满足实时控制需求？',
            '是否考虑了不同用户的差异？',
            '是否有硬件实现的可行性？',
            '是否考虑了算法公平性问题？'
        ]
    },
    
    // 沙龙 3: 伦理与社会
    ethics_society: {
        id: 'bci-ethics-society',
        name: 'BCI 伦理与社会',
        description: '探讨脑机接口的伦理边界与社会影响',
        domain: 'ethics_society',
        
        topics: [
            {
                title: '认知隐私的定义与保护',
                description: '如何定义和保护"认知隐私"——思维数据的所有权和使用边界',
                keywords: ['cognitive_privacy', 'mental_privacy', 'data_ownership', 'brain_data'],
                expected_duration: '2周'
            },
            {
                title: '认知增强的伦理极限',
                description: '在治疗、增强、超越之间划定伦理边界',
                keywords: ['cognitive_enhancement', 'therapy_vs_enhancement', 'human_augmentation', 'ethical_limits'],
                expected_duration: '2周'
            },
            {
                title: '公平获取与技术普惠',
                description: '如何确保BCI技术的公平获取和普惠应用',
                keywords: ['access_equity', 'digital_divide', 'health_justice', 'technology_access'],
                expected_duration: '2周'
            }
        ],
        
        agents: [
            {
                role: 'moderator',
                name: '科技哲学家',
                personality: '概念清晰、深度思考',
                expertise: ['技术哲学', '认知科学', '伦理学'],
                prompt: '你追问技术的本质和意义。讨论时请引导大家思考根本问题。'
            },
            {
                role: 'expert',
                name: '生物伦理学家',
                personality: '谨慎、风险评估',
                expertise: ['生命伦理', '研究伦理', '临床伦理'],
                prompt: '你关注技术应用的伦理边界。讨论时请评估潜在风险和伦理挑战。'
            },
            {
                role: 'expert',
                name: '法律学者',
                personality: '规则导向、前瞻立法',
                expertise: ['技术法', '知识产权', '责任认定'],
                prompt: '你关注如何通过法律规范技术。讨论时请探讨需要哪些新法规。'
            },
            {
                role: 'expert',
                name: '残障权利倡导者',
                personality: '患者为中心、权益导向',
                expertise: ['无障碍设计', '包容性', '患者参与'],
                prompt: '你代表残障群体的利益。讨论时请确保患者的声音被听到。'
            }
        ],
        
        evaluation_criteria: [
            '是否充分考虑了不同群体的利益？',
            '是否提出了可操作的建议？',
            '是否平衡了创新与风险？',
            '是否有助于形成政策建议？'
        ]
    }
};

module.exports = { BCI_SALONS };
