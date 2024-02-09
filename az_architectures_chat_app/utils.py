import os
from datetime import datetime
from configs import EXPORT_DIR
import pandas as pd
import tiktoken

EXPORT_FILE_EXTENSION = ".csv"

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR, exist_ok=False)


def get_export_file_path() -> str:
    # Get the current date and time
    now = datetime.now()

    # Format the date and time as "YYYYMMDD_HHMM"
    export_file_name = now.strftime("%Y%m%d_%H%M%S")

    return os.path.join(EXPORT_DIR, export_file_name + EXPORT_FILE_EXTENSION)


def export_current_conversation(current_conversation: list[dict]):
    export_file_path = get_export_file_path()
    df = pd.DataFrame(current_conversation)
    df.to_csv(export_file_path, index=False)
    print(f"Conversation exported successfully to {export_file_path}")


"""
Copied from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
"""


def num_tokens_from_messages(messages: list[dict], model: str) -> int:
    """Return the number of tokens used by a list of messages."""
    if not messages or len(messages) == 0:
        return 0
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
