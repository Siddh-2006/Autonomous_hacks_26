# Deployment Cheat Sheet: Railway.app 🚀

You asked "Where do I deploy?". Here is the direct link and steps.

## 1. The Website
**URL**: [https://railway.app](https://railway.app)

## 2. Steps to Go Live
1.  **Login**: Click "Login" and select **GitHub**.
2.  **New Project**: Click the purple **" + New Project"** button.
3.  **Source**: Select **"Deploy from GitHub repo"**.
4.  **Select Repo**: Choose your repository: `Siddh-2006/Autonomous_hacks_26`.
5.  **Deploy**: Click "Deploy Now".

## 3. Environment Variables (Critical!)
Once the project is created, go to the **"Variables"** tab in Railway dashboard.
Add this variable:
*   `GITHUB_TOKEN` = (Paste your GitHub Personal Access Token here)

*Note: You do not need to set PORT, Railway handles it automatically.*

## 4. That's it!
*   **Frontend**: Click the generated URL (e.g., `web-production-xyz.up.railway.app`) to see your Dashboard.
*   **Backend**: The scheduler is fast-asleep in the background, waking up every 6 hours.
*   **Vectors**: The system will auto-detect it's new and run the "Backfill" automatically on the first run.
