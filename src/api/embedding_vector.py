from langchain_ollama import OllamaEmbeddings


OlamaEmbedding = OllamaEmbeddings(
    model= "nomic-embed-text", 
    base_url="http://localhost:11434"
            )
