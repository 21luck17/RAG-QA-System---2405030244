import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"

def split_text(text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks

def create_vector_db(documents):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    if os.path.exists(CHROMA_DB_PATH) and os.listdir(CHROMA_DB_PATH):
        vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        existing_count = vectordb._collection.count()
        print(f"Existing vector DB found with {existing_count} chunks")
    else:
        vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    
    all_chunks = []
    all_metadatas = []
    
    for doc in documents:
        chunks = split_text(doc["content"])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": doc["filename"],
                "chunk_index": i,
                "total_chunks": len(chunks)
            })
    
    if all_chunks:
        vectordb.add_texts(texts=all_chunks, metadatas=all_metadatas)
        vectordb.persist()
        print(f"Added {len(all_chunks)} chunks to vector DB")
    
    return vectordb

def get_retriever(k=3):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": k})

def search_similar(query, k=3):
    retriever = get_retriever(k=k)
    docs = retriever.get_relevant_documents(query)
    results = []
    for doc in docs:
        results.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "chunk_index": doc.metadata.get("chunk_index", 0)
        })
    return results

if __name__ == "__main__":
    from document_loader import load_documents_from_folder
    
    docs = load_documents_from_folder("docs")
    if docs:
        create_vector_db(docs)
        
        query = "natural language processing"
        results = search_similar(query)
        print(f"\nSearch results for '{query}':")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Source: {result['source']}")
            print(f"Content snippet: {result['content'][:200]}...")