import os

def parse_hsts(file_path):
    """
    Parse the ani-hsts file to extract viewing progress.
    
    Args:
        file_path (str): Path to the ani-hsts file.
        
    Returns:
        list: A list of dictionaries containing progress data.
    """
    progress = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"History file not found: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            watched_episodes, unique_id, title_info = parts
            title, _, total_episodes = title_info.rpartition("(")
            total_episodes = total_episodes.rstrip(" episodes)")
            progress.append({
                "watched_episodes": int(watched_episodes),
                "unique_id": unique_id,
                "title": title.strip(),
                "total_episodes": int(total_episodes)
            })
    return progress
