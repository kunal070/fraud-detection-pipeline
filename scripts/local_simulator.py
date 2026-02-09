import pandas as pd
import time
import json

class LocalFraudSimulator:
    def __init__(self, filepath, speed_factor=100):
        self.filepath = filepath
        self.speed_factor = speed_factor
        self.df = None
        
    def load_data(self):
        """Load and sort dataset by Time"""
        print(f"Loading dataset from {self.filepath}...")
        self.df = pd.read_csv(self.filepath)
        self.df = self.df.sort_values(by='Time')
        print(f"Loaded {len(self.df)} transactions")
        
    def simulate(self, max_records=100):
        """Simulate streaming by printing transactions with delays"""
        records = self.df.head(max_records).to_dict('records')
        
        prev_time = records[0]['Time']
        print(f"\n🚀 Starting simulation (Speed: {self.speed_factor}x)")
        print("=" * 60)
        
        for i, record in enumerate(records):
            curr_time = record['Time']
            
            # Calculate delay
            time_delta = curr_time - prev_time
            real_delay = time_delta / self.speed_factor
            
            # Wait
            if real_delay > 0:
                time.sleep(real_delay)
            
            # Print transaction
            fraud_label = "🚨 FRAUD" if record['Class'] == 1 else "✅ LEGIT"
            print(f"[{i+1}] Time: {curr_time:.0f}s | Amount: ${record['Amount']:.2f} | {fraud_label}")
            
            prev_time = curr_time
        
        print("=" * 60)
        print("✅ Simulation complete!")

if __name__ == "__main__":
    sim = LocalFraudSimulator('../data/creditcard.csv', speed_factor=1000)
    sim.load_data()
    sim.simulate(max_records=50)  # Test with 50 records