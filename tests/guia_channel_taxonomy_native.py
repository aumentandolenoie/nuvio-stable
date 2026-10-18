#!/usr/bin/env python3
"""Compile and execute the real channel classifier using representative sources."""
from pathlib import Path
import subprocess, tempfile
s=Path("src/guia.c").read_text()
helper=s[s.index("static int contemSemCaixa("):s.index("static const char *categoriaPorNome(")]
classifier=s[s.index("static const char *categoriaCanal("):s.index("static int sCatDe(")]
tests=[
 ("Sky Sport F1 HD","Esportes","TvVoo Italia","Formula 1"),
 ("F1 TV","Sport","TvVoo Italia","Formula 1"),
 ("F1","F1","StreamViX Eventi","Formula 1"),
 ("MotoGP Live","Sport","StreamViX","MotoGP"),
 ("Sky Sport MotoGP","Sport","TvVoo","MotoGP"),
 ("Tennis Channel","Sport","TvVoo","Tennis"),
 ("Serie A Live","Serie A","StreamViX","Serie A"),
 ("Sky Cinema Uno","Sky","StreamViX","Canali cinema e serie"),
 ("Film - Serie TV","Film - Serie TV","TvVoo","Canali cinema e serie"),
 ("Rai Sport 1","Rai","TvVoo","Canali sportivi"),
 ("Formula 1","Sport","StreamViX","Formula 1"),
 ("Basket NBA","Sport","TvVoo","Basket"),
]
def esc(x):return '"'+x.replace("\\","\\\\").replace('"','\\"')+'"'
main="int main(void) {\n"
for n,g,c,want in tests:
 main+=f"  if(strcmp(categoriaCanal({esc(n)},{esc(g)},{esc(c)}),{esc(want)})) return __LINE__;\n"
main+="  return 0;\n}\n"
src="#include <string.h>\n#include <strings.h>\n"+helper+"\n"+classifier+"\n"+main
with tempfile.TemporaryDirectory() as td:
 p=Path(td); (p/"test.c").write_text(src)
 subprocess.run(["cc","-std=c11","-Wall","-Wextra","-Werror",str(p/"test.c"),"-o",str(p/"test")],check=True)
 subprocess.run([str(p/"test")],check=True)
print(f"PASS: actual C channel classifier, {len(tests)} mixed TVVoo/StreamViX cases")
