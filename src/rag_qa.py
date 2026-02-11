# src/rag_qa.py

from embedder import Embedder
from retriever import retrieve_documents
import ollama


def build_prompt(context_chunks, question):
    """
    Build a RAG prompt using retrieved context.
    """
    context_text = "\n\n".join(
        f"- {chunk['content']}" for chunk in context_chunks
    )

    prompt = f"""
You are an intelligent assistant.
Use ONLY the context below to answer the question.

Context:
{context_text}

Question:
{question}

Answer clearly and concisely.
"""
    return prompt


def answer_question(question: str, top_k: int = 3):
    """
    Run full RAG pipeline:
    - Embed question
    - Retrieve relevant documents
    - Generate answer using LLM
    """
    print("\n🔍 Processing question...\n")

    # 1. Embed the question
    embedder = Embedder()
    query_vector = embedder.embed_texts([question])[0]

    # 2. Retrieve relevant documents
    retrieved_docs = retrieve_documents(query_vector, top_k)

    if not retrieved_docs:
        return "No relevant documents found to answer the question."

    # 3. Build RAG prompt
    prompt = build_prompt(retrieved_docs, question)

    # 4. Query LLM (Ollama)
    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    print("📄 RAG Document Question Answering System")
    print("Type 'exit' to quit.\n")

    while True:
        user_question = input("❓ Ask a question: ").strip()

        if user_question.lower() in ("exit", "quit"):
            print("👋 Exiting. Goodbye!")
            break

        answer = answer_question(user_question)
        print("\n✅ Answer:\n")
        print(answer)
        print("\n" + "-" * 60)
