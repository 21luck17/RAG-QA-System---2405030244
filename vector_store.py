import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
BATCH_SIZE = 5

def get_embeddings():
    return OllamaEmbeddings(model=EMBEDDING_MODEL)

def split_text(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks

def create_vector_db(documents):
    embeddings = get_embeddings()
    
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
        total_chunks = len(all_chunks)
        print(f"Processing {total_chunks} chunks in batches...")
        
        for i in range(0, total_chunks, BATCH_SIZE):
            batch_chunks = all_chunks[i:i+BATCH_SIZE]
            batch_metadatas = all_metadatas[i:i+BATCH_SIZE]
            
            try:
                vectordb.add_texts(texts=batch_chunks, metadatas=batch_metadatas)
                vectordb.persist()
                print(f"Processed {min(i+BATCH_SIZE, total_chunks)}/{total_chunks} chunks")
            except Exception as e:
                print(f"Error adding batch {i//BATCH_SIZE}: {e}")
                raise
        
        print(f"Successfully added {total_chunks} chunks to vector DB")
    
    return vectordb

def get_retriever(k=3):
    embeddings = get_embeddings()
    vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": k})

def get_vector_db_stats():
    if not os.path.exists(CHROMA_DB_PATH) or not os.listdir(CHROMA_DB_PATH):
        return {"document_count": 0, "chunk_count": 0, "sources": []}
    embeddings = get_embeddings()
    vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    chunk_count = vectordb._collection.count()
    results = vectordb.get()
    sources = list(set([meta.get("source", "unknown") for meta in results.get("metadatas", [])]))
    return {"document_count": len(sources), "chunk_count": chunk_count, "sources": sources}

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

def clear_vector_db():
    import shutil
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)
        print("Vector DB cleared")

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