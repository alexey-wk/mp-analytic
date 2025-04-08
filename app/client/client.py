import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

def get_client_with_retries():
    client = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=2,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    client.mount("https://", adapter)

    return client

def get_auth_headers(api_token: str):
    return {
        'Authorization': f'Bearer {api_token}'
    }