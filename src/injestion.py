from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import ollama  

def readPDF(pdfpath):
    pdf_path = Path(pdfpath)
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    return documents

def Charactersplit_Chunking(pdf_to_str):
    text = pdf_to_str
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def Chunk_Embeddings(preprocessed_chunks_string):
    embeddings = []
    for chunk in preprocessed_chunks_string:
        response = ollama.embeddings(  # <-- CHANGED
            model="nomic-embed-text",   # <-- CHANGED
            prompt=chunk
        )
        embeddings.append(response["embedding"])
    return embeddings

def storetoChroma(chunks, embeddings, source_name="test.pdf"):
    client = chromadb.PersistentClient(path="./chroma_langchain_db")
    collection = client.get_or_create_collection("pdf_collection")
    
    collection.add(
        ids=[f"{source_name}_{i}" for i in range(len(chunks))],  # e.g. "test.pdf_0", "test.pdf_1"
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source_name, "chunk_index": i} for i in range(len(chunks))]
    )
    return collection

def InjestionPipeLine(pathtopdf):
    documents = readPDF(pathtopdf)
    injestion_str = "\n".join(doc.page_content for doc in documents)
    preprocessed_chunks = Charactersplit_Chunking(injestion_str)
    embedded_chunks = Chunk_Embeddings(preprocessed_chunks)
    source_name = Path(pathtopdf).name
    chromadbvectors = storetoChroma(preprocessed_chunks, embedded_chunks,source_name)
    return chromadbvectors