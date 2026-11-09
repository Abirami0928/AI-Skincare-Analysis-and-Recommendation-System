
from retrieval_service import retrieve_research
from gemini_service import generate_answer


def answer_question(question):
    # Step 1: Retrieve relevant research from ChromaDB
    retrieved_documents = retrieve_research(question, top_k=5)

    if not retrieved_documents:
        return {
            "response": "I couldn't find relevant information in the available skincare research documents.",
            "sources": []
        }

    # Step 2: Prepare research context for Gemini
    research_context = "\n\n".join(
        f"Source: {document['source']}\n"
        f"Research content:\n{document['text']}"
        for document in retrieved_documents
    )

    # Step 3: Generate an answer using Gemini
    answer = generate_answer(question, research_context)

    # Step 4: Collect unique source filenames
    sources = list(dict.fromkeys(
        document["source"] for document in retrieved_documents
    ))

    return {
        "response": answer,
        "sources": sources
    }


# if __name__ == "__main__":
#     question = "What ingredients help improve dry skin?"

#     result = answer_question(question)

#     print("\nSkinSense AI Answer:\n")
#     print(result["response"])

#     print("\nResearch Sources:")
#     for source in result["sources"]:
#         print("-", source)
