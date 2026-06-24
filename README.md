# RAG-QA-System---2405030244

基于本地知识库的RAG（检索增强生成）智能问答系统，使用Ollama本地大模型、LangChain框架和Streamlit构建。

## 功能特点

- 📄 支持PDF、DOCX和TXT文档上传
- 📚 自动构建本地向量知识库
- 🔍 智能文档检索与问答
- 💬 支持多轮对话记忆
- 🌐 友好的Web交互界面

## 环境要求

- Python 3.9+
- Git
- Ollama（用于本地大模型部署）
- 至少8GB内存（推荐16GB以上）

## 安装步骤

### 1. 安装Git

下载并安装Git：https://git-scm.com/download/win

### 2. 安装Ollama

下载并安装Ollama：https://ollama.com/download

### 3. 下载大模型

打开命令行（cmd）并执行：

```bash
ollama pull qwen2:0.5b
ollama pull nomic-embed-text
```

### 4. 安装依赖

```bash
# 克隆或下载本项目到本地

# 进入项目目录
cd RAG-QA-System-姓名-学号

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 5. 一键安装脚本

也可以直接运行 `install.bat` 脚本（需要管理员权限）

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

应用将在浏览器中打开，通常是 http://localhost:8501

### 使用步骤

1. 在左侧侧边栏上传PDF、DOCX或TXT文档
2. 点击"构建/更新知识库"按钮
3. 在问答区输入问题
4. 点击"提问"按钮获取回答

### 命令行版本

也可以使用命令行版本进行问答：

```bash
python rag_chain.py
```

## 关键技术点

### RAG流程

1. **文档加载**：使用PyPDF2和python-docx解析PDF和DOCX文件
2. **文本分块**：使用RecursiveCharacterTextSplitter进行文本分割（chunk_size=1000, chunk_overlap=200）
3. **向量化**：使用Ollama的nomic-embed-text模型将文本块转换为向量
4. **向量存储**：使用Chroma向量数据库存储向量
5. **检索**：基于相似度检索最相关的文本块
6. **生成**：使用Qwen2-0.5b大模型基于检索到的内容生成回答

### 所用模型

- **大语言模型**：qwen2:0.5b（内存占用小，适合8GB内存环境）
- **嵌入模型**：nomic-embed-text

### 系统提示词

系统使用以下提示词策略：
- 要求模型基于提供的参考文档回答问题
- 如果文档中没有相关信息，明确回答"文档中未找到相关答案"
- 不编造答案，严格基于文档内容进行回答

## 项目结构

```
RAG-QA-System-姓名-学号/
├── app.py              # Streamlit Web应用主入口
├── rag_chain.py        # RAG问答链实现（命令行版本）
├── vector_store.py     # 向量数据库管理
├── document_loader.py  # 文档加载模块
├── test_ollama.py      # Ollama测试脚本
├── requirements.txt    # 依赖列表
├── install.bat         # 一键安装脚本
├── build.bat           # PyInstaller打包脚本
├── app.spec            # PyInstaller配置文件
├── README.md           # 项目说明文档
├── AI_USAGE_LOG.md     # AI使用日志
├── .gitignore          # Git忽略配置
├── docs/               # 文档目录（存放示例文档，共5份NLP相关文档）
├── screenshots/        # 项目截图目录
└── chroma_db/          # Chroma向量数据库目录
```

## 测试问答示例

### 相关问题（应能正确回答）

1. 什么是自然语言处理？
2. NLP的主要应用领域有哪些？
3. RAG技术如何缓解大模型的"幻觉"问题？
4. Transformer架构是什么？
5. 预训练语言模型有哪些？

### 无关问题（应拒答）

1. 今天天气怎么样？
2. 世界上最深的海是什么？

## 本地打包exe

如需将应用打包为独立exe文件：

```bash
# 运行打包脚本
build.bat
```

打包后的exe文件位于 `dist\RAG-QA-System.exe`

**注意**：打包exe前请确保已安装Ollama并下载所需模型。

## 已知问题与改进方向

- ⚠️ 首次运行需要下载模型，耗时较长
- ⚠️ 大模型推理速度较慢，建议使用GPU加速
- 🚀 可添加更多文档格式支持（如Markdown等）
- 🚀 可添加夜间模式
- 🚀 可添加问答记录导出功能
- 🚀 可添加批量上传功能

## 项目截图

### 截图1：初始界面
![初始界面](screenshots/initial.png)

### 截图2：知识库构建
![知识库构建](screenshots/knowledge_base.png)

### 截图3：问答示例
![问答示例](screenshots/qa_example.png)

## License

MIT License