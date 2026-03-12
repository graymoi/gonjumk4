"""
向量记忆系统
借鉴DeerFlow的长期记忆设计，实现智能记忆存储与检索
"""

import json
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import math


@dataclass
class MemoryEntry:
    id: str
    content: str
    embedding: List[float]
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    importance: float = 0.5
    memory_type: str = "general"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "embedding": self.embedding[:10] if self.embedding else [],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "importance": self.importance,
            "memory_type": self.memory_type
        }


class SimpleEmbedding:
    """简单的文本嵌入实现（可替换为真实嵌入模型）"""
    
    def __init__(self, dim: int = 128):
        self.dim = dim
    
    def encode(self, text: str) -> List[float]:
        text_hash = hashlib.md5(text.encode()).hexdigest()
        seed = int(text_hash[:8], 16)
        
        embedding = []
        for i in range(self.dim):
            val = math.sin(seed * (i + 1) * 0.1) * math.cos(seed * (i + 2) * 0.05)
            embedding.append(val)
        
        norm = math.sqrt(sum(x * x for x in embedding))
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding


class VectorMemory:
    """向量记忆系统"""
    
    def __init__(self, persist_path: str = "data/memory"):
        self.persist_path = Path(persist_path)
        self.persist_path.mkdir(parents=True, exist_ok=True)
        
        self.memories: List[MemoryEntry] = []
        self.embedder = SimpleEmbedding()
        self.index_file = self.persist_path / "memories.json"
        
        self._load_memories()
    
    def _load_memories(self):
        """加载持久化记忆"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = [
                        MemoryEntry(
                            id=m["id"],
                            content=m["content"],
                            embedding=m.get("embedding", []),
                            metadata=m.get("metadata", {}),
                            created_at=datetime.fromisoformat(m["created_at"]) if m.get("created_at") else datetime.now(),
                            access_count=m.get("access_count", 0),
                            importance=m.get("importance", 0.5),
                            memory_type=m.get("memory_type", "general")
                        )
                        for m in data
                    ]
            except Exception as e:
                self.memories = []
    
    def _persist(self):
        """持久化记忆"""
        data = [asdict(m) for m in self.memories]
        for d in data:
            d["created_at"] = d["created_at"].isoformat()
            if len(d.get("embedding", [])) > 10:
                d["embedding"] = d["embedding"][:10]
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def store(
        self,
        content: str,
        metadata: Dict = None,
        memory_type: str = "general",
        importance: float = 0.5
    ) -> str:
        """存储记忆"""
        entry = MemoryEntry(
            id=self._generate_id(content),
            content=content,
            embedding=self.embedder.encode(content),
            metadata=metadata or {},
            memory_type=memory_type,
            importance=importance
        )
        
        existing = next((m for m in self.memories if m.id == entry.id), None)
        if existing:
            existing.access_count += 1
            existing.importance = min(1.0, existing.importance + 0.1)
        else:
            self.memories.append(entry)
        
        self._persist()
        return entry.id
    
    def recall(
        self,
        query: str,
        top_k: int = 5,
        memory_type: str = None
    ) -> List[Dict]:
        """检索相关记忆"""
        query_embedding = self.embedder.encode(query)
        
        candidates = self.memories
        if memory_type:
            candidates = [m for m in self.memories if m.memory_type == memory_type]
        
        scored = []
        for memory in candidates:
            similarity = self._cosine_similarity(query_embedding, memory.embedding)
            recency = self._recency_score(memory.created_at)
            access = min(1.0, memory.access_count / 10)
            
            final_score = (
                similarity * 0.5 +
                recency * 0.2 +
                access * 0.1 +
                memory.importance * 0.2
            )
            
            scored.append((memory, final_score, similarity))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for memory, final_score, similarity in scored[:top_k]:
            memory.access_count += 1
            results.append({
                "id": memory.id,
                "content": memory.content,
                "metadata": memory.metadata,
                "similarity": round(similarity, 4),
                "final_score": round(final_score, 4),
                "memory_type": memory.memory_type,
                "created_at": memory.created_at.isoformat()
            })
        
        self._persist()
        return results
    
    def forget(self, memory_id: str) -> bool:
        """删除记忆"""
        for i, m in enumerate(self.memories):
            if m.id == memory_id:
                self.memories.pop(i)
                self._persist()
                return True
        return False
    
    def consolidate(self, threshold_days: int = 30) -> int:
        """记忆整合：删除低重要性且长期未访问的记忆"""
        now = datetime.now()
        to_remove = []
        
        for memory in self.memories:
            age_days = (now - memory.created_at).days
            if age_days > threshold_days and memory.importance < 0.3 and memory.access_count < 2:
                to_remove.append(memory.id)
        
        for mid in to_remove:
            self.forget(mid)
        
        return len(to_remove)
    
    def get_context(self, query: str, max_tokens: int = 2000) -> str:
        """获取上下文（用于LLM输入）"""
        memories = self.recall(query, top_k=10)
        
        context_parts = []
        total_length = 0
        
        for m in memories:
            content = m["content"]
            if total_length + len(content) > max_tokens:
                break
            context_parts.append(f"[{m['memory_type']}] {content}")
            total_length += len(content)
        
        return "\n".join(context_parts)
    
    def _generate_id(self, content: str) -> str:
        """生成记忆ID"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """计算余弦相似度"""
        if not a or not b or len(a) != len(b):
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def _recency_score(self, created_at: datetime) -> float:
        """计算新近度得分"""
        now = datetime.now()
        age_days = (now - created_at).days
        
        if age_days == 0:
            return 1.0
        elif age_days < 7:
            return 0.9
        elif age_days < 30:
            return 0.7
        elif age_days < 90:
            return 0.5
        else:
            return 0.3
    
    def stats(self) -> Dict:
        """获取记忆统计"""
        type_counts = {}
        for m in self.memories:
            type_counts[m.memory_type] = type_counts.get(m.memory_type, 0) + 1
        
        return {
            "total_memories": len(self.memories),
            "by_type": type_counts,
            "avg_importance": sum(m.importance for m in self.memories) / len(self.memories) if self.memories else 0,
            "total_access": sum(m.access_count for m in self.memories)
        }


class PolicyMemory(VectorMemory):
    """政策专用记忆系统"""
    
    def __init__(self, persist_path: str = "data/memory/policy"):
        super().__init__(persist_path)
    
    def store_policy(
        self,
        policy_name: str,
        policy_content: str,
        metadata: Dict = None
    ) -> str:
        """存储政策记忆"""
        return self.store(
            content=f"{policy_name}\n{policy_content}",
            metadata=metadata or {},
            memory_type="policy",
            importance=0.8
        )
    
    def store_workflow(
        self,
        workflow_name: str,
        workflow_result: Dict,
        metadata: Dict = None
    ) -> str:
        """存储工作流记忆"""
        return self.store(
            content=json.dumps(workflow_result, ensure_ascii=False),
            metadata={"workflow_name": workflow_name, **(metadata or {})},
            memory_type="workflow",
            importance=0.6
        )
    
    def store_learning(
        self,
        learning_content: str,
        metadata: Dict = None
    ) -> str:
        """存储学习记忆"""
        return self.store(
            content=learning_content,
            metadata=metadata or {},
            memory_type="learning",
            importance=0.7
        )
    
    def recall_policies(self, query: str, top_k: int = 5) -> List[Dict]:
        """检索政策记忆"""
        return self.recall(query, top_k=top_k, memory_type="policy")
    
    def recall_workflows(self, query: str, top_k: int = 5) -> List[Dict]:
        """检索工作流记忆"""
        return self.recall(query, top_k=top_k, memory_type="workflow")


vector_memory = VectorMemory()
policy_memory = PolicyMemory()
