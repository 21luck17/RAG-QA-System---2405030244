import streamlit as st
import os
import tempfile
from document_loader import load_document
from vector_store import create_vector_db, get_vector_db_stats, clear_vector_db

def main():
    st.set_page_config(page_title="RAG智能问答系统", page_icon="📚", layout="wide")
    
    st.title("📚 RAG智能问答系统")
    st.subheader("基于本地知识库的智能问答")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "db_initialized" not in st.session_state:
        st.session_state.db_initialized = False
    
    with st.sidebar:
        st.header("知识库管理")
        
        uploaded_files = st.file_uploader(
            "上传文档",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=False,
            help="支持PDF、DOCX和TXT格式的文档（单次上传一个）"
        )
        
        if st.button("构建/更新知识库"):
            if uploaded_files:
                with st.spinner("正在处理文档..."):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_files.name)[1]) as temp_file:
                            temp_file.write(uploaded_files.getvalue())
                            temp_file_path = temp_file.name
                        
                        text = load_document(temp_file_path)
                        os.unlink(temp_file_path)
                        
                        if text:
                            documents = [{"filename": uploaded_files.name, "content": text}]
                            st.info(f"文档内容长度: {len(text)} 字符")
                            
                            create_vector_db(documents)
                            st.session_state.db_initialized = True
                            st.success(f"成功处理文档: {uploaded_files.name}")
                        else:
                            st.error("未能提取文档内容")
                    except Exception as e:
                        st.error(f"处理失败: {str(e)}")
            else:
                st.warning("请先上传文档")
        
        if st.button("清空知识库"):
            clear_vector_db()
            st.session_state.db_initialized = False
            st.session_state.chat_history = []
            st.success("知识库已清空")
    
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
                if st.session_state.db_initialized:
                    with st.spinner("正在检索..."):
                        try:
                            from rag_chain import create_rag_chain, ask_question
                            
                            chain = create_rag_chain()
                            answer = ask_question(chain, question)
                            st.session_state.chat_history.append((question, answer))
                            st.rerun()
                        except Exception as e:
                            st.error(f"问答失败: {str(e)}")
                else:
                    st.warning("请先构建知识库")
            else:
                st.warning("请输入问题")
    
    with col2:
        st.header("知识库状态")
        
        if st.session_state.db_initialized:
            stats = get_vector_db_stats()
            st.success("✅ 知识库已构建")
            st.metric("文档数量", stats["document_count"])
            st.metric("文本块数量", stats["chunk_count"])
            st.write(f"对话历史：{len(st.session_state.chat_history)} 条")
            if stats["sources"]:
                with st.expander("已加载文档"):
                    for src in stats["sources"]:
                        st.write(f"📄 {src}")
        else:
            st.info("📋 知识库尚未构建")
            st.write("请上传文档并点击'构建知识库'按钮")
        
        st.subheader("使用说明")
        st.write("1. 上传PDF、DOCX或TXT文档")
        st.write("2. 点击'构建/更新知识库'")
        st.write("3. 在问答区输入问题")
        st.write("4. 点击'提问'获取回答")

if __name__ == "__main__":
    main()