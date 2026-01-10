# Deployment Strategy: Auto-Diligence System ☁️

## 1. The Challenge with Vercel ⚠️
You mentioned you are familiar with **Vercel**. While Vercel is amazing for Frontend (React/Next.js), it is **NOT SUITABLE** for this specific internal backend for two reasons:
1.  **No Memory (Ephemeral)**: Vercel uses "Serverless Functions". Every time the agent finishes a task, Vercel **wipes the hard drive**. Your `cfo.db` (Financial History) and `chroma_data` (Vector Memory) would be deleted instantly.
2.  **No Infinite Loops**: Our Scheduler (`run_agents.py`) needs to sleep for 6 hours. Vercel kills any process that runs longer than **10 seconds**.

## 2. The Solution: Persistent Cloud (Railway / Render) 🚉
To enable "Future Prediction" and maintain the Vector Database, you need a server that **keeps running** and **remembers data**.
I recommend **Railway.app** or **Render.com**. They are as easy as Vercel but allow:
*   **Persistent Disk**: Your DBs grow over time.
*   **Background Workers**: Your Scheduler runs 24/7.

## 3. Deployment Steps (Railway Example)

### Step A: Preparation (What to do before deploying)
1.  **Secrets**: You need your `GITHUB_TOKEN` ready.
2.  **Procfile**: We already created it (`web: uvicorn ...`).
3.  **Requirements**: We already created it.

### Step B: The "Vector" Issue
Since `chroma_data` is heavy and ignored in Git, you have two choices:
*   **Option 1 (Fresh Start - Recommended)**: Deploy empty. The system will auto-create the DB. You must run the `backfill.py` script **ON** the server (via Railway Console) to restore the 2-year history.
*   **Option 2 (Upload)**: Commit the `chroma_data` (Not recommended, huge file size).

### Step C: How "Future Prediction" Works Live 🔮
Once deployed on Railway:
1.  **The Scheduler**: Runs every 6 hours automatically.
2.  **Data Accumulation**:
    *   Day 1: 15 Vectors.
    *   Day 30: 450 Vectors.
3.  **Benefit**: In 3 months, the system will compare New News against the **exact trend line** it observed while you slept. This is how "Mean Reversion" analysis becomes possible.

## 4. If you MUST use Vercel...
You would need to rewrite the entire architecture:
*   **Database**: Migrated to **Supabase** (Postgres).
*   **Vectors**: Migrated to **Pinecone** (Cloud Vector DB).
*   **Scheduler**: Migrated to **GitHub Actions** (Cron Triggers).
*   *Verdict*: This is weeks of refactoring. Stick to Railway/Render for this Python Agent.
