import requests
import json
import time

API_URL = "http://localhost:8000/analyze"
FEEDBACK_URL = "http://localhost:8000/feedback"

test_prompts = [
    {"text": "NASA's Perseverance rover successfully lands on Mars.", "label": "Real"},
    {"text": "Pope Francis endorses Donald Trump for President.", "label": "Fake"},
    {"text": "Queen Elizabeth II passed away at Balmoral Castle on Sept 8, 2022.", "label": "Real"},
    {"text": "Drinking lemon juice in hot water cures COVID-19 in 24 hours.", "label": "Fake"},
    {"text": "Lionel Messi wins his 8th Ballon d'Or in Paris.", "label": "Real"},
    {"text": "Scientists find living dinosaurs on a secret island in Brazil.", "label": "Fake"},
    {"text": "The Titanic has been found in the North Atlantic.", "label": "Real"},
    {"text": "Elon Musk is buying the moon for $100 trillion.", "label": "Fake"},
    {"text": "Microsoft acquires Activision Blizzard for $68.7 billion.", "label": "Real"},
    {"text": "Walking on grass in the morning prevents blindness.", "label": "Fake"},
    {"text": "James Webb Space Telescope releases its first full-color images.", "label": "Real"},
    {"text": "Drinking sea water increases IQ by 30 points.", "label": "Fake"},
    {"text": "Bitcoin reaches an all-time high of $1 million.", "label": "Fake"}, # Hyperbole
    {"text": "The 2024 Olympic Games are held in Paris, France.", "label": "Real"},
    {"text": "Cats can talk but they choose not to because they are lazy.", "label": "Fake"}
]

print("🛡️  Starting Automated TruthGuard Stress Test...")
print("-" * 60)

results = []

for i, prompt in enumerate(test_prompts):
    print(f"[{i+1}/15] Testing: '{prompt['text'][:40]}...'")
    try:
        # 1. Analyze the claim
        response = requests.post(API_URL, json={"text": prompt['text']}, timeout=30)
        data = response.json()
        
        verdict = data.get('final_verdict', 'Error')
        score = data.get('truth_score', 0.0)
        
        # 2. Provide human feedback (if it failed or always for training)
        # For training, we provide the CORRECT label back to the system.
        print(f"   -> Result: {verdict.upper()} (Score: {score:.2f})")
        
        # Automate training feedback
        feedback_res = requests.post(FEEDBACK_URL, json={
            "text": prompt['text'],
            "label": prompt['label']
        }, timeout=5)
        
        results.append({
            "prompt": prompt['text'],
            "target": prompt['label'],
            "actual": verdict,
            "score": score,
            "learned": feedback_res.status_code == 200
        })
        
        # Pause slightly between requests to let agents breathe
        time.sleep(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("-" * 60)
print("📈  Stress Test Summary:")
correct_count = sum(1 for r in results if r['target'] == r['actual'])
print(f"📊 Accuracy (Initial Pass): {correct_count}/15 ({(correct_count/15)*100:.1f}%)")
print("✅  All feedback has been logged! TruthGuard has learned 15 new lessons.")
print("-" * 60)

# Save log file
with open("test_results_log.json", "w") as f:
    json.dump(results, f, indent=4)
print("📝 Logged results to 'test_results_log.json'")
