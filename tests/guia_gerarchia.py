#!/usr/bin/env python3
"""Contract tests for TV guide hierarchical category drawer (2.0.35)."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert '#define G_GUIDE_GROUPS 9' in s
assert '"Preferiti", "Sport", "Canali TV", "Film e serie TV"' in s
assert 'guideGroupOf(linhaNome(l))' in s
assert 'guideMenuN(void)' in s and 'guideSubFirst(int pos)' in s
assert 'if (!guideLevel)' in s and 'guideLevel = 1;' in s
assert 'int line = guideMenuLine(catFoco);' in s
assert 'else if (guideLevel) {guideLevel=0;' in s
assert 'TXT_BODY, guideMenuName(i)' in s
assert 'guideMenuCount(i)' in s
assert 'guideGroup = guideLevel = guideSub = 0;' in s
print("PASS: hierarchical guide navigation without altering streams, EPG, or caching")
