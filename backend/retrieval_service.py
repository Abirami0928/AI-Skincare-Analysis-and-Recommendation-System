
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "chroma_db"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_collection(
    name="skincare_research"
)


def retrieve_research(question, top_k=5):

    # Convert question into embedding
    question_embedding = model.encode(
        question
    ).tolist()

    # Search relevant research chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):
        retrieved_documents.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return retrieved_documents


if __name__ == "__main__":

    question = "What ingredients help improve dry skin?"

    results = retrieve_research(question)

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Source:", result["source"])
        print("Distance:", result["distance"])
        print("Text:", result["text"][:500])
