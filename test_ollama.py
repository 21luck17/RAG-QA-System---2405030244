import ollama

def test_ollama_connection(model="qwen2:0.5b"):
    try:
        response = ollama.chat(model=model, messages=[
            {'role': 'user', 'content': 'Hello, how are you?'}
        ])
        print("✅ Ollama API connection successful!")
        print("Model:", model)
        print("Response:", response['message']['content'])
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print("Please make sure Ollama is installed and running, and the model is downloaded.")
        print("Install Ollama: https://ollama.com/download")
        print(f"Download model: ollama pull {model}")
        return False

def test_embedding():
    try:
        response = ollama.embeddings(model="nomic-embed-text", prompt="test")
        print("✅ Embedding model connection successful!")
        print("Embedding dimension:", len(response["embedding"]))
        return True
    except Exception as e:
        print(f"❌ Failed to connect to embedding model: {e}")
        print("Download embedding model: ollama pull nomic-embed-text")
        return False

if __name__ == "__main__":
    print("Testing Ollama connection...")
    test_ollama_connection()
    print("\nTesting embedding model...")
    test_embedding()