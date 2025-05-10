import os
import json

# Configuration file path
CONFIG_PATH = os.path.expanduser("~/.ani-sync/config.json")
TOKEN_PATH = os.path.expanduser("~/.ani-sync/token")

# Default configuration
DEFAULT_CONFIG = {
    "server_url": "https://services-anisync.hamzie.net",
}

def init_config():
    """
    Ensure the configuration directory and file exist.
    """
    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)

def load_config():
    """
    Load the configuration from the config file.
    Returns:
        dict: The configuration dictionary.
    """
    init_config()
    with open(CONFIG_PATH, "r") as config_file:
        return json.load(config_file)

def save_config(config):
    """
    Save the configuration to the config file.
    Args:
        config (dict): The configuration dictionary to save.
    """
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config, config_file, indent=4)

def save_token(token):
    """
    Save the user's token securely.
    Args:
        token (str): The token string.
    """
    with open(TOKEN_PATH, "w") as token_file:
        token_file.write(token)

def load_token():
    """
    Load the user's token.
    Returns:
        str: The token string, or None if not found.
    """
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as token_file:
            return token_file.read().strip()
    return None


def clear_token():
    """
    Clear the stored token.
    """
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)
