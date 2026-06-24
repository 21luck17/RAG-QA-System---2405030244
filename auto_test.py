import ollama
from document_loader import load_document

print("=" * 60)
print("RAG智能问答系统 - 自动测试")
print("=" * 60)

print("\n【1】加载知识库")
content = load_document('docs/sample_nlp_intro.txt')
print(f"已加载文档: sample_nlp_intro.txt")
print(f"文档长度: {len(content)} 字符")

def find_relevant_text(query, content, top_k=2):
    results = []
    query_lower = query.lower()
    query_words = query_lower.split()
    
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        current_section += line + " "
        
        if len(current_section) > 100:
            score = 0
            for word in query_words:
                if word in current_section.lower():
                    score += 1
            
            if score > 0:
                results.append({
                    'content': current_section.strip()[:250],
                    'score': score
                })
            current_section = ""
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def generate_answer(query, content):
    relevant = find_relevant_text(query, content)
    
    if not relevant:
        context = content[:500]
    else:
        context = "\n".join([f"参考内容{i+1}:\n{r['content']}" for i, r in enumerate(relevant)])
    
    prompt = f"""基于以下参考文档回答问题：

参考文档：
{context}

问题：{query}

请严格基于提供的参考文档回答，不要编造信息。

回答："""
    
    response = ollama.chat(model='qwen2:0.5b', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

test_questions = [
    "什么是自然语言处理？",
    "NLP的主要任务有哪些？",
    "今天天气怎么样？"
]

print("\n" + "=" * 60)
print("测试问答")
print("=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n【问题{i}】{question}")
    print("思考中...")
    answer = generate_answer(question, content)
    print(f"【回答】{answer}")
    print("-" * 40)

print("\n✅ 所有测试完成！")