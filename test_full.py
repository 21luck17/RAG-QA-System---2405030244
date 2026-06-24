import os
import sys

print("=" * 50)
print("RAG智能问答系统 - 完整测试")
print("=" * 50)

# 清理旧数据库
print("\n【1】清理旧数据库")
from vector_store import clear_vector_db
clear_vector_db()

# 加载文档
print("\n【2】加载文档")
from document_loader import load_documents_from_folder
docs = load_documents_from_folder('docs')
print(f"已加载 {len(docs)} 份文档")

# 构建知识库（使用所有文档）
print("\n【3】构建知识库")
from vector_store import create_vector_db
try:
    vectordb = create_vector_db(docs)
    print("✅ 知识库构建成功")
except Exception as e:
    print(f"❌ 知识库构建失败: {e}")
    sys.exit(1)

# 测试搜索
print("\n【4】测试搜索")
from vector_store import search_similar
query = "Transformer架构"
results = search_similar(query)
print(f"搜索 '{query}' 找到 {len(results)} 条结果")
if results:
    print(f"来源: {results[0]['source']}")
    print(f"摘要: {results[0]['content'][:100]}...")
    print("✅ 搜索功能正常")
else:
    print("❌ 未找到结果")

# 测试RAG问答
print("\n【5】测试RAG问答")
from rag_chain import create_rag_chain, ask_question
try:
    chain = create_rag_chain()
    answer = ask_question(chain, "什么是Transformer架构？")
    print(f"问题: 什么是Transformer架构？")
    print(f"回答: {answer}")
    print("✅ RAG问答功能正常")
except Exception as e:
    print(f"❌ RAG问答失败: {e}")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)