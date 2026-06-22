import requests
import json

API_URL = "http://localhost:8000/analyze"

test_prompts = [
    "NASA's James Webb Space Telescope released new images of Neptune.",
    "Lionel Messi joins Inter Miami CF.",
    "Scientists discover that milk is actually liquid plastic.",
    "Drinking sea water increases IQ by 30 points.",
    "Microsoft acquisition of Activision Blizzard completed."
]

for prompt in test_prompts:
    print(f"Testing: {prompt}")
    try:
        res = requests.post(API_URL, json={"text": prompt}, timeout=30)
        data = res.json()
        print(f"VERDICT: {data['final_verdict']} | SCORE: {data['truth_score']}")
        print(f"EXPLANATION: {data['explanation']}")
        print(f"SYNOPSIS: {data['neural_synthesis'][:120]}...")
        print("-" * 50)
    except Exception as e:
        print(f"ERROR: {e}")
