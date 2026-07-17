import os

file_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\app\templates\brd_full_template.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    "var(--ink)": "#151515",
    "var(--paper)": "#ffffff",
    "var(--cream)": "#f5f4ef",
    "var(--soft)": "#fbfaf7",
    "var(--border)": "#d5d0c8",
    "var(--muted)": "#5e5a54",
    "var(--shadow)": "0 8px 32px rgba(0, 0, 0, 0.12)"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("CSS variables inlined in brd_full_template.html.")
