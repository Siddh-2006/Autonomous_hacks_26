# 🧠 Vector Database Strategy: The "Long-Term Memory" Upgrade

## 1. Why SQL is Not Enough
Currently, our **SQLite** database stores *structured data* (numbers and strings):
*   `open_roles`: 12
*   `sentiment_score`: 0.8
*   `ceo_statement`: "We are optimizing efficiency."

**The Problem**: Relational DBs cannot understand *meaning*.
If the CEO says "We are streamlining operations" today, and 3 months ago they said "We are executing a reduction in force", SQLite sees two completely different strings.
**A Vector DB** understands that **"Streamlining" == "Reduction in Force"**. It captures the *intent*.

## 2. Importance in Auto-Diligence (Examples)

### Use Case A: Detecting "Narrative Drift" (The CEO Flip-Flop)
*   **Goal**: Has the CEO secretly changed their strategy without admitting it?
*   **Vector Query**: Embed the current strategy statement and search for the *most similar* past statement.
*   **Example**:
    *   *6 Months Ago*: "We are an **enterprise-first** database company."
    *   *Today*: "We are analyzing **PLG (Product-Led Growth)** opportunities."
    *   **Vector DB Insight**: These two vectors point in different directions. `Cosine Similarity < 0.6`.
    *   **Alert**: "STRATEGIC PIVOT DETECTED (Confidence: 90%)."

### Use Case B: Historical Risk Matching
*   **Goal**: Does today's financial snapshot look like a previous disaster?
*   **Vector Query**: Embed today's financial metrics + CFO commentary. Search history.
*   **Example**:
    *   *Today*: "CFO mentions 'macro headwinds' and 'conserving cash'."
    *   *Result*: The Vector DB matches this *exactly* to **Q3 2022**, just before the stock dropped 40%.
    *   **Alert**: "PATTERN MATCH: This language usually precedes a miss."

## 3. Implementation Plan

### Step 1: Choose the Tech
*   **Option A (Local)**: **ChromaDB**. Runs inside our Python app. Efficient, free, no API keys. **(Recommended)**.
*   **Option B (Cloud)**: **Pinecone**. Managed, scalable, costs money.

### Step 2: The Embedding Model
We need a model to turn text into numbers (Vectors).
*   **OpenAI Embeddings** (`text-embedding-3-small`): Cheap, high quality.
*   **Sentence-Transformers** (HuggingFace): Free, runs locally.

### Step 3: Integration (How to Code it)
1.  **Ingest**: Every time the CEO Agent runs, we send the `explanation` text to the Embedder.
2.  **Store**: Save the `List[float]` vector into ChromaDB with metadata `{'timestamp': '2026-01-11'}`.
3.  **Query**: Before the Board makes a verdict, it queries Chroma: *"Find the last 3 times the CEO sounded this defensive."*

## 4. Setup Guide (Draft)

1.  **Install**:
    ```bash
    pip install chromadb sentence-transformers
    ```

2.  **Code Snippet**:
    ```python
    import chromadb
    client = chromadb.PersistentClient(path="./brain_memory")
    collection = client.create_collection("ceo_narratives")

    # Store
    collection.add(
        documents=["We are optimizing for efficiency."],
        metadatas=[{"risk": "high"}],
        ids=["doc1"]
    )

    # Query
    results = collection.query(
        query_texts=["Are we firing people?"],
        n_results=1
    )
    # Output: ["We are optimizing for efficiency."] (It understands the link!)
    ```
