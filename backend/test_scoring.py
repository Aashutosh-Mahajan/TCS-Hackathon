import sys
import io
import asyncio
import json

# Ensure UTF-8 output encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.rag.embeddings import encode_passages, preload_model
from app.rag.bm25_index import BM25Index
from app.rag.vector_store import VectorStore
from app.agents.retriever_agent import init_retriever
from app.agents.graph import run_pipeline

def load_data():
    with open("app/data/rag_dataset.json", "r", encoding="utf-8") as f:
        return json.load(f)

async def test():
    print("--- Initializing RAG System ---")
    dataset = load_data()
    passages = [entry["passage"] for entry in dataset]
    preload_model()
    embeddings = encode_passages(passages)
    
    vs = VectorStore()
    metadata = [
        {
            "text": entry["passage"],
            "source": entry["metadata"]["source"],
            "language": entry["language"],
            "category": entry["category"],
        }
        for entry in dataset
    ]
    vs.add(embeddings, metadata)
    
    bm25 = BM25Index()
    bm25.build(passages)
    
    init_retriever(vs, bm25, dataset)
    print("--- System Ready! Running Test Cases ---\n")

    test_queries = [
        ("Supported English", "What is the annual leave policy?"),
        ("Contradicted Claim", "Is it true that employees get 60 days of paid annual leave?"),
        ("Hindi Cross-lingual", "वार्षिक छुट्टी नीति क्या है?"),
        ("Marathi Cross-lingual", "वार्षिक रजा धोरण काय आहे?"),
        ("No Evidence Query", "What is the policy for flying in a private jet?"),
    ]

    for label, query in test_queries:
        print(f"==================================================")
        print(f"TEST CASE: {label}")
        print(f"QUERY: '{query}'")
        res = await run_pipeline(query)
        print(f"DETECTED LANG  : {res.get('detected_language')}")
        print(f"ANSWER         : {res.get('answer')}")
        print(f"RETRIEVAL SCORE: {res.get('retrieval_score')}")
        print(f"GROUNDING LABEL: {res.get('grounding_label')}")
        print(f"GROUNDING REASON: {res.get('grounding_details')}")
        print(f"CONFIDENCE SCORE: {res.get('confidence_score')} -> TAG: {res.get('confidence_tag')}")
        print(f"EXPLANATION    : {res.get('explanation')}")
        if res.get('warning'):
            print(f"WARNING        : {res.get('warning')}")
        print(f"==================================================\n")

if __name__ == "__main__":
    asyncio.run(test())
