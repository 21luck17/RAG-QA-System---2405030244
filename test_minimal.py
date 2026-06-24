import os
import sys

print("测试1: 基础嵌入")
import ollama
r = ollama.embeddings(model='nomic-embed-text', prompt='test')
print(f"嵌入长度: {len(r['embedding'])}")

print("\n测试2: 文档加载")
from document_loader import load_document
content = load_document('docs/transformer_architecture.txt')
print(f"文档长度: {len(content)}")

print("\n测试3: 创建向量DB")
from vector_store import create_vector_db, split_text

# 创建测试文档
test_docs = [{"filename": "test.txt", "content": content[:500]}]
print(f"测试文档长度: {len(test_docs[0]['content'])}")

try:
    vectordb = create_vector_db(test_docs)
    print("✅ 向量DB创建成功")
except Exception as e:
    print(f"❌ 失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成")