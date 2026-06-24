import ollama
import sys
import time

def pull_model(model_name):
    print(f"开始下载 {model_name}...")
    sys.stdout.flush()
    try:
        result = ollama.pull(model_name)
        print(f"{model_name} 下载结果: {result}")
        return True
    except Exception as e:
        print(f"{model_name} 下载失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("开始下载模型")
    print("=" * 50)
    sys.stdout.flush()
    
    success = True
    
    # 下载大语言模型
    if not pull_model("qwen2:0.5b"):
        success = False
    
    # 下载嵌入模型
    if not pull_model("nomic-embed-text"):
        success = False
    
    if success:
        print("\n✅ 所有模型下载完成！")
    else:
        print("\n❌ 部分模型下载失败")
        sys.exit(1)