from typing import List, Dict
from openai import OpenAI
from template import JinjaPromptTemplate
import os
from pathlib import Path


jinja_prompt_template = JinjaPromptTemplate()
prompts_dir = os.path.join(Path(__file__).parent, "prompts")


def get_final_response(
    oai_client: OpenAI, model_name: str, messages: List[Dict[str, str]], stream: bool
):
    prompt_template_path = os.path.join(prompts_dir, "search_query.jinja2")
    user_query = (
        messages[-1]["content"]
        if messages[-1]["role"] == "user"
        else "Please provide a valid user query"
    )
    conversation_history = messages[:-1]
    print(f"user_query: {user_query}")
    print(f"conversation_history: {conversation_history}")
    search_query_prompt = jinja_prompt_template.execute(
        prompt_template_path, user_query=user_query, conversation_history=conversation_history
    )
    print(f"search_query_prompt: {search_query_prompt}")
    search_query_messages = [{"role": "user", "content": search_query_prompt}]
    search_query = oai_client.chat.completions.create(
        model=model_name, messages=search_query_messages, temperature=0, stream=stream
    )

    print(f"search_query: {search_query}")
    return search_query
