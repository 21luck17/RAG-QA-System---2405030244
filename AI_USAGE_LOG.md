# AI使用日志

本文档记录在本项目开发过程中向AI工具（Trae/GitHub Copilot）提问的内容，用于符合课程作业要求。

## AI使用记录

### 1. 代码结构设计咨询

**向AI提问**：
我正在开发一个基于本地知识库的RAG智能问答系统，使用Ollama+LangChain+Streamlit。请帮我设计代码结构，需要包含哪些模块？

**AI回答摘要**：
建议模块划分：
- `app.py`：Streamlit Web主入口
- `rag_chain.py`：RAG问答链核心逻辑
- `vector_store.py`：向量数据库管理
- `document_loader.py`：文档加载解析
- `test_ollama.py`：Ollama连接测试

这种模块化设计符合单一职责原则，便于维护和扩展。

---

### 2. LangChain RAG链配置问题

**向AI提问**：
使用LangChain的ConversationalRetrievalChain时，如何让模型在文档中没有相关信息时明确回答"文档中未找到相关答案"？

**AI回答摘要**：
可以通过`combine_docs_chain_kwargs`参数传递自定义提示词：

```python
SYSTEM_PROMPT = """
基于提供的参考文档回答问题。
如果文档中没有相关信息，请明确回答"文档中未找到相关答案"。
不要编造答案，严格基于文档内容进行回答。
"""

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": SYSTEM_PROMPT}
)
```

---

### 3. Streamlit会话状态管理

**向AI提问**：
如何在Streamlit中实现多轮对话记忆？我需要让系统记住之前的问答历史。

**AI回答摘要**：
使用`st.session_state`来存储对话历史：

```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 每次问答后追加历史
st.session_state.chat_history.append((question, answer))

# 在界面上显示历史
for question, answer in st.session_state.chat_history:
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(answer)
```

---

### 4. Chroma向量数据库持久化

**向AI提问**：
Chroma向量数据库如何持久化存储？我希望重启应用后知识库数据不会丢失。

**AI回答摘要**：
Chroma支持通过`persist_directory`参数持久化：

```python
vectordb = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
# 添加数据后需要调用persist()
vectordb.add_texts(texts=all_chunks, metadatas=all_metadatas)
vectordb.persist()
```

---

### 5. PyInstaller打包Streamlit应用

**向AI提问**：
如何使用PyInstaller将Streamlit应用打包成exe？有哪些特殊的hiddenimports需要配置？

**AI回答摘要**：
创建.spec文件时需要添加以下hiddenimports：

```python
hiddenimports=[
    'streamlit',
    'langchain',
    'langchain_core',
    'langchain_community',
    'langchain_chroma',
    'langchain_ollama',
    'chromadb',
    'PyPDF2',
    'docx',
    'tiktoken',
    'ollama',
],
```

同时需要通过`datas`参数包含docs文件夹等资源文件。

---

### 6. 向量数据库统计信息获取

**向AI提问**：
如何获取Chroma向量数据库中的文档数量和文本块数量，用于在Streamlit界面显示知识库状态？

**AI回答摘要**：
可以通过`vectordb._collection.count()`获取文本块数量，通过`vectordb.get()`获取所有数据后统计来源文档数：

```python
def get_vector_db_stats():
    vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    chunk_count = vectordb._collection.count()
    results = vectordb.get()
    sources = list(set([meta.get("source") for meta in results.get("metadatas", [])]))
    return {"document_count": len(sources), "chunk_count": chunk_count}
```

---

### 7. 文档格式支持扩展

**向AI提问**：
项目要求支持PDF和DOCX格式，我还想添加TXT格式支持，代码需要如何修改？

**AI回答摘要**：
在`document_loader.py`中添加TXT加载函数，并在`load_document`中注册：

```python
def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return load_pdf(file_path)
    elif ext == '.docx':
        return load_docx(file_path)
    elif ext == '.txt':
        return load_txt(file_path)
```

同时在Streamlit的file_uploader中也需要添加`type=["pdf", "docx", "txt"]`。

---

### 8. pyinstaller打包后资源文件路径问题

**向AI提问**：
打包成exe后，如何确保docs等资源文件夹能被正确访问？

**AI回答摘要**：
使用`sys._MEIPASS`处理打包后的路径：

```python
import sys
import os

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 使用示例
docs_path = get_resource_path('docs')
```

---

## 总结

通过AI辅助，我完成了：
1. 代码架构设计
2. LangChain RAG链的配置调试
3. Streamlit会话状态管理
4. 向量数据库持久化方案
5. PyInstaller打包配置
6. 知识库状态显示功能

所有AI生成的代码都已理解并根据项目实际情况修改使用。
