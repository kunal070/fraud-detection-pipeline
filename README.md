# 🚨 Real-Time Fraud Detection Pipeline
### Azure Event Hubs | Databricks | Delta Lake | Power BI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4?style=flat-square&logo=microsoft-azure)
![Databricks](https://img.shields.io/badge/Databricks-Unified%20Analytics-FF3621?style=flat-square&logo=databricks)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-ACID%20Compliant-000000?style=flat-square)
![Power BI](https://img.shields.io/badge/Power%20BI-Interactive%20Dashboards-F2C80F?style=flat-square&logo=microsoft-power-bi)
![Status](https://img.shields.io/badge/Status-Complete-28a745?style=flat-square)

---

## 📊 Project Overview

This project implements a **production-grade real-time fraud detection pipeline** that processes credit card transactions from ingestion to visualization. Built using modern data engineering practices, it demonstrates:

- Real-time streaming with sub-second latency
- Cloud-native architecture on Azure
- Medallion (Bronze/Silver/Gold) data architecture
- Interactive analytics dashboards with Power BI
- Scalable processing of 284K+ transactions

---

## 🎯 Business Impact

| Insight | Detail |
|--------|--------|
| **Off-Hours Fraud** | 25.2% of fraud occurs during midnight–6am, enabling optimized fraud team scheduling |
| **High-Value Fraud** | Frauds >€1,000 represent only 2% of transactions but **22% of total fraud value** |
| **Peak Fraud Hour** | Hour 11 identified as peak, suggesting coordinated attack patterns |
| **Analyst Efficiency** | Interactive exploration reduces investigation time via self-service analytics |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                   │
└─────────────────────────────────────────────────────────────────────┘

CSV Dataset (284K records)
    ↓
Python Async Simulator
    ├── Reads transactions chronologically
    ├── Respects time deltas (48-hour replay)
    ├── Batches events for efficiency
    └── Streams via HTTPS/AMQP
         ↓
Azure Event Hubs (Ingestion Layer)
    ├── Partitioned streaming
    ├── 1 TU throughput
    └── Two consumers:
         ├─────────────────────────┬──────────────────────────┐
         ↓                         ↓                          ↓
Azure Stream Analytics    Azure Databricks         Event Hubs Capture
    ├── SQL windowing         ├── Bronze Layer          ├── Avro format
    ├── Real-time aggs        ├── Silver Layer          └── Blob Storage
    └── JSON output           └── Gold Layer
         ↓                         ↓
    Blob Storage           Delta Lake Tables
         ↓                         ↓
         └─────────────────────────┘
                   ↓
            Power BI Dashboard
              ├── Fraud Overview
              ├── Temporal Analysis
              ├── Amount Analysis
              └── Interactive Explorer
```

---

## 🛠️ Technology Stack

### Data Ingestion & Streaming
| Technology | Role |
|-----------|------|
| Python 3.9+ | Async simulator with `asyncio` |
| Azure Event Hubs | Managed event streaming service |
| Azure Stream Analytics | SQL-based stream processing |

### Data Processing & Storage
| Technology | Role |
|-----------|------|
| Azure Databricks | Unified analytics platform |
| Apache Spark (PySpark) | Distributed data processing |
| Delta Lake | ACID-compliant data lake storage |
| Azure Blob Storage | Cloud object storage |

### Analytics & Visualization
| Technology | Role |
|-----------|------|
| Power BI Desktop | Interactive dashboards |
| DAX | Custom measures and calculations |

### Development & DevOps
| Technology | Role |
|-----------|------|
| Git/GitHub | Version control |
| Jupyter Notebooks | Exploratory data analysis |
| VS Code | IDE |

---

## 📁 Project Structure

```
fraud-detection-pipeline/
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
│
├── data/                          # Dataset storage
│   └── creditcard.csv            # Kaggle fraud dataset (284,807 records)
│
├── notebooks/                     # Jupyter notebooks
│   └── 01_eda.ipynb              # Exploratory Data Analysis
│
├── scripts/                       # Python scripts
│   ├── local_simulator.py        # Local testing simulator
│   ├── azure_simulator.py        # Production Azure simulator
│   └── test_connection.py        # Connection validation
│
├── databricks_notebook/           # Databricks notebooks (exported)
│   ├── 01_setup_connections.py   # Storage & Event Hubs setup
│   ├── 02_bronze_layer.py        # Raw data ingestion
│   ├── 04_silver_layer.py        # Data cleaning & transformation
│   └── 05_gold_layer.py          # Business aggregations
│
├── config/                        # Configuration (not in Git)
│   └── .env                      # Environment variables
│
└── docs/                          # Documentation
    ├── architecture.png          # Architecture diagram
    └── dashboard_screenshots/    # Power BI screenshots
```

---

## 🚀 Getting Started

### Prerequisites

**Required:**
- Python 3.9 or higher
- Azure subscription (free tier works)
- Power BI Desktop (for dashboards)

**Azure Services Needed:**
| Service | Tier | Estimated Cost |
|---------|------|----------------|
| Event Hubs Namespace | Basic | ~$10/month |
| Databricks Workspace | 14-day free trial | Free (trial) |
| Storage Account | LRS | ~$1/month |
| Stream Analytics Job | — | Charged only when running |

---

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/kunal070/fraud-detection-pipeline.git
cd fraud-detection-pipeline
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Download Dataset

Download the **Credit Card Fraud Detection** dataset from Kaggle:
- **URL:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- Save as `data/creditcard.csv`

#### 4. Configure Azure Credentials

Create `config/.env` file:
```env
EVENT_HUB_CONN_STR=Endpoint=sb://YOUR_NAMESPACE.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_KEY
EVENT_HUB_NAME=fraud-detection-stream
```

---

## 🎯 Usage

### Step 1: Exploratory Data Analysis

```bash
jupyter notebook notebooks/01_eda.ipynb
```

**What it does:**
- Loads the 284K transaction dataset
- Analyzes class imbalance (0.17% fraud)
- Visualizes transaction distributions
- Identifies temporal patterns

---

### Step 2: Azure Infrastructure Setup

#### Create Azure Resources:

**Event Hubs Namespace:**
```bash
az eventhubs namespace create \
  --name fraud-detection-ns \
  --resource-group fraud-detection-rg \
  --location eastus \
  --sku Basic
```

**Event Hub:**
```bash
az eventhubs eventhub create \
  --name fraud-detection-stream \
  --namespace-name fraud-detection-ns \
  --resource-group fraud-detection-rg \
  --partition-count 2
```

**Storage Account (for Event Hubs Capture & Databricks):**
```bash
az storage account create \
  --name fraudstorageYOURNAME \
  --resource-group fraud-detection-rg \
  --location eastus \
  --sku Standard_LRS
```

**Databricks Workspace:**
- Create via Azure Portal
- Select **14-day Premium trial** (or Standard tier)

---

### Step 3: Run Data Simulator

**Test locally first:**
```bash
python scripts/local_simulator.py
```

**Stream to Azure:**
```bash
python scripts/azure_simulator.py
```

**Configuration options in `azure_simulator.py`:**
```python
SPEED_FACTOR = 1000  # 1000x faster than real-time
max_records = 500    # Number of transactions to stream
```

---

### Step 4: Databricks Setup

1. **Import notebooks** to Databricks workspace
2. **Create compute cluster:**
   - Cluster mode: Single Node
   - Runtime: 14.3 LTS or higher
   - Node type: Standard_D4ds_v5

3. **Run notebooks in order:**

| Order | Notebook | Purpose |
|-------|----------|---------|
| 1 | `01_setup_connections` | Configure storage access |
| 2 | `02_bronze_layer` | Ingest from Event Hubs |
| 3 | `04_silver_layer` | Clean and transform |
| 4 | `05_gold_layer` | Create business aggregations |

---

### Step 5: Power BI Dashboard

1. Open **Power BI Desktop**
2. **Connect to Databricks:**
   - Get Data → Azure → Azure Databricks
   - Enter server hostname and HTTP path (from Databricks SQL Warehouse)
   - Authenticate with **Personal Access Token**

3. **Import Gold tables:**
   - `gold_fraud_summary`
   - `gold_hourly_patterns`
   - `gold_high_value_alerts`

4. Build dashboards (or import provided `.pbix` file)

---

## 📊 Dashboard Pages

### 1. Fraud Overview
**Purpose:** Executive summary with key metrics

**Visuals:**
- Total Transactions (KPI card)
- Fraud Percentage (KPI card)
- Total Amount Processed (KPI card)
- Average Transaction Amount (KPI card)
- Fraud vs Legitimate Distribution (Donut chart)
- Recent Flagged Transactions (Table)

> **Key Insight:** Only 0.20% of transactions are fraudulent, but they represent significant financial risk.

---

### 2. Temporal Analysis
**Purpose:** Identify when fraud occurs

**Visuals:**
- Fraud Count by Hour (Line chart)
- Fraud Distribution by Time Period (Column chart)
- Peak Fraud Hour (KPI card)
- Off-Hours Fraud Percentage (KPI card)

> **Key Insight:** 25.2% of fraud occurs during off-hours (midnight–6am), suggesting automated bot attacks.

---

### 3. Amount Analysis
**Purpose:** Understand fraud patterns by transaction value

**Visuals:**
- Transaction Distribution by Category (Column chart)
- Amount vs Time Scatter Plot (Fraud highlighted)
- Fraud Value by Category (Donut chart)
- Highest / Average / Total Fraud Amount (KPI cards)

> **Key Insight:** High-value frauds (>€1,000) are only 2% of fraud cases but 22% of total fraud value.

---

### 4. Interactive Explorer
**Purpose:** Self-service analytics for fraud analysts

**Features:**
- **Slicers:** Amount Category, Transaction Type, Time Period, Alert Severity, Amount Range
- **Dynamic Visuals:** Matrix, Combo Chart, Bar Chart, Filtered Transactions Table
- **Cross-filtering:** All visuals respond to slicer selections

> **Use Case:** Analysts can answer ad-hoc questions like *"What do high-value frauds during night hours look like?"*

---

## 🧪 Key Features

### Medallion Architecture (Lakehouse Pattern)

#### 🥉 Bronze Layer (Raw Zone)
- Ingests raw JSON from Event Hubs
- Schema: All 30 original columns preserved
- Format: Delta Lake
- Purpose: Immutable audit trail

#### 🥈 Silver Layer (Cleansed Zone)
- Removes nulls and duplicates
- Adds derived columns:
  - `transaction_hour` — Hour of day (0–47)
  - `is_high_value` — Flag for amounts >€1,000
  - `is_fraud` — Boolean fraud indicator
  - `amount_category` — Small / Medium / Large / Very Large
- Format: Delta Lake with ACID transactions

#### 🥇 Gold Layer (Curated Zone)
- Business-ready aggregations
- **Three tables:**
  - `gold_fraud_summary` — Overall statistics
  - `gold_hourly_patterns` — Time-based analysis
  - `gold_high_value_alerts` — High-risk transactions
- Purpose: Optimized for BI consumption

---

### Real-Time Streaming

**Event-Driven Architecture:**
```python
# Python simulator uses async I/O
async def send_batch(self, records):
    batch = await self.producer.create_batch()
    for record in records:
        batch.add(EventData(json.dumps(record)))
    await self.producer.send_batch(batch)
```

**Structured Streaming in Databricks:**
```python
# Bronze layer ingestion
df_stream = spark.readStream \
    .format("eventhubs") \
    .options(**ehConf) \
    .load()

df_bronze.writeStream \
    .format("delta") \
    .option("checkpointLocation", checkpoint_path) \
    .toTable("bronze_transactions")
```

---

## 📈 Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **Total Transactions** | 284,807 | Full Kaggle dataset |
| **Fraud Cases** | 492 | 0.17% of total |
| **Streaming Throughput** | 1 TU | Supports up to 1000 events/sec |
| **Processing Latency** | <1 second | Bronze ingestion |
| **Data Freshness** | Real-time | Sub-second E2E latency |
| **Storage Format** | Delta Lake | ACID compliance |
| **Dashboard Pages** | 4 | 20+ interactive visuals |
| **DAX Measures** | 12+ | Custom calculations |

---

## 🎓 Learning Outcomes

### Technical Skills Acquired

**Data Engineering:**
- Real-time data streaming patterns
- Event-driven architecture design
- Async programming in Python
- Cloud infrastructure setup (Azure)
- Medallion architecture implementation
- Delta Lake & ACID transactions
- PySpark transformations
- Checkpoint & watermarking strategies

**Data Analytics:**
- Exploratory data analysis
- Class imbalance handling
- Temporal pattern analysis
- Statistical segmentation
- Interactive dashboard design
- DAX measure creation
- Cross-filtering logic

**Tools & Technologies:**
- Azure Event Hubs
- Azure Databricks
- Azure Stream Analytics
- Power BI & DAX
- Python (`asyncio`, `pandas`, `azure-sdk`)
- Apache Spark (PySpark)
- Delta Lake
- Git/GitHub

---

## 🐛 Troubleshooting

### Common Issues

**1. Event Hubs Connection Error**
```
Error: "No EntityPath has been set in the Event Hubs connection string"
```
**Solution:** Add `;EntityPath=fraud-detection-stream` to your connection string

---

**2. Databricks Unity Catalog Error**
```
Error: "Public DBFS root is disabled"
```
**Solution:** Use managed tables instead of file paths:
```python
.toTable("catalog_name.schema_name.table_name")
```

---

**3. Power BI Can't Connect to Databricks**

**Solution:**
- Ensure SQL Warehouse is running
- Use **Personal Access Token** (not Microsoft account)
- Verify firewall allows Power BI

---

**4. Simulator Runs Too Fast/Slow**

**Solution:** Adjust `SPEED_FACTOR` in `azure_simulator.py`:
```python
SPEED_FACTOR = 1      # Real-time (48 hours)
SPEED_FACTOR = 100    # 100x faster (~30 minutes)
SPEED_FACTOR = 1000   # 1000x faster (~3 minutes)
```

---

## 🔮 Future Enhancements

- [ ] **Machine Learning Integration** — Train fraud detection model (Random Forest, XGBoost)
- [ ] **Real-time Alerts** — Trigger SMS/Email when fraud detected
- [ ] **MLflow Integration** — Model tracking and versioning
- [ ] **Automated Retraining** — Daily model refresh pipeline
- [ ] **Cost Optimization** — Implement auto-scaling and spot instances
- [ ] **Monitoring Dashboard** — Azure Monitor + Application Insights
- [ ] **CI/CD Pipeline** — GitHub Actions for automated deployment
- [ ] **Multi-Region Deployment** — Geographic redundancy
- [ ] **API Endpoint** — REST API for real-time scoring
- [ ] **A/B Testing Framework** — Test model variants

---

## 📚 References & Resources

### Dataset
- **Kaggle Credit Card Fraud Detection:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Research Paper:** Andrea Dal Pozzolo et al. *"Calibrating Probability with Undersampling for Unbalanced Classification"*

### Documentation
- **Azure Event Hubs:** https://learn.microsoft.com/azure/event-hubs/
- **Azure Databricks:** https://learn.microsoft.com/azure/databricks/
- **Delta Lake:** https://delta.io/
- **Power BI:** https://learn.microsoft.com/power-bi/

### Learning Resources
- **Medallion Architecture:** https://www.databricks.com/glossary/medallion-architecture
- **Structured Streaming:** https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
- **DAX Guide:** https://dax.guide/

---

## 👤 Author

**Kunal Panchal**

- GitHub: [@kunal070](https://github.com/kunal070)
- LinkedIn: [linkedin.com/in/kunal0303](https://www.linkedin.com/in/kunal0303/)
- Email: kp058665@gmail.com

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Kaggle** for providing the fraud detection dataset
- **Machine Learning Group - ULB** for the original research
- **Microsoft Azure** for cloud platform
- **Databricks** for unified analytics platform
- **Power BI Community** for visualization inspiration

---

- *Built by Kunal Panchal*
- *Last Updated: January 2025*
