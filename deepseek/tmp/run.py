import requests
import json
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_model():
    """
    Test deployed DeepSeek model
    """

    URL = "http://localhost:8000/generate"
    headers = {"Content-Type": "application/json"}

    data = {"prompt": "The drought had lasted now for ten million years, and the reign of the terrible lizards had long since ended.",
            "max_tokens": 100,
            "temperature": 0.5,
            }

    
    logger.info(f"Sending request to {URL}")


    
    try:
        response = requests.post(URL,
                                 headers=headers,
                                 data=json.dumps(data))
        
        response.raise_for_status()  # Raise an exception for bad status codes
        logger.info("Request successful")
        result = response.json()
        logger.info(f"Response received: {result}")
        print(result)

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise

    
    print(response.json())

if __name__ == "__main__":
    test_model()