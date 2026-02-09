import os
from pathlib import Path

from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData

# Load environment variables 
ENV_PATH = Path(__file__).resolve().parent.parent / "config" / ".env"
if not ENV_PATH.exists():
    raise FileNotFoundError(f".env not found at: {ENV_PATH}")
load_dotenv(ENV_PATH)

CONNECTION_STRING = os.getenv("EVENT_HUB_CONN_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

def test_connection():
    """Test if we can connect to Azure Event Hubs"""
    try:
        print("🔄 Testing connection to Azure Event Hubs...")
        print(f"Event Hub: {EVENT_HUB_NAME}")
        
        # Create producer client
        producer = EventHubProducerClient.from_connection_string(
            conn_str=CONNECTION_STRING,
            eventhub_name=EVENT_HUB_NAME
        )
        
        # Send a test event
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData('{"test": "Hello from Python!"}'))
        
        producer.send_batch(event_data_batch)
        producer.close()
        
        print("✅ SUCCESS! Connection working!")
        print("✅ Test message sent to Event Hub!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nCheck:")
        print("1. Is your .env file in config/ folder?")
        print("2. Did you copy the full connection string?")
        print("3. Is Event Hub name correct?")

if __name__ == "__main__":
    test_connection()
