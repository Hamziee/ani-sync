import requests

class SyncClient:
    """
    A client for synchronizing progress with a remote server.
    """
    def __init__(self, server_url, user_id):
        self.server_url = server_url
        self.user_id = user_id

    def sync_progress(self, progress):
        """
        Sync the given progress data to the server.
        
        Args:
            progress (list): A list of progress dictionaries.
        """
        response = requests.post(f"{self.server_url}/api/sync", json={
            "user_id": self.user_id,
            "progress": progress
        })
        if response.status_code == 200:
            print("Sync successful!")
        else:
            print(f"Sync failed: {response.status_code} - {response.text}")

    def fetch_progress(self):
        """
        Fetch progress data from the server.
        
        Returns:
            list: A list of progress dictionaries.
        """
        response = requests.get(f"{self.server_url}/api/progress/{self.user_id}")
        if response.status_code == 200:
            return response.json().get("progress", [])
        else:
            print(f"Failed to fetch progress: {response.status_code} - {response.text}")
            return []
