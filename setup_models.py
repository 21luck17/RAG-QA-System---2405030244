import ollama
import sys
import time

def check_and_pull_model(model_name):
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models['models']]
        print(f"已安装的模型: {model_names}")
        
        if model_name in model_names:
            print(f"✅ 模型 {model_name} 已存在")
            return True
        else:
            print(f"⬇️  正在下载模型 {model_name} (请耐心等待)...")
            try:
                result = ollama.pull(model_name)
                if result.get('status') == 'success':
                    print(f"✅ 模型 {model_name} 下载完成")
                    return True
                else:
                    print(f"❌ 下载模型 {model_name} 失败: {result}")
                    return False
            except Exception as e:
                print(f"❌ 下载模型 {model_name} 失败: {e}")
                return False
    except Exception as e:
        print(f"❌ 连接Ollama失败: {e}")
        print("请确保Ollama已安装并正在运行")
        print("下载Ollama: https://ollama.com/download")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("检查Ollama环境")
    print("=" * 50)
    
    # 检查大语言模型
    llm_model = "qwen2:0.5b"
    print(f"\n【1/2】检查大语言模型: {llm_model}")
    llm_ok = check_and_pull_model(llm_model)
    
    # 检查嵌入模型
    embed_model = "nomic-embed-text"
    print(f"\n【2/2】检查嵌入模型: {embed_model}")
    embed_ok = check_and_pull_model(embed_model)
    
    print("\n" + "=" * 50)
    if llm_ok and embed_ok:
        print("✅ 所有模型准备就绪！")
        sys.exit(0)
    else:
        print("❌ 部分模型未准备好，请检查网络连接后重试")
        sys.exit(1)