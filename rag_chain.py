from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from vector_store import get_retriever

LLM_MODEL = "qwen2:0.5b"

def create_rag_chain():
    llm = ChatOllama(model=LLM_MODEL)
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    retriever = get_retriever(k=3)
    
    template = """
基于提供的参考文档回答问题。
如果文档中没有相关信息，请明确回答"文档中未找到相关答案"。
不要编造答案，严格基于文档内容进行回答。

参考文档：
{context}

问题：{question}

回答：
"""
    
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
        verbose=False
    )
    
    return chain

def ask_question(chain, question):
    try:
        result = chain({"question": question})
        return result["answer"]
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Initializing RAG chain...")
    chain = create_rag_chain()
    print("RAG chain ready!\n")
    
    while True:
        question = input("请输入问题（输入 'exit' 退出）：")
        if question.lower() == 'exit':
            break
        
        answer = ask_question(chain, question)
        print(f"\n回答：{answer}\n")