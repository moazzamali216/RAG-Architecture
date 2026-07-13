# 📚 PDF RAG Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot that lets you ask questions about the contents of a PDF file. It ingests a PDF, splits it into chunks, embeds those chunks, stores them in a local vector database, and then answers questions using a local LLM grounded in the retrieved context.

## ✨ Features

- 📄 **PDF ingestion** — extracts text from a PDF and splits it into overlapping chunks
- 🧠 **Local embeddings** — uses Ollama's `nomic-embed-text` model to embed chunks
- 🗄️ **Vector storage** — persists embeddings in a local ChromaDB database
- 🔍 **Semantic search** — retrieves the most relevant chunks for a given question
- 💬 **Local LLM answers** — uses Ollama's `tinyllama` model to answer questions grounded only in retrieved context
- 🖥️ **Interactive CLI chat loop** — ask multiple questions in a single session

## 🧱 Project Structure

```
.
├── main.py                  # Entry point: ingests PDF, runs chat loop
├── src/
│   ├── injestion.py          # PDF loading, chunking, embedding, storage pipeline
│   └── retrieval.py          # Semantic search + LLM answer generation
├── pdf/
│   └── test.pdf              # Example PDF to ingest
└── chroma_langchain_db/       # Auto-created local ChromaDB persistence folder
```

> Note: the module is named `injestion` (not `ingestion`) — this matches the actual file/import names in the codebase, so keep the spelling consistent if you rename anything.

## ⚙️ Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally
- The following Ollama models pulled locally:
  ```bash
  ollama pull nomic-embed-text
  ollama pull tinyllama
  ```

### Python Dependencies

```bash
pip install chromadb ollama langchain-community langchain-text-splitters pypdf
```

> `PyPDFLoader` (from `langchain_community.document_loaders`) requires the `pypdf` package to read PDF files.

## 🚀 Usage

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Place your PDF** in the `pdf/` folder (or update the path in `main.py`):
   ```python
   pdf = "./pdf/test.pdf"
   ```

3. **Run the chatbot**:
   ```bash
   python main.py
   ```

4. The script will:
   - Ingest the PDF and store its embeddings in ChromaDB
   - Run one sample query automatically
   - Drop you into an interactive chat loop where you can ask more questions

5. **Exit the chat** by typing `stop`, `exit`, `quit`, or `q`.

### Example Session

```
📄 Ingesting PDF...
✅ PDF ingested!
============================================================

🔍 Testing with single query...
Answer: ...

============================================================

💬 RAG CHATBOT
============================================================
Ask questions about your documents.
Type 'stop' or 'exit' to quit.
============================================================

Your question: What is this document about?

🔍 Searching...

✅ Answer: ...
------------------------------------------------------------
```

## 🔧 How It Works

### Ingestion (`src/injestion.py`)

| Step | Function | Description |
|------|----------|-------------|
| 1 | `readPDF` | Loads the PDF using `PyPDFLoader` |
| 2 | `Charactersplit_Chunking` | Splits combined text into 500-character chunks with 10-character overlap using `RecursiveCharacterTextSplitter` |
| 3 | `Chunk_Embeddings` | Embeds each chunk using Ollama's `nomic-embed-text` model |
| 4 | `storetoChroma` | Stores chunks + embeddings in a persistent ChromaDB collection (`pdf_collection`) |
| — | `InjestionPipeLine` | Orchestrates the full ingestion flow |

### Retrieval (`src/retrieval.py`)

| Step | Function | Description |
|------|----------|-------------|
| 1 | `QuerySemanticSearch` | Embeds the question and retrieves the top 2 most similar chunks from ChromaDB |
| 2 | `ConcatenatewithQuery` | Builds a context-aware prompt and sends it to Ollama's `tinyllama` chat model |
| — | `RetrievalPipeline` | Orchestrates the full retrieval + answer flow |

## ⚠️ Known Limitations

- **Re-ingestion on every run**: `main.py` calls `InjestionPipeLine` every time it runs, which will re-add the same chunks to the collection (IDs are re-used as `0, 1, 2, ...`, so duplicates may be overwritten, but re-embedding is still wasted work on unchanged PDFs). Consider checking whether the collection is already populated before re-ingesting.
- **Small model, small context**: `tinyllama` is a lightweight model and may produce weaker answers than larger LLMs, especially on nuanced questions.
- **Fixed retrieval size**: only the top 2 chunks (`n_results=2`) are retrieved per query — increase this for documents where answers may span more context.
- **No answer citation/source tracking**: answers don't currently indicate which chunk(s) they were derived from.

## 🛠️ Possible Improvements

- Skip re-ingestion if the ChromaDB collection already contains data for a given PDF
- Make chunk size, overlap, model names, and `n_results` configurable (e.g. via CLI args or a config file)
- Add source citations to answers
- Swap `tinyllama` for a larger local model (e.g. `llama3`) for better answer quality
- Add support for ingesting multiple PDFs at once

## 📄 License

Add your preferred license here (e.g. MIT).
