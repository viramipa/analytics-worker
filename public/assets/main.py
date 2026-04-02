import os
import logging
import time
import json
import redis
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
ANALYTICS_ENDPOINT = os.environ.get('ANALYTICS_ENDPOINT', 'http://localhost:8000/analytics')
RETRY_DELAY = int(os.environ.get('RETRY_DELAY', 5))
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'analytics_queue')

# Initialize Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def process_message(message):
    """
    Processes a single message from the queue.
    """
    try:
        data = json.loads(message)

        # Add timestamp
        data['processed_at'] = datetime.utcnow().isoformat()

        # Send data to analytics endpoint
        send_to_analytics(data)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")


def send_to_analytics(data):
    """
    Sends data to the analytics endpoint with retry logic.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(ANALYTICS_ENDPOINT, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            logging.info(f"Successfully sent data to analytics endpoint. Status code: {response.status_code}")
            return
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending data to analytics endpoint: {e}")
            retries += 1
            time.sleep(RETRY_DELAY)

    logging.error(f"Failed to send data to analytics endpoint after {MAX_RETRIES} retries.")


def main():
    """
    Main function to poll the Redis queue and process messages.
    """
    logging.info("Starting analytics worker...")
    while True:
        try:
            # BLPOP blocks until an item is available
            item = redis_client.blpop(QUEUE_NAME, timeout=1) # timeout to avoid blocking indefinitely on shutdown

            if item:
                queue_name, message = item
                process_message(message)
            else:
                # No message received within timeout.  Just continue the loop.
                pass

        except redis.exceptions.RedisError as e:
            logging.error(f"Redis error: {e}")
            time.sleep(RETRY_DELAY) # Avoid tight loop on redis connection errors
        except KeyboardInterrupt:
            logging.info("Stopping analytics worker...")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(RETRY_DELAY) # Avoid tight loop on errors


if __name__ == "__main__":
    main()