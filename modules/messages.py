# **********************************************
# ---------------- 98 SOFTWARES ----------------
# -------------- MESSAGES MODULE ---------------
# **********************************************

import os

# Function to load messages
def load_messages(messages_directory:str) -> dict:
    # Check if messages directory is empty, in that case return an empty dict
    if len(os.listdir(messages_directory)) == 0: return {}

    # Load messages
    msg_dict = {}
    for messages_file in os.listdir(messages_directory):
        msg_dict[messages_file.replace(".txt", "")] = {}

        with open(os.path.join(messages_directory, messages_file), "r", encoding="utf-8") as f:
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
