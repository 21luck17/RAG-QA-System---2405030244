import streamlit as st
import ollama
from document_loader import load_document

DOCUMENTS = {}
KB_LOADED = False

def load_knowledge_base():
    global DOCUMENTS, KB_LOADED
    try:
        content = load_document('docs/sample_nlp_intro.txt')
        DOCUMENTS['sample_nlp_intro.txt'] = content
        KB_LOADED = True
        return True
    except Exception as e:
        st.error(f"加载失败: {e}")
        return False

def find_relevant_text(query, content, top_k=2):
    results = []
    query_lower = query.lower()
    query_words = query_lower.split()
    
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        current_section += line + " "
        
        if len(current_section) > 100:
            score = 0
            for word in query_words:
                if word in current_section.lower():
                    score += 1
            
            if score > 0:
                results.append({
                    'content': current_section.strip()[:250],
                    'score': score
                })
            current_section = ""
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def generate_answer(query):
    if not DOCUMENTS:
        return "请先加载知识库"
    
    content = "\n".join(DOCUMENTS.values())
    relevant = find_relevant_text(query, content)
    
    if not relevant:
        context = content[:500]
        has_relevant = False
    else:
        context = "\n".join([f"参考内容{i+1}:\n{r['content']}" for i, r in enumerate(relevant)])
        has_relevant = True
    
    prompt = f"""基于以下参考文档回答问题：

参考文档：
{context}

问题：{query}

请严格基于提供的参考文档回答，不要编造信息。如果文档中没有相关信息，请明确说"文档中未找到相关答案"。

回答："""
    
    response = ollama.chat(model='qwen2:0.5b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def main():
    global KB_LOADED
    
    st.set_page_config(page_title="RAG智能问答系统", page_icon="📚", layout="wide")
    
    st.title("📚 RAG智能问答系统")
    st.subheader("基于本地知识库的智能问答")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    with st.sidebar:
        st.header("知识库管理")
        
        if not KB_LOADED:
            if st.button("加载知识库"):
                with st.spinner("正在加载..."):
                    if load_knowledge_base():
                        st.success("✅ 知识库加载成功")
        else:
            st.success("✅ 知识库已加载")
            st.write(f"文档数量: {len(DOCUMENTS)}")
            for fname in DOCUMENTS.keys():
                st.write(f"📄 {fname}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("问答交互")
        
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                st.write(answer)
        
        question = st.text_input("请输入您的问题：", key="question_input")
        
        if st.button("提问", key="ask_button"):
            if question.strip():
                if KB_LOADED:
                    with st.spinner("正在回答..."):
                        answer = generate_answer(question)
                        st.session_state.chat_history.append((question, answer))
                        st.rerun()
                else:
                    st.warning("请先加载知识库")
            else:
                st.warning("请输入问题")
    
    with col2:
        st.header("系统状态")
        
        if KB_LOADED:
            st.success("✅ 系统就绪")
            st.write(f"对话历史：{len(st.session_state.chat_history)} 条")
        else:
            st.info("📋 等待加载知识库")
        
        st.subheader("测试问题")
        test_questions = [
            "什么是自然语言处理？",
            "NLP的主要任务有哪些？",
            "今天天气怎么样？"
        ]
        
        for q in test_questions:
            if st.button(q):
                if KB_LOADED:
                    with st.spinner("正在回答..."):
                        answer = generate_answer(q)
                        st.session_state.chat_history.append((q, answer))
                        st.rerun()

if __name__ == "__main__":
    main()