# **********************************************
# ---------------- 98 SOFTWARES ----------------
# -------------- MESSAGES MODULE ---------------
# **********************************************

import os

# Session import
from modules.session import session

# Constants import
from modules.constants import MESSAGES_DIRECTORY

# Function to load messages
def load_messages() -> dict:
    # Check if messages directory is empty, in that case return an empty dict
    if len(os.listdir(MESSAGES_DIRECTORY)) == 0: return {}

    # Load messages
    messages_language_directory = os.path.join(MESSAGES_DIRECTORY, session.get("settings")["language"])
    msg_dict = {}
    for messages_file in os.listdir(messages_language_directory):
        msg_dict[messages_file.replace(".txt", "")] = {}

        with open(os.path.join(messages_language_directory, messages_file), "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"): continue # Skip comments
                if line.strip() == "": continue # Skip empty lines

                # Split line into 2 parts list
                try:
                    line_list = line.split(":", 1)
                    msg_dict[messages_file.replace(".txt", "")][line_list[0].strip()] = line_list[1].strip()
                except Exception as e:
                    print(f"Error on reading file: {messages_file} - {e}")

    return msg_dict

# Function to import style
def import_style(filename:str, styles_directory:str) -> str:
    # Add .txt if is not present in filename add it to filename string
    if ".txt" not in filename: filename = f"{filename}.txt"

    file_path = os.path.join(styles_directory, filename)

    # Check if file exists, if not return an empty string
    if not os.path.exists(file_path): return ""

    # Load style
    with open(file_path, "r") as f:
        file_content = f.read().strip()

    return file_content
