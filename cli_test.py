import ollama
from document_loader import load_document

print("=" * 60)
print("RAG智能问答系统 - 命令行版本")
print("=" * 60)

print("\n【1】加载知识库")
content = load_document('docs/sample_nlp_intro.txt')
print(f"已加载文档: sample_nlp_intro.txt")
print(f"文档长度: {len(content)} 字符")

print("\n【2】文档预览:")
print(content[:300] + "...")

def find_relevant_text(query, content, top_k=2):
    results = []
    query_lower = query.lower()
    paragraphs = content.split('\n\n')
    
    for i, para in enumerate(paragraphs):
        if len(para) < 50:
            continue
        score = sum(1 for word in query_lower.split() if word in para.lower())
        if score > 0:
            results.append({
                'content': para[:200],
                'score': score
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def generate_answer(query, content):
    relevant = find_relevant_text(query, content)
    
    if not relevant:
        return "文档中未找到相关答案"
    
    context = "\n".join([f"参考内容{i+1}:\n{r['content']}..." for i, r in enumerate(relevant)])
    
    prompt = f"""基于以下参考文档回答问题：

参考文档：
{context}

问题：{query}

请严格基于提供的参考文档回答，不要编造信息。如果文档中没有相关信息，请明确说"文档中未找到相关答案"。

回答："""
    
    response = ollama.chat(model='qwen2:0.5b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

print("\n" + "=" * 60)
print("开始问答（输入 'exit' 退出）")
print("=" * 60)

while True:
    question = input("\n请输入问题: ")
    if question.lower() == 'exit':
        break
    
    print("思考中...")
    answer = generate_answer(question, content)
    print(f"\n回答:\n{answer}")

print("\n✅ 测试完成！")