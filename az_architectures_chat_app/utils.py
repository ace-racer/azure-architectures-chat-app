import os
from datetime import datetime
from configs import EXPORT_DIR
import pandas as pd

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
