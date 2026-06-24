import os
from document_loader import load_document
from vector_store import create_vector_db, clear_vector_db, get_vector_db_stats

def initialize_knowledge_base():
    print("=" * 50)
    print("初始化知识库")
    print("=" * 50)
    
    print("\n清理旧知识库...")
    clear_vector_db()
    
    print("\n加载单个文档...")
    content = load_document('docs/sample_nlp_intro.txt')
    print(f"文档长度: {len(content)} 字符")
    
    docs = [{"filename": "sample_nlp_intro.txt", "content": content[:2000]}]
    
    print("\n构建向量数据库...")
    create_vector_db(docs)
    
    stats = get_vector_db_stats()
    print(f"\n✅ 知识库初始化完成！")
    print(f"   文档数量: {stats['document_count']}")
    print(f"   文本块数量: {stats['chunk_count']}")

if __name__ == "__main__":
    initialize_knowledge_base()