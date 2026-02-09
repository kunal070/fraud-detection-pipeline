import asyncio
import json
import os
import pandas as pd
from dotenv import load_dotenv
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

# Load config
load_dotenv('config/.env')
CONNECTION_STRING = os.getenv('EVENT_HUB_CONN_STR')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')
DATASET_PATH = 'data/creditcard.csv'
SPEED_FACTOR = 1000  # 1000x faster than real-time

class AzureFraudSimulator:
    def __init__(self, filepath, conn_str, hub_name, speed_factor):
        self.filepath = filepath
        self.conn_str = conn_str
        self.hub_name = hub_name
        self.speed_factor = speed_factor
        self.producer = None
        self.df = None
        
    def load_data(self):
        """Load and prepare dataset"""
        print(f"📂 Loading dataset from {self.filepath}...")
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Dataset not found at {self.filepath}")
            
        self.df = pd.read_csv(self.filepath)
        self.df = self.df.sort_values(by='Time')
        print(f"✅ Loaded {len(self.df)} transactions")
        print(f"⚡ Speed Factor: {self.speed_factor}x")
        
    async def run(self, max_records=100):
        """Stream transactions to Azure Event Hubs"""
        print(f"📡 Connecting to Event Hub: {self.hub_name}...")
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=self.conn_str,
            eventhub_name=self.hub_name
        )
        
        try:
            # Create the first batch
            batch = await self.producer.create_batch()
            
            # Get records to stream
            records = self.df.head(max_records).to_dict('records')
            prev_time = records[0]['Time']
            
            print(f"\n🚀 Starting stream of {max_records} records...")
            print("=" * 70)
            
            sent_count = 0
            for i, record in enumerate(records):
                curr_time = record['Time']
                
                # Calculate delay to simulate real-time
                time_delta = curr_time - prev_time
                real_delay = time_delta / self.speed_factor
                
                if real_delay > 0:
                    await asyncio.sleep(real_delay)
                
                # Prepare event
                event_body = json.dumps(record)
                
                try:
                    # Attempt to add to current batch
                    batch.add(EventData(event_body))
                except ValueError:
                    # Batch is full - send it and start a new one
                    await self.producer.send_batch(batch)
                    sent_count += len(batch)
                    print(f"📤 Sent batch! Total so far: {sent_count}")
                    
                    batch = await self.producer.create_batch()
                    batch.add(EventData(event_body))
                
                # Progress update every 500 records
                if (i + 1) % 500 == 0:
                    fraud_label = "🚨 FRAUD" if record['Class'] == 1 else "✅ LEGIT"
                    print(f"--- Progress: [{i+1}/{max_records}] | Last Amount: ${record['Amount']:.2f} | {fraud_label} ---")
                
                prev_time = curr_time
            
            # CRITICAL: Send the final batch that wasn't full yet
            if len(batch) > 0:
                print(f"📤 Sending final remaining {len(batch)} records...")
                await self.producer.send_batch(batch)
                sent_count += len(batch)
            
            print("=" * 70)
            print(f"✅ FINISHED! Successfully pushed {sent_count} transactions to Azure.")
            
        except Exception as e:
            print(f"❌ Error during streaming: {e}")
        finally:
            await self.producer.close()
            print("🔒 Connection closed.")

async def main():
    # Increase max_records to 10000 once you confirm the 1000-record test works
    TEST_LIMIT = 1000 
    
    sim = AzureFraudSimulator(
        DATASET_PATH, 
        CONNECTION_STRING, 
        EVENT_HUB_NAME,
        SPEED_FACTOR
    )
    
    try:
        sim.load_data()
        await sim.run(max_records=TEST_LIMIT)
    except Exception as e:
        print(f"❌ Main Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())