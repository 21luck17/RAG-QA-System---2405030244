import ollama

def test_ollama_connection():
    try:
        response = ollama.chat(model='deepseek-r1:7b', messages=[
            {'role': 'user', 'content': 'Hello, how are you?'}
        ])
        print("✅ Ollama API connection successful!")
        print("Response:", response['message']['content'])
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print("Please make sure Ollama is installed and running, and the model is downloaded.")
        print("Install Ollama: https://ollama.com/download")
        print("Download model: ollama pull deepseek-r1:7b")
        return False

if __name__ == "__main__":
    test_ollama_connection()