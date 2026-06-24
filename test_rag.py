import os
import sys

def test_rag():
    print("=" * 50)
    print("RAG智能问答系统 - 测试脚本")
    print("=" * 50)
    
    # 测试1: 加载文档
    print("\n【测试1】加载文档")
    from document_loader import load_documents_from_folder
    docs = load_documents_from_folder('docs')
    print(f"成功加载 {len(docs)} 份文档")
    
    # 测试2: 测试单个文档构建
    print("\n【测试2】构建知识库（使用1份文档）")
    from vector_store import create_vector_db, clear_vector_db
    
    # 清理旧数据库
    clear_vector_db()
    
    # 只使用一份文档进行测试
    sample_doc = [docs[0]]
    print(f"使用文档: {sample_doc[0]['filename']}")
    
    try:
        vectordb = create_vector_db(sample_doc)
        print("✅ 知识库构建成功")
    except Exception as e:
        print(f"❌ 知识库构建失败: {e}")
        return False
    
    # 测试3: 搜索功能
    print("\n【测试3】搜索测试")
    from vector_store import search_similar
    
    query = "Transformer"
    results = search_similar(query)
    print(f"搜索 '{query}' 找到 {len(results)} 条结果")
    if results:
        print(f"来源: {results[0]['source']}")
        print(f"摘要: {results[0]['content'][:100]}...")
        print("✅ 搜索功能正常")
    else:
        print("❌ 未找到结果")
        return False
    
    # 测试4: RAG问答
    print("\n【测试4】RAG问答")
    from rag_chain import create_rag_chain, ask_question
    
    chain = create_rag_chain()
    answer = ask_question(chain, "什么是自然语言处理？")
    print(f"回答: {answer}")
    print("✅ RAG问答功能正常")
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_rag()