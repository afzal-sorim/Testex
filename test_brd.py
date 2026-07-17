import sys
import json
from pathlib import Path

cache_file = Path(r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\workspace\analysis_cache.json")
repo_url = "https://github.com/PRIYANKA-RAVI-ST/Student_Mangement_System.git"

cache_data = None
if cache_file.exists():
    try:
        cache = json.loads(cache_file.read_text(encoding="utf-8"))
        for key, data in cache.items():
            print(f"Checking key: {key}")
            if data.get("repoUrl") == repo_url:
                cache_data = data
                print("Found match!")
                break
    except Exception as e:
        print(f"Error parsing cache: {e}")

if not cache_data:
    print("No cache data found.")
else:
    full_brd_report = cache_data.get("fullBrdReport", {})
    if not full_brd_report:
        print("No fullBrdReport.")
    else:
        print("Success! fullBrdReport exists.")
