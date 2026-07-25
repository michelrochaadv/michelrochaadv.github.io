# -*- coding: utf-8 -*-
"""Atualiza páginas de categoria (todos os artigos) e index.html (Publicados Hoje + carrosséis)."""
import json, re

DATE = "2026-07-25"
DATE_DISPLAY = "25/07/2026"
DATE_SHORT = "25 jul 2026"

AREAS = {
    "penal": "Penal",
    "previdenciario": "Previdenciário",
    "empresarial": "Empresarial",
    "consumidor": "Consumidor",
    "familia": "Família",
    "imobiliario": "Imobiliário",
}
# IDs dos carrosséis (família com acento!)
CAR_IDS = {
    "Penal": "car-penal",
    "Previdenciário": "car-previdenciario",
    "Empresarial": "car-empresarial",
    "Consumidor": "car-consumidor",
    "Família": "car-família",
    "Imobiliário": "car-imobiliario",
}

with open("artigos/index.json", encoding="utf-8") as f:
    index = json.load(f)

# ---------- 1. Páginas de categoria (novo layout) ----------
import subprocess
subprocess.run(["python3", "gera_categorias.py"], check=True)

# ---------- 2. index.html ----------
with open("index.html", encoding="utf-8") as f:
    html = f.read()

novos = [a for a in index if a["date"] == DATE]
print(f"Artigos do dia: {len(novos)}")
assert len(novos) == 6, "esperava 6 artigos do dia"

def home_card(a):
    return (
        f'    <div class="art-card" onclick="window.location.href=\'artigo/{a["slug"]}.html\'" style="cursor:pointer">\n'
        f'      <div class="art-tag">{a["tag"]}</div>\n'
        f'      <div class="art-title">{a["titulo"]}</div>\n'
        f'      <div class="art-excerpt">{a["subtitulo"]}.</div>\n'
        f'      <div class="art-meta"><span>{DATE_SHORT}</span><span>{a["tempo_leitura"]}</span></div>\n'
        f'      <span class="art-more">Ler artigo \u2192</span>\n'
        f'    </div>'
    )

g1 = "\n".join(home_card(a) for a in novos[:3])
g2 = "\n".join(home_card(a) for a in novos[3:])
secao = (
    '<hr class="divider">\n'
    '<section class="section">\n'
    '  <div class="sec-header">\n'
    f'    <div class="sec-title">Publicados Hoje \u2014 {DATE_DISPLAY}</div>\n'
    '    <a href="categoria/consumidor.html" class="sec-link">Ver todos \u2192</a>\n'
    '  </div>\n'
    f'  <div class="grid3">\n{g1}\n  </div>\n'
    f'  <div class="grid3" style="margin-top:1.25rem">\n{g2}\n  </div>\n'
    '</section>\n\n'
)

html, n = re.subn(
    r'<hr class="divider">\s*<section class="section">\s*<div class="sec-header">\s*<div class="sec-title">Publicados Hoje.*?</section>\s*(?=<div class="captacao")',
    lambda m: secao,
    html, count=1, flags=re.DOTALL,
)
if n != 1:
    raise SystemExit("ERRO: seção Publicados Hoje não encontrada")
print("\u2713 Publicados Hoje substituído")

# Carrosséis: prepend cards novos das áreas afetadas
def car_card(a):
    return (
        f'<div class="car-card" onclick="window.location.href=\'artigo/{a["slug"]}.html\'">'
        f'<div class="art-tag">{a["tag"]}</div>'
        f'<div class="art-title">{a["titulo"]}</div>'
        f'<div class="art-excerpt">{a["subtitulo"]}</div>'
        f'<div class="art-meta"><span>{a["date_display"]}</span><span>{a["tempo_leitura"]}</span></div>'
        f'<span class="art-more">Ler artigo \u2192</span></div>'
    )

from collections import defaultdict
por_area = defaultdict(list)
for a in novos:
    por_area[a["area"]].append(a)

for area, arts in por_area.items():
    uid = CAR_IDS[area]
    cards = "".join(car_card(a) for a in arts)
    marker = f'id="{uid}">'
    if marker not in html:
        raise SystemExit(f"ERRO: carrossel {uid} não encontrado")
    html = html.replace(marker, marker + cards, 1)
    print(f"\u2713 {uid} +{len(arts)} cards")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\u2713 index.html atualizado")
