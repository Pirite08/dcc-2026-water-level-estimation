"""Check public links, notebook structure and accidental private-file inclusion.

This check does not run model training or verify recorded experiment metrics.
Run from any directory: python tools/validate_repository.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.py', '.json', '.csv', '.cff', '.yaml', '.yml', '.ipynb', '.svg'}
FORBIDDEN_SUFFIXES = {'.pt', '.pth', '.parquet', '.safetensors', '.zip', '.tar'}
TOKEN_PATTERNS = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b'),
    'google-api-key': re.compile(r'\bAIza[A-Za-z0-9_-]{30,}\b'),
}


def check() -> dict:
    errors: list[str] = []
    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts]
    links = 0
    notebooks = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f'raw-data-or-model-file: {rel}')
        if path.stat().st_size > 25 * 1024 * 1024:
            errors.append(f'oversize-file: {rel}')
        if path.name.startswith('.env') or path.name.startswith('credentials'):
            errors.append(f'private-config-file: {rel}')
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding='utf-8-sig')
        for label, pattern in TOKEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f'{label}: {rel}')
        if path.suffix == '.ipynb':
            notebooks += 1
            try:
                nb = json.loads(text)
                assert nb['nbformat'] == 4 and isinstance(nb['cells'], list)
                assert nb['cells'] and nb['cells'][0]['cell_type'] == 'markdown'
                for cell in nb['cells']:
                    assert cell['cell_type'] in {'markdown', 'code', 'raw'}
                    assert isinstance(cell['source'], (str, list))
                    assert not cell.get('attachments'), 'embedded markdown attachment'
                    for output in cell.get('outputs', []):
                        assert all(k == 'text/plain' for k in output.get('data', {})), 'non-text embedded output'
            except (ValueError, KeyError, AssertionError, TypeError) as exc:
                errors.append(f'invalid-public-notebook: {rel}: {exc}')
        if path.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^\n)]*)\)', text):
                target = target.strip().strip('<>')
                if not target or target.startswith('#') or urlsplit(target).scheme:
                    continue
                target = unquote(target.split('#', 1)[0])
                links += 1
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.exists():
                    errors.append(f'broken-local-link: {rel} -> {target}')
    return {'files': len(files), 'notebooks': notebooks, 'local_links': links, 'errors': errors, 'passed': not errors}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['passed'] else 1)
