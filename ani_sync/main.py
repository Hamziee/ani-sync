import argparse
import subprocess
import sys
import os
import shutil
import requests
from ani_sync.config import load_config, save_config, load_token, save_token, clear_token


def get_hsts_file_path(custom_path=None):
    """
    Get the full path to the ani-hsts file.
    Args:
        custom_path (str): Optional custom path for the ani-hsts file.
    Returns:
        str: Full path to the ani-hsts file.
    """
    if custom_path:
        return custom_path
    # Default location for the ani-hsts file
    return os.path.expanduser("~/.local/state/ani-cli/ani-hsts")


def validate_server_url(url):
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
    return url


def register():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config = load_config()
    server_url = validate_server_url(config["server_url"])

    response = requests.post(f"{server_url}/register", json={"email": email, "password": password})
    if response.status_code == 201:
        print("Registration successful. You can now log in.")
    else:
        print("Registration failed:", response.json().get("error"))


def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    config = load_config()
    server_url = validate_server_url(config["server_url"])

    response = requests.post(f"{server_url}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        token = response.json().get("token")
        save_token(token)
        print("Login successful. Token saved.")
    else:
        print("Login failed:", response.json().get("error"))


def fetch_progress():
    token = load_token()
    if not token:
        print("Error: You need to log in first. Use `ani-sync --- --login`.")
        return None

    config = load_config()
    server_url = validate_server_url(config["server_url"])
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{server_url}/progress", headers=headers)

    if response.status_code == 200:
        return response.json().get("progress", [])
    elif response.status_code == 401:
        print("Error: Invalid or expired token.")
        clear_token()
        return None
    else:
        print(f"Error fetching progress: {response.text}")
        return None


def update_progress(file_path):
    file_path = get_hsts_file_path(file_path)
    if not os.path.exists(file_path):
        print(f"Error: Local file {file_path} not found. Cannot upload progress.")
        return

    token = load_token()
    if not token:
        print("Error: You need to log in first. Use `ani-sync --- --login`.")
        return

    config = load_config()
    server_url = validate_server_url(config["server_url"])
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with open(file_path, "rb") as file:
            response = requests.post(f"{server_url}/progress/upload", headers=headers, files={"file": file})
        if response.status_code == 200:
            print("Progress file uploaded successfully.")
        elif response.status_code == 401:
            print("Error: Invalid or expired token.")
            clear_token()
        else:
            print(f"Error uploading progress file: {response.text}")
    except Exception as e:
        print(f"Error: Failed to upload progress file. {e}")


def download_progress(file_path=None):
    """
    Download progress from the server and write it to the local ani-hsts file.
    """
    file_path = get_hsts_file_path(file_path)

    print("Fetching progress from the server...")
    server_progress = fetch_progress()

    if server_progress is None:
        print("Error: Unable to fetch progress from the server.")
        sys.exit(1)

    if not server_progress:
        print("No progress data available on the server. Creating an empty ani-hsts file.")
        with open(file_path, "w") as file:
            pass
        return

    print("Server progress fetched. Writing to the local ani-hsts file...")
    with open(file_path, "w") as file:
        for item in server_progress:
            # Write progress data to the file in tab-separated format
            file.write(f"{item['progress']}\t{item['anime_id']}\t{item['title']}\n")
    print(f"Progress downloaded and saved to {file_path}.")


def run_ani_cli(cli_args):
    if os.name == "nt":  # Windows
        git_bash_path = shutil.which("bash")
        if not git_bash_path:
            print("Error: Git Bash is required to run ani-cli on Windows.")
            return
        command = [git_bash_path, "-c", f"ani-cli {' '.join(cli_args)}"]
    else:
        command = ["ani-cli"] + cli_args

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: ani-cli command not found. Ensure ani-cli is in your PATH.")


def sync_before_ani_cli(file_path=None):
    """
    Sync progress with the server before running ani-cli.
    Downloads progress from the server and updates the local file.
    """
    file_path = get_hsts_file_path(file_path)

    print("Fetching progress from the server...")
    server_progress = fetch_progress()

    if server_progress is None:
        print("Error: Sync failed. Cannot connect to the server.")
        sys.exit(1)

    if not server_progress:
        print("No progress data available on the server. Keeping local progress unchanged.")
        return

    print("Server progress fetched. Writing to the local ani-hsts file...")
    with open(file_path, "w") as file:
        for item in server_progress:
            file.write(f"{item['progress']}\t{item['anime_id']}\t{item['title']} (unknown episodes)\n")
    print(f"Updated {file_path} with progress fetched from the server.")


def main():
    if "---" in sys.argv:
        sync_args = sys.argv[sys.argv.index("---") + 1:]
        cli_args = sys.argv[1:sys.argv.index("---")]
    else:
        cli_args = sys.argv[1:]
        sync_args = []

    config = load_config()

    parser = argparse.ArgumentParser(description="Sync ani-cli progress with a remote server.")
    parser.add_argument("--register", action="store_true", help="Register a new account.")
    parser.add_argument("--login", action="store_true", help="Log in to get a token.")
    parser.add_argument("--upload", action="store_true", help="Upload local progress to the server.")
    parser.add_argument("--download", action="store_true", help="Download progress from the server and update local file.")
    parser.add_argument("--file", type=str, help="Path to the ani-hsts file.")
    parser.add_argument("--server", type=str, help="Specify a custom server URL.")
    parser.add_argument("--logout", action="store_true", help="Log out and clear the token.")

    args = parser.parse_args(sync_args)

    if args.server:
        config["server_url"] = validate_server_url(args.server)
        save_config(config)
        print(f"Server URL updated to: {config['server_url']}")
        return

    if args.register:
        register()
        return

    if args.login:
        login()
        return

    if args.logout:
        clear_token()
        print("Logged out successfully.")
        return

    if args.upload:
        print("Uploading local progress to the server...")
        update_progress(args.file)
        print("Upload completed.")
        return

    if args.download:
        print("Downloading progress from the server...")
        download_progress(args.file)
        print("Download completed.")
        return

    # Normal execution: run ani-cli
    sync_before_ani_cli(args.file)
    print("Starting ani-cli...")
    run_ani_cli(cli_args)
    print("ani-cli exited. Updating progress to the server...")
    update_progress(args.file)
