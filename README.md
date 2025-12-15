# 📊 Data Engineer – Jira Ticket Analysis Project

## 🧠 Overview

This project demonstrates a **full data engineering pipeline** built around **Jira ticket data**.

It simulates real-world Jira tickets, ingests them from the Jira API, enriches them using **NLP embeddings**, stores structured results in a database, and performs analytical insights such as **technology classification** and **server-level analysis**.

The project is designed with **clear separation of concerns**, async data ingestion, and modular analysis components.

---

## 🎯 Project Goals

* Generate and ingest realistic Jira tickets
* Store structured ticket data in a database
* Create semantic embeddings for text fields
* Classify tickets by technology domain
* Analyze server occurrences in ticket descriptions
* Export analytical results for inspection and visualization
* Follow production-style project structure

---

## 🚀 Key Capabilities

* ✅ Async Jira API ingestion (rate-limit aware)
* ✅ Realistic ticket description generation
* ✅ SQLite-based persistence layer
* ✅ Sentence Transformer embeddings (MiniLM)
* ✅ Ticket ↔ Technology semantic matching
* ✅ Keyword-enriched cosine similarity
* ✅ Server occurrence analysis using regex
* ✅ CSV export & plot generation
* ✅ Clean, interview-ready architecture

---

## 🗂️ Project Structure

```
data-enginer/
│
├── analysis/
│   ├── cosine_similarity.py      # Ticket ↔ Technology matching
│   ├── server_analysis.py        # Server statistics & visualization
│   └── __init__.py
│
├── db/
│   ├── connection.py             # SQLite connection handling
│   ├── schema.py                 # CREATE TABLE definitions
│   ├── repository.py             # DB read/write logic
│   └── __init__.py
│
├── embeddings/
│   ├── init_embeddings.py        # Ticket & technology embeddings
│   ├── utils.py                  # BLOB → numpy vector helpers
│   └── __init__.py
│
├── templates/
│   └── technologies.py           # Technology descriptions (domain knowledge)
│
├── utils/
│   ├── plot_utils.py             # Server counting & plots
│   ├── jira_utils.py             # Jira client & async ingestion
│   ├── config_utils.py           # Config loading (config.json)
│   └── __init__.py
│
├── main.py                       # Pipeline entry point
├── requirements.txt
└── README.md
```

---

## 📁 Folder Responsibilities

### `analysis/`

Contains **pure analysis logic**:

* Cosine similarity computation
* Keyword-based score enrichment
* Server extraction and statistics
* No database writes

> *Think of this as the brain of the system.*

---

### `db/`

Handles **all persistence concerns**:

* SQLite connections
* Table creation
* Insert / update / select operations

> *The storage layer.*

---

### `embeddings/`

Responsible for **NLP representation**:

* SentenceTransformer usage
* Embedding creation
* Vector serialization/deserialization

> *Easily replaceable embedding layer.*

---

### `templates/`

Contains **domain knowledge only**:

* Technology descriptions
* Text templates

> *Human knowledge injected into the system.*

---

### `utils/`

Reusable helpers and infrastructure code:

#### Jira utilities

* Jira client initialization
* Async ticket fetching with pagination
* Rate-limit–safe ingestion

#### Server analysis utilities

* Regex-based server extraction
* Frequency counting
* Bar plot generation (saved to file)

> *Support layer shared across the project.*

---

### `main.py`

The **orchestrator**:

* Runs ingestion
* Triggers embeddings
* Executes analysis
* Exports results

> No heavy logic, only pipeline control.

---

## 🧬 Technologies Used

* **Python 3**
* **Jira REST API**
* **SQLite**
* **pandas**
* **numpy**
* **matplotlib**
* **sentence-transformers (MiniLM)**

---

## 📦 Installation

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
python main.py
```

The pipeline will:

1. Connect to Jira
2. Fetch tickets asynchronously
3. Store structured ticket data
4. Create embeddings (if missing)
5. Match tickets to technologies
6. Analyze server occurrences
7. Export results (CSV + plots)

---

## 🧠 Ticket ↔ Technology Matching

1. Ticket descriptions → embeddings
2. Technology descriptions → embeddings
3. Cosine similarity computation
4. Keyword-based bonus applied
5. Best matching technology selected

> ⚠️ This is a **ranking system**, not a hard classifier.

---

## 📊 Outputs

* `ticket_technology_match.csv`
* `server_occurrences.png`
* Similarity scores per ticket
* Structured tables in SQLite

---

## 🧠 Design Principles

* Clear separation of concerns
* Async where I/O is involved
* Deterministic and reproducible
* Domain-aware (not “ML magic”)
* Easy to extend and explain

---

## 🚀 Possible Extensions

* Top-K technology matching
* Confidence labels (high / medium / low)
* Dashboard (Streamlit / Superset)
* Streaming ingestion
* Migration to PostgreSQL
* Feature store integration

---

## 📝 Summary

This project showcases:

* Practical data engineering skills
* Real-world Jira data ingestion
* NLP-based semantic analysis
* Clean, modular architecture
* Interview-ready design and explanations

