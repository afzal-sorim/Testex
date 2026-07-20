import re
import sys

filepath = 'c:/Users/ST-Sivaranjini/Downloads/java_convertion 4/frontend/src/pages/MigrationCenter.jsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract Migration History block from parameter form
# Find:
#         {/* Migration History Section - appears after rocket */}
#         <section className="mt-8">
#           ...
#         </section>
#       </div>

migration_history_regex = re.compile(
    r'(\s*{\/\* Migration History Section - appears after rocket \*\/}\s*<section className="mt-8">.*?</section>\s*)\</div>',
    re.DOTALL
)

match = migration_history_regex.search(content)
if not match:
    print("Could not find migration history block")
    sys.exit(1)

migration_history_block = match.group(1)
content = content[:match.start()] + '\n      </div>' + content[match.end():]

# Transform the migration history block to be its own card
migration_history_new = f"""
      {{/* Migration History Section */}}
      <div className="p-6 glass-card mb-8">
        <section>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Clock className="text-brand-500" size={{20}} />
            Migration History
          </h3>
          <MigrationHistoryTable history={{history}} clearHistory={{clearHistory}} loading={{loading}} />
        </section>
      </div>
"""


# 2. Extract Validation Blocks
# - Build Check
build_check_re = re.compile(r'(\s*<div className="p-6 glass-card">\s*<h3 className="text-md font-bold text-slate-900 dark:text-white mb-4 flex items-center justify-between">\s*Build Check & Verification\s*</h3>.*?<div className="text-xs text-slate-400 italic">No files modified</div>\s*}\s*</div>\s*</div>)', re.DOTALL)
match = build_check_re.search(content)
if not match:
    print("Could not find build check block")
    sys.exit(1)
build_check_block = match.group(1)
content = content[:match.start()] + content[match.end():]

# - Playwright
playwright_re = re.compile(r'(\s*{\/\* Playwright Test Summary Card \*\/}\s*<div className="p-6 glass-card mt-6">.*?</PlaywrightTestSummary>\s*</div>)', re.DOTALL)
match = playwright_re.search(content)
if not match:
    print("Could not find playwright block")
    sys.exit(1)
playwright_block = match.group(1)
content = content[:match.start()] + content[match.end():]

# - Audit Reports
audit_re = re.compile(r'(\s*<div className="mt-auto pt-6">\s*{\/\* Reports Link \*\/}.*?View Migration Report\s*</button>\s*</div>\s*</div>)', re.DOTALL)
match = audit_re.search(content)
if not match:
    print("Could not find audit reports block")
    sys.exit(1)
audit_block = match.group(1)
content = content[:match.start()] + content[match.end():]

# 3. Modify Validation Blocks to remove 'mt-6' and add 'h-full flex flex-col justify-center'
build_check_new = build_check_block.replace('<div className="p-6 glass-card">', '<div className="p-6 glass-card h-full flex flex-col justify-start">')
playwright_new = playwright_block.replace('<div className="p-6 glass-card mt-6">', '<div className="p-6 glass-card h-full flex flex-col justify-start">')
audit_new = audit_block.replace('<div className="mt-auto pt-6">', '<div className="h-full flex flex-col justify-start">').replace('<div className="p-6 glass-card space-y-3">', '<div className="p-6 glass-card space-y-3 h-full flex flex-col justify-center">')

# 4. Construct the Horizontal Grid
horizontal_grid = f"""
      {{/* Horizontal Validation Grid */}}
      {{result && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fadeIn mb-8">
          {build_check_new.strip()}
          {playwright_new.strip()}
          {audit_new.strip()}
        </div>
      )}}
"""

# 5. Insert the grids back into the content
# We want to insert them right before {/* Error state */}
insert_point = content.find('{/* Error state */}')
if insert_point == -1:
    print("Could not find Error state insertion point")
    sys.exit(1)

content = content[:insert_point] + horizontal_grid + '\n' + migration_history_new + '\n      ' + content[insert_point:]

# 6. Change col-span-1 to flex-col gap-6
content = content.replace('<div className="lg:col-span-1 flex flex-col justify-between h-full">', '<div className="lg:col-span-1 flex flex-col justify-start h-full gap-6">')
content = content.replace('<div className="p-6 glass-card border-brand-500/20 mt-6">', '<div className="p-6 glass-card border-brand-500/20">')
content = content.replace('<div className="p-6 glass-card mt-6">', '<div className="p-6 glass-card">')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Refactor completed successfully!")
