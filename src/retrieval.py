import chromadb
import ollama

db = chromadb.PersistentClient(path="./chroma_langchain_db")
collection = db.get_or_create_collection("pdf_collection")

def QuerySemanticSearch(question):
    embedding = ollama.embeddings(
        model="nomic-embed-text", 
        prompt=question
    )["embedding"]
    
    result = collection.query(
        query_embeddings=[embedding],
        n_results=2,
        include=["documents"]
    )
    
    return result["documents"][0]

def ConcatenatewithQuery(question):
    docs = QuerySemanticSearch(question)
    context = "\n\n".join(docs)
    
    response = ollama.chat(
        model="tinyllama",  # <-- CHANGED from tinyllama (better)
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer based only on the context provided."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
    )
    
    return response["message"]["content"]

def RetrievalPipeline(question):
    return ConcatenatewithQuery(question)

