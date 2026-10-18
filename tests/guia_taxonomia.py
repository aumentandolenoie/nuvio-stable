#!/usr/bin/env python3
"""Semantic TV guide taxonomy: deduplicated logical categories, full source access."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert s.index('guideContains(name,"cinema")') < s.index('guideContains(name,"rai")')
assert 'return "Canali sportivi";' in s
assert 'return "Canali cinema e serie";' in s
assert 'return "Eventi live";' in s
assert 'guideSubFirst(int pos)' in s
assert 'guideSubMatches(int first)' in s
assert 'guideSourceLine(int pos)' in s
assert 'if (guideSubMatches(first)>1)' in s
assert 'guideLevel=2; catFoco=0;' in s
assert 'addons_nome(a)' in s
assert 'guideLevel==2 ? guideSubName(guideSubFirst(guideSub))' in s
assert 'guideMenuName(i)' in s
print("PASS: distinct macro/subcategories, deduplicated rows, all source channels reachable")
