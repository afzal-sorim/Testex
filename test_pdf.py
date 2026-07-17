import sys
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import io

cache_file = Path(r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\workspace\analysis_cache.json")
repo_url = "https://github.com/PRIYANKA-RAVI-ST/Student_Mangement_System.git"

cache_data = None
cache = json.loads(cache_file.read_text(encoding="utf-8"))
for key, data in cache.items():
    if data.get("repoUrl") == repo_url:
        cache_data = data
        break

full_brd_report = cache_data.get("fullBrdReport", {})

templates_dir = Path(r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend\app\templates")
env = Environment(loader=FileSystemLoader(str(templates_dir)))
template = env.get_template("brd_full_template.html")
html_out = template.render(full_brd_report)

pdf_buffer = io.BytesIO()
pisa_status = pisa.CreatePDF(io.StringIO(html_out), dest=pdf_buffer)

if pisa_status.err:
    print("Error during PDF generation")
else:
    print("PDF generated successfully.")
