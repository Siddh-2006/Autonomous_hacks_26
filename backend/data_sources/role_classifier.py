from typing import List, Dict

def classify_roles(titles: List[str]) -> Dict[str, int]:
    """
    Classifies a list of job titles into categories: Engineering, Sales, Ops, Other.
    """
    categories = {
        "engineering": 0,
        "sales": 0,
        "ops": 0,
        "other": 0
    }

    # Simple keyword matching
    keywords = {
        "engineering": ["engineer", "developer", "architect", "data", "qa", "test", "tech", "software"],
        "sales": ["sales", "account", "business development", "sdr", "ae", "revenue"],
        "ops": ["finance", "hr", "legal", "operations", "recruiter", "people", "admin"]
    }

    for title in titles:
        title_lower = title.lower()
        matched = False
        
        for cat, keys in keywords.items():
            if any(k in title_lower for k in keys):
                categories[cat] += 1
                matched = True
                break
        
        if not matched:
            categories["other"] += 1

    return categories

def analyze_seniority(titles: List[str]) -> Dict[str, int]:
    """
    Analyzes the seniority mix of open roles.
    """
    seniority = {
        "exec": 0,    # VP, C-Level, Director, Head of
        "senior": 0,  # Senior, Staff, Principal, Lead
        "junior": 0,  # Junior, Associate, Intern, II, III (often mid but usually individual contrib)
        "entry": 0    # No prefix, or 'Entry Level'
    }
    
    # Weights/Keywords
    exec_keys = ["vp", "vice president", "chief", "director", "head of"]
    senior_keys = ["senior", "staff", "principal", "lead", "architect", "manager"]
    junior_keys = ["junior", "associate", "intern", "graduate", " i ", " ii "]

    for title in titles:
        t = title.lower()
        if any(k in t for k in exec_keys):
            seniority["exec"] += 1
        elif any(k in t for k in senior_keys):
            seniority["senior"] += 1
        elif any(k in t for k in junior_keys):
            seniority["junior"] += 1
        else:
            seniority["entry"] += 1 # Default bucket
            
    return seniority
