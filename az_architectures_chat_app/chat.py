from typing import List, Dict
from openai import OpenAI
from template import JinjaPromptTemplate
import os
from pathlib import Path
from search import ChromaIndexSearch
from configs import DATA_DIR, ANSWER_GENERATION_TEMPERATURE, QUERY_MODEL

jinja_prompt_template = JinjaPromptTemplate()
chroma_search_client = ChromaIndexSearch(device="cuda")
prompts_dir = os.path.join(Path(__file__).parent, "prompts")
chroma_index_path = os.path.join(DATA_DIR, "chroma")

chroma_collection_name = "azure_architectures"
top_k = 5


def get_final_response(
    oai_client: OpenAI,
    answer_generation_model_name: str,
    messages: List[Dict[str, str]],
    stream: bool,
):
    search_prompt_template_path = os.path.join(prompts_dir, "search_query.jinja2")
    rag_prompt_template_path = os.path.join(prompts_dir, "rag.jinja2")
    user_query = (
        messages[-1]["content"]
        if messages[-1]["role"] == "user"
        else "Please provide a valid user query"
    )
    conversation_history = messages[:-1]
    print(f"user_query: {user_query}")
    print(f"conversation_history: {conversation_history}")
    search_query_prompt = jinja_prompt_template.execute(
        search_prompt_template_path,
        user_query=user_query,
        conversation_history=conversation_history,
    )
    print(f"search_query_prompt: {search_query_prompt}")
    search_query_messages = [{"role": "user", "content": search_query_prompt}]
    search_query_completion = oai_client.chat.completions.create(
        model=QUERY_MODEL, messages=search_query_messages, temperature=0, stream=False
    )
    search_query = search_query_completion.choices[0].message.content
    if search_query == "0":
        print("ERROR: Search query could not be generated for the conversation...")
        return None

    print(f"generated search_query: {search_query}")
    results_df = chroma_search_client.execute(
        chroma_index_path,
        chroma_collection_name,
        search_query,
        top_k=top_k,
        additional_metadata_fields=["url", "title"],
    )
    results_df = results_df[["url", "title", "content"]]
    relevant_contexts = results_df.to_dict(orient="records")
    print(f"len(relevant_contexts): {len(relevant_contexts)}")

    rag_prompt = jinja_prompt_template.execute(
        rag_prompt_template_path,
        user_query=user_query,
        conversation_history=conversation_history,
        relevant_contexts=relevant_contexts,
    )
    print(f"rag_prompt: {rag_prompt}")
    rag_messages = [{"role": "user", "content": rag_prompt}]
    rag_completion = oai_client.chat.completions.create(
        model=answer_generation_model_name,
        messages=rag_messages,
        temperature=ANSWER_GENERATION_TEMPERATURE,
        stream=stream,
    )
    return rag_completion
