def fetch_latest_earnings_call():
    """
    Simulates fetching the latest Earnings Call Q&A segment.
    In a real system, this would scrape SeekingAlpha or Quartr.
    """
    return {
        "fiscal_quarter": "Q4 2024",
        "qa_pairs": [
            {
                "analyst": "Morgan Stanley",
                "question": "Can you explain the sudden drop in gross margins this quarter?",
                "answer": "We are very excited about the long-term roadmap and our AI initiatives are gaining traction." 
                # ^ Evasive
            },
            {
                "analyst": "Goldman Sachs",
                "question": "Are you planning any headcount reductions?",
                "answer": "We are continuing to hire for critical roles, but we are being prudent with spend."
                # ^ Semantically "No", but vague.
            },
            {
                "analyst": "JPMorgan",
                "question": " What is the churn rate in the enterprise segment?",
                "answer": "Enterprise churn increased by 1% due to legacy migrations."
                # ^ Direct
            }
        ]
    }
