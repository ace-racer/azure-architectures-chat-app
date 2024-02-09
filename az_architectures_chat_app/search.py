import pandas as pd
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
from typing import List


class ChromaIndexSearch:
    def __init__(self, **kwargs) -> None:
        self.retriever_score_field_name = "cosine_distance"
        self.DEFAULT_EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=kwargs.get("model_name")
            if kwargs.get("model_name")
            else self.DEFAULT_EMBEDDINGS_MODEL,
            device=kwargs.get("device") if kwargs.get("device") else "cpu",
        )

    def execute(
        self,
        chroma_index_path: str,
        chroma_collection_name: str,
        query: str,
        top_k: int,
        additional_metadata_fields: List[str],
        **kwargs,
    ) -> pd.DataFrame:
        print("Start ChromaIndexSearch")
        self.chroma_client = chromadb.PersistentClient(path=chroma_index_path)
        self.chroma_collection = self.chroma_client.get_collection(
            name=chroma_collection_name, embedding_function=self.embedding_function
        )
        print(f"Num elements in Chroma collection: {self.chroma_collection.count()}")
        query_texts = [query]
        docs = self.chroma_collection.query(query_texts=query_texts, n_results=top_k)
        results = {}
        # print(f"results: {docs}")

        results["ids"] = docs["ids"][0]
        results["distances"] = docs["distances"][0]
        results["content"] = docs["documents"][0]
        metadatas = docs["metadatas"][0]
        results["chunk_numbers"] = [x["chunk_number"] for x in metadatas]
        for m in additional_metadata_fields:
            results[m] = [x[m] for x in metadatas]

        results_df = pd.DataFrame.from_dict(results)

        print("Finished ChromaIndexSearch")
        return results_df
