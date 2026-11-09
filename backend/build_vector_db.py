
from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_FILE = BASE_DIR / "research_chunks" / "chunks.json"
DB_DIR = BASE_DIR / "chroma_db"

# Load research chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Total chunks loaded:", len(chunks))

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB database
client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="skincare_research",
    metadata={"hnsw:space": "cosine"}
)

# Prepare data
ids = [f"chunk_{i}" for i in range(len(chunks))]
documents = [chunk["text"] for chunk in chunks]
metadatas = [
    {
        "source": chunk["source"],
        "chunk_id": chunk["chunk_id"]
    }
    for chunk in chunks
]

# Generate and store embeddings in batches
BATCH_SIZE = 100

for start in range(0, len(chunks), BATCH_SIZE):
    end = start + BATCH_SIZE

    batch_ids = ids[start:end]
    batch_documents = documents[start:end]
    batch_metadatas = metadatas[start:end]

    embeddings = model.encode(
        batch_documents,
        show_progress_bar=False
    ).tolist()

    collection.upsert(
        ids=batch_ids,
        documents=batch_documents,
        metadatas=batch_metadatas,
        embeddings=embeddings
    )

    print(f"Processed {min(end, len(chunks))}/{len(chunks)} chunks")

print("\nEmbedding generation completed!")
print("Total vectors stored:", collection.count())
print("Database location:", DB_DIR)
