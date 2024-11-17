import requests
from requests.exceptions import RequestException

def fetch_from_llama(prompt, model="koesn/dolphin-llama3-8b", num_ctx=8192):
    """
    Fetch suggestions from the local Llama model using the provided API.
    
    Parameters:
    - prompt (str): The prompt to send to the Llama model.
    - model (str): The name of the Llama model.
    - num_ctx (int): The context length for generating responses.

    Returns:
    - list: A list of strings containing suggestions.
    """
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "num_ctx": num_ctx
            },
            stream=True
        )
        response.raise_for_status()
        return response.json().get("text", "").split(",")
    except RequestException as e:
        return [f"Error: Unable to fetch suggestions. Details: {e}"]

