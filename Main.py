import requests
import time
import json
import sys
import os

# Your AbstractAPI key (for phone number validation)
API_KEY = "957d9c2310f241c89553ddd116cdb4ae"

def simulate_trace_animation():
    stages = [
        "Checking carrier...",
        "Verifying line type...",
        "Pinging international gateway...",
        "Geo-locating network origin...",
        "Analyzing spam reports...",
        "Correlating with OCFT Database...",
        "Finalizing trace..."
    ]
    for i, stage in enumerate(stages):
        percent = int((i + 1) / len(stages) * 100)
        bar = "■" * (i + 1) + "□" * (len(stages) - i - 1)
        print(f"[{bar}] {percent}% — {stage}")
        time.sleep(0.4)
    print("[■■■■■■■■■■] 100% — Trace complete.\n")

def phone_lookup(number):
    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEY}&phone={number}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def log_result(data, number):
    if not os.path.exists("traces"):
        os.makedirs("traces")
    safe_number = number.replace("+", "").replace(" ", "")
    filename = f"traces/trace_{safe_number}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def print_result(data):
    print("📞 Trace Results")
    print("-" * 40)
    print(f"Number:      {data.get('format', {}).get('international', 'N/A')}")
    print(f"Country:     {data.get('country', {}).get('name', 'N/A')}")
    print(f"Region:      {data.get('location', 'N/A')}")
    print(f"Carrier:     {data.get('carrier', 'N/A')}")
    print(f"Line Type:   {data.get('type', 'N/A')}")
    print(f"Valid:       {data.get('valid', False)}")
    print("-" * 40)

def main():
    if len(sys.argv) < 2:
        print("Usage: python OCFT_CallTrace.py <phone_number>")
        print("Example: python OCFT_CallTrace.py +17063300069")
        return

    phone_number = sys.argv[1]
    print(f"Starting trace on {phone_number}...\n")
    simulate_trace_animation()

    print("📡 Contacting data provider...")
    data = phone_lookup(phone_number)

    if not data or not data.get("valid", False):
        print("❌ Invalid or untraceable number.")
        return

    print_result(data)
    log_result(data, phone_number)

    safe_number = phone_number.replace("+", "").replace(" ", "")
    print(f"\n✅ Trace data saved to traces/trace_{safe_number}.json")

if __name__ == "__main__":
    main()
  
