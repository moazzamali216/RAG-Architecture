from src.injestion import InjestionPipeLine
from src.retrieval import RetrievalPipeline

pdf = "./pdf/test.pdf"

# Ingest PDF first
print("📄 Ingesting PDF...")
InjestionPipeLine(pdf)
print("✅ PDF ingested!")
print("=" * 60)

# Test single query
print("\n🔍 Testing with single query...")
answer = RetrievalPipeline("How many people died in 2026 war")
print(f"Answer: {answer}")
print("=" * 60)

# Chat loop
print("\n💬 RAG CHATBOT")
print("=" * 60)
print("Ask questions about your documents.")
print("Type 'stop' or 'exit' to quit.")
print("=" * 60)

while True:
    # Get user input
    query = input("\nYour question: ")
    
    # Check if user wants to exit
    if query.lower() in ['stop', 'exit', 'quit', 'q']:
        print("\n👋 Goodbye!")
        break
    
    # Skip empty questions
    if query.strip() == "":
        print("⚠️ Please enter a question.")
        continue
    
    # Get answer
    print("\n🔍 Searching...")
    answer = RetrievalPipeline(query)
    print(f"\n✅ Answer: {answer}")
    print("-" * 60)