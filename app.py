import streamlit as st
import os
import tempfile
from document_loader import load_document
from vector_store import create_vector_db
from rag_chain import create_rag_chain, ask_question

def main():
    st.set_page_config(page_title="RAG智能问答系统", page_icon="📚", layout="wide")
    
    st.title("📚 RAG智能问答系统")
    st.subheader("基于本地知识库的智能问答")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "chain" not in st.session_state:
        st.session_state.chain = None
    
    if "db_initialized" not in st.session_state:
        st.session_state.db_initialized = False
    
    with st.sidebar:
        st.header("知识库管理")
        
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="支持PDF、DOCX和TXT格式的文档"
        )
        
        if st.button("构建/更新知识库"):
            if uploaded_files:
                with st.spinner("正在处理文档..."):
                    documents = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                            temp_file.write(uploaded_file.getvalue())
                            temp_file_path = temp_file.name
                        
                        text = load_document(temp_file_path)
                        if text:
                            documents.append({"filename": uploaded_file.name, "content": text})
                        os.unlink(temp_file_path)
                    
                    if documents:
                        create_vector_db(documents)
                        st.session_state.db_initialized = True
                        st.session_state.chain = create_rag_chain()
                        st.success(f"成功处理 {len(documents)} 份文档！")
                    else:
                        st.error("未能提取文档内容")
            else:
                st.warning("请先上传文档")
        
        if st.session_state.db_initialized:
            st.info("知识库已初始化")
    
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
                if st.session_state.chain:
                    with st.spinner("正在思考..."):
                        answer = ask_question(st.session_state.chain, question)
                        st.session_state.chat_history.append((question, answer))
                        st.rerun()
                else:
                    st.warning("请先构建知识库")
            else:
                st.warning("请输入问题")
    
    with col2:
        st.header("知识库状态")
        
        if st.session_state.db_initialized:
            st.success("✅ 知识库已构建")
            st.write(f"对话历史：{len(st.session_state.chat_history)} 条")
        else:
            st.info("📋 知识库尚未构建")
            st.write("请上传文档并点击'构建知识库'按钮")
        
        st.subheader("使用说明")
        st.write("1. 在左侧上传PDF、DOCX或TXT文档")
        st.write("2. 点击'构建/更新知识库'")
        st.write("3. 在问答区输入问题")
        st.write("4. 点击'提问'获取回答")

if __name__ == "__main__":
    main()