#!/usr/bin/env python3
"""Build the OpenAI upload ZIP from an explicit allowlist; no private files."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'plugin.json').read_text())
interface = manifest['extensions']['com.openai']['interface']
assert len(interface['displayName']) <= 30
assert len(interface['shortDescription']) <= 30
assert len(interface['longDescription']) <= 4000
cases = manifest['extensions']['com.openai']['review']['test_cases']
assert len(cases['positive']) == 5 and len(cases['negative']) == 3
files = [root / name for name in ('plugin.json', 'mcp.json', 'LICENSE')]
for field in ('logo', 'composerIcon'):
    file = (root / interface[field]).resolve()
    assert file.is_relative_to(root) and file.is_file()
    files.append(file)
for skill in ('daily-journal-api', 'resumo', 'topico'):
    base = root / 'skills' / skill
    assert (base / 'SKILL.md').is_file()
    files.extend(p for p in base.rglob('*') if p.is_file() and not p.name.startswith('.'))
output = root / 'dist' / f"daily-journal-openai-{manifest['version']}.zip"
output.parent.mkdir(exist_ok=True)
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for file in sorted(set(files)):
        archive.write(file, file.relative_to(root))
print(output)
