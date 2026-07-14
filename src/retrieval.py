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
        n_results=4,
        include=["documents"]
    )
    
    return result["documents"][0]

def ConcatenatewithQuery(question):
    docs = QuerySemanticSearch(question)
    context = "\n\n".join(docs)
    
    response = ollama.chat(
        model="llama3.2:3b", 
        messages=[
            {"role": "system", "content": "Answer the question directly and concisely using only the information in the Context. Do not mention whether the question or context contains specific terms. If the answer is not present in the Context, respond only with: 'I don't know based on the given information.'"},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
    )
    
    return response["message"]["content"]

def RetrievalPipeline(question):
    return ConcatenatewithQuery(question)

