/**
 * SalonManager: 沙龙管理器
 * 连接和管理多个知识沙龙
 */

const { v4: uuidv4 } = require('uuid');

class SalonManager {
    constructor(knowledgeGraph, router) {
        this.knowledgeGraph = knowledgeGraph;
        this.router = router;
        this.salons = new Map();
        this.adapters = {
            'suilight': new SuiLightAdapter(),
            'capsulehub': new CapsuleHubAdapter(),
            'external': new ExternalAdapter()
        };
    }
    
    get_stats() {
        return {
            total: this.salons.size,
            active: [...this.salons.values()].filter(s => s.status === 'active').length,
            types: [...this.salons.values()].reduce((acc, s) => {
                acc[s.type] = (acc[s.type] || 0) + 1;
                return acc;
            }, {})
        };
    }
    
    get_active_salons() {
        return [...this.salons.values()].filter(s => s.status === 'active');
    }
    
    list_salons() {
        return [...this.salons.values()].map(s => ({
            id: s.id,
            name: s.name,
            type: s.type,
            status: s.status,
            connected_at: s.connected_at,
            stats: s.stats
        }));
    }
    
    async connect_salon(type, config) {
        const adapter = this.adapters[type];
        if (!adapter) {
            throw new Error(`Unknown salon type: ${type}`);
        }
        
        const salon = {
            id: uuidv4(),
            type,
            name: config.name || `${type}_${Date.now()}`,
            status: 'connecting',
            adapter,
            config,
            connected_at: new Date().toISOString(),
            stats: {
                topics: 0,
                discussions: 0,
                capsules: 0
            }
        };
        
        try {
            // 测试连接
            await adapter.test_connection(config);
            
            // 获取初始数据
            const initialData = await adapter.get_initial_data(config);
            
            salon.status = 'active';
            salon.stats = {
                topics: initialData.topics?.length || 0,
                discussions: initialData.discussions?.length || 0,
                capsules: initialData.capsules?.length || 0
            };
            
            // 注册到知识图谱
            await this.knowledgeGraph.register_salon(salon);
            
            this.salons.set(salon.id, salon);
            
            console.log(`✅ 已连接沙龙: ${salon.name} (${type})`);
            
            return salon;
        } catch (error) {
            salon.status = 'error';
            salon.error = error.message;
            this.salons.set(salon.id, salon);
            throw error;
        }
    }
    
    disconnect_salon(salonId) {
        const salon = this.salons.get(salonId);
        if (!salon) return false;
        
        salon.adapter?.disconnect?.(salon.config);
        this.salons.delete(salonId);
        
        console.log(`❌ 已断开沙龙: ${salon.name}`);
        return true;
    }
    
    async get_recent_updates(salonId) {
        const salon = this.salons.get(salonId);
        if (!salon) return [];
        
        return await salon.adapter.get_recent_updates(salon.config);
    }
}

// 适配器基类
class BaseAdapter {
    async test_connection(config) { return true; }
    async get_initial_data(config) { return {}; }
    async get_recent_updates(config) { return []; }
    disconnect(config) {}
}

// SuiLight 适配器
class SuiLightAdapter extends BaseAdapter {
    async test_connection(config) {
        try {
            const response = await fetch(`${config.url}/api/`);
            return response.ok;
        } catch {
            throw new Error('Cannot connect to SuiLight');
        }
    }
    
    async get_initial_data(config) {
        try {
            const [topicsRes, capsulesRes] = await Promise.all([
                fetch(`${config.url}/api/discussions/topics/`),
                fetch(`${config.url}/api/capsules/`)
            ]);
            
            const topics = await topicsRes.json();
            const capsules = await capsulesRes.json();
            
            return {
                topics: topics.topics || [],
                capsules: capsules.capsules || []
            };
        } catch (error) {
            console.error('Failed to get SuiLight data:', error);
            return {};
        }
    }
    
    async get_recent_updates(config) {
        // 实现增量更新检查
        return [];
    }
}

// CapsuleHub 适配器
class CapsuleHubAdapter extends BaseAdapter {
    async test_connection(config) {
        try {
            const response = await fetch(`${config.url}/api/capsules/`);
            return response.ok;
        } catch {
            throw new Error('Cannot connect to CapsuleHub');
        }
    }
    
    async get_initial_data(config) {
        try {
            const response = await fetch(`${config.url}/api/capsules/?limit=50`);
            const data = await response.json();
            return { capsules: data.capsules || [] };
        } catch (error) {
            console.error('Failed to get CapsuleHub data:', error);
            return {};
        }
    }
    
    async get_recent_updates(config) {
        return [];
    }
}

// 外部系统适配器
class ExternalAdapter extends BaseAdapter {
    async test_connection(config) {
        if (!config.endpoint) {
            throw new Error('Missing endpoint config');
        }
        return true;
    }
    
    async get_initial_data(config) {
        return config.initialData || {};
    }
    
    async get_recent_updates(config) {
        return [];
    }
}

module.exports = { SalonManager };
