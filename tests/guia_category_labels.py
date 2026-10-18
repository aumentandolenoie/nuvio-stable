#!/usr/bin/env python3
"""The guide drawer must show identical names regardless of focus."""
from pathlib import Path
s=Path("src/guia.c").read_text()
assert 'tn = foc ? txt_linha_corta(TXT_BODY, guideMenuName(i)' in s
assert ': txt_linha_corta(TXT_BODY, guideMenuName(i)' in s
assert ': txt_linha_corta(TXT_BODY, linhaNome(i)' not in s
assert 'guideLevel ? guideGroups[guideGroup]' in s
assert 'guideLevel ? i18n("OK seleziona' in s
print("PASS: focused/unfocused categories render the same hierarchical label")
