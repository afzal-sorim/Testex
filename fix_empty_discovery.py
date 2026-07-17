import os

file_path = r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\frontend\src\pages\Discovery.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Change the condition for the input area from (!repoUrl || error || loading) to (!result?.projectType || error || loading)
content = content.replace("{(!repoUrl || error || loading) && (", "{(!result?.projectType || error || loading) && (")

# There is a second nested condition right below it: {(!repoUrl || error) && ( ... }
# Change it to {(!result?.projectType || error) && (
content = content.replace("{(!repoUrl || error) && (", "{(!result?.projectType || error) && (")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed Discovery.jsx blank screen bug.")
