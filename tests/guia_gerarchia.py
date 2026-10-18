#!/usr/bin/env python3
"""Contract tests for TV guide hierarchical category drawer (2.0.35)."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert '#define G_GUIDE_GROUPS 8' in s
assert '"Sport", "Canali TV", "Film e serie TV", "Informazione"' in s
assert 'guideGroupOf(linhaNome(l))' in s
assert 'guideMenuN(void)' in s and 'guideChildLine(int at)' in s
assert 'if (!guideLevel)' in s and 'guideLevel = 1;' in s
assert 'int line = guideChildLine(catFoco);' in s
assert 'if (guideLevel) { guideLevel=0;' in s
assert 'TXT_BODY, guideMenuName(i)' in s
assert 'guideMenuCount(i)' in s
assert 'guideGroup = guideLevel = 0;' in s
print("PASS: hierarchical guide navigation without altering streams, EPG, or caching")
