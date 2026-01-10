import requests

def brute_force_tokens():
    tokens = ["couchbase", "couchbaseinc", "couchbasesystems", "couchbasecareers", "couchbasejobs"]
    
    for token in tokens:
        url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                print(f"[FOUND] Valid Token: {token}")
                print(f"URL: {url}")
                return token
            elif resp.status_code == 404:
                print(f"[FAIL] {token} (404)")
            else:
                print(f"[BLOCK] {token} ({resp.status_code})")
        except:
            pass

    print("No valid token found.")

if __name__ == "__main__":
    brute_force_tokens()
