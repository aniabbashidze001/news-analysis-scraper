"""
Utility helper functions for user-agent randomization, safe HTTP requests,
and configuration loading used across the scraping project.
"""

import random
import requests
import time
import yaml


def get_random_user_agent():
    """
        Returns a random user-agent string from a predefined list.

        Used to avoid detection by rotating headers in HTTP requests.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)",
        "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) Trident/7.0; rv:11.0",
        "Mozilla/5.0 (Linux; Android 10) Chrome/88.0.4324.93 Mobile Safari/537.36",
    ]
    return random.choice(user_agents)


def safe_request(url, headers=None, retries=3, timeout=5):
    """
        Sends an HTTP GET request with retry logic and error handling.

        Args:
            url (str): The target URL to request.
            headers (dict, optional): Optional HTTP headers to include.
            retries (int): Number of retry attempts on failure.
            timeout (int): Timeout duration for each request.

        Returns:
            requests.Response or None: The response object if successful, otherwise None.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
            else:
                print(f"⚠️ Status {response.status_code} on attempt {attempt}")
        except requests.RequestException as e:
            print(f"❌ Attempt {attempt} failed for {url}: {e}")
        time.sleep(2)
    return None


def load_config(path="config/settings.yaml"):
    """
        Loads YAML configuration settings from the specified file path.

        Args:
            path (str): Relative path to the YAML config file.

        Returns:
            dict: Parsed configuration as a dictionary.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)
