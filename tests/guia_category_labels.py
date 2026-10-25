#!/usr/bin/env python3
"""The guide displays only the requested provider categories."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert 'static const char *guideGroups[G_GUIDE_GROUPS] = { "Tvvoo", "Streamvix" };' in s
assert 'guideMenuName(i)' in s
print("PASS: guide provider labels")
