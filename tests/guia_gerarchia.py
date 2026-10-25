#!/usr/bin/env python3
"""Guide groups now select the addon directly, without genre nesting."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert '#define G_GUIDE_GROUPS 2' in s
assert '{ "Tvvoo", "Streamvix" }' in s
assert 'int first = guideSubFirst(0);' in s
assert 'focoLin = first; focoCol = 0;' in s
print("PASS: two guide provider groups, direct navigation")
