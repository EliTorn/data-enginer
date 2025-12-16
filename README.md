## 📌 Jira Ticket Data Engineering Pipeline

This file runs the **entire Jira data pipeline from start to finish**.

In short, it:

1. Connects to Jira
2. Fetches all Jira tickets
3. Saves the tickets locally
4. Analyzes servers mentioned in tickets
5. Runs embeddings to classify tickets by technology


## 🧠 What topics are covered in this pipeline?

* **Jira API ingestion**
* **Async data fetching**
* **Data persistence**
* **Server analysis (regex-based)**
* **NLP embeddings**
* **Technology classification**
* **Logging & pipeline orchestration**

---

## ⚙️ Required configuration (`config.json`)

At the **root of the project**, you must create a file called `config.json`:

```json
{
  "API_TOKEN": "YOUR_JIRA_API_TOKEN",
  "EMAIL": "your_email@gmail.com",
  "API_SERVER": "https://your-domain.atlassian.net"
}
```

This file is used to authenticate and connect to Jira.

❗ **Do not commit this file to GitHub**.

---

## 📥 How to clone and run the project

### 1. Clone the repository

```bash
git clone https://github.com/EliTorn/data-enginer.git
cd data-enginer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `config.json`

Create `config.json` in the project root (see above).

### 4. Run the pipeline

```bash
python main.py
```

---

## ✅ Summary (one sentence)

This file orchestrates a full Jira data pipeline: **fetch → store → analyze → classify**, using async code, embeddings, and clean modular design.

