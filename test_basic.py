import os
import sys

print("=" * 50)
print("RAG智能问答系统 - 基础测试")
print("=" * 50)

# 测试文档加载
print("\n【1】测试文档加载")
from document_loader import load_documents_from_folder, load_document

# 测试单文件加载
test_file = "docs/transformer_architecture.txt"
if os.path.exists(test_file):
    content = load_document(test_file)
    print(f"成功加载: {test_file}")
    print(f"内容长度: {len(content)} 字符")
    print(f"内容预览:\n{content[:200]}...")
else:
    print(f"文件不存在: {test_file}")
    sys.exit(1)

# 测试文件夹加载
print("\n【2】测试文件夹加载")
docs = load_documents_from_folder('docs')
print(f"成功加载 {len(docs)} 份文档")
for doc in docs:
    print(f"  - {doc['filename']}: {len(doc['content'])} 字符")

print("\n【3】测试文本分块")
from vector_store import split_text
chunks = split_text(content, chunk_size=500, chunk_overlap=100)
print(f"分块数量: {len(chunks)}")
for i, chunk in enumerate(chunks[:3], 1):
    print(f"  块{i}: {len(chunk)} 字符")

print("\n" + "=" * 50)
print("✅ 基础测试通过！")
print("=" * 50)