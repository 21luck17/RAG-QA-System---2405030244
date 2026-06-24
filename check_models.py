import ollama

try:
    models = ollama.list()
    model_names = [m['name'] for m in models['models']]
    print("已安装模型:", model_names)
    
    has_qwen = any('qwen2' in m for m in model_names)
    has_embed = any('nomic-embed-text' in m for m in model_names) or any('bge' in m for m in model_names) or any('mxbai' in m for m in model_names)
    
    print("\n检查结果:")
    print(f"  大语言模型(qwen2:0.5b): {'✅' if has_qwen else '❌'}")
    print(f"  嵌入模型: {'✅' if has_embed else '❌'}")
    
    if has_qwen and has_embed:
        print("\n✅ 所有模型已准备就绪！")
    else:
        print("\n❌ 部分模型未找到")
        
except Exception as e:
    print(f"错误: {e}")