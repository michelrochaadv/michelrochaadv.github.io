# -*- coding: utf-8 -*-
"""Atualiza páginas de categoria (todos os artigos) e index.html (Publicados Hoje + carrosséis).
Funciona para qualquer quantidade de artigos do dia (1 a N), não apenas lotes de 6.
Pode ser rodado mais de uma vez no mesmo dia (ex: publicar 1 de manha e mais 2 a
tarde) sem duplicar cards ja inseridos."""
import json, re
from datetime import date
from collections import defaultdict

# ---------- ÚNICA coisa a editar a cada publicação ----------
DATE = "2026-08-11"  # <- editar aqui a cada publicacao  # AAAA-MM-DD da publicação de hoje
# DATE_DISPLAY e DATE_SHORT são derivados automaticamente abaixo, não editar.

_MESES_PT = ["", "jan", "fev", "mar", "abr", "mai", "jun",
             "jul", "ago", "set", "out", "nov", "dez"]
_d = date.fromisoformat(DATE)
DATE_DISPLAY = _d.strftime("%d/%m/%Y")
DATE_SHORT = f"{_d.day:02d} {_MESES_PT[_d.month]} {_d.year}"

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
# Slug de categoria por área, para o link dinâmico "Ver todos" de Publicados Hoje
CAT_SLUG = {
    "Penal": "penal",
    "Previdenciário": "previdenciario",
    "Empresarial": "empresarial",
    "Consumidor": "consumidor",
    "Família": "familia",
    "Imobiliário": "imobiliario",
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
if len(novos) == 0:
    raise SystemExit(f"ERRO: nenhum artigo com date={DATE} no index.json. Confira a data.")
if len(novos) > 12:
    print(f"AVISO: {len(novos)} artigos no mesmo dia e incomum, confira se e intencional.")

def home_card(a):
    return (
        '    <div class="art-card" onclick="window.location.href=\'artigo/' + a["slug"] + '.html\'" style="cursor:pointer">\n'
        '      <div class="art-tag">' + a["tag"] + '</div>\n'
        '      <div class="art-title">' + a["titulo"] + '</div>\n'
        '      <div class="art-excerpt">' + a["subtitulo"] + '.</div>\n'
        '      <div class="art-meta"><span>' + DATE_SHORT + '</span><span>' + a["tempo_leitura"] + '</span></div>\n'
        '      <span class="art-more">Ler artigo \u2192</span>\n'
        '    </div>'
    )

# Grid único: .grid3 e CSS grid de verdade (repeat(3,1fr)) e quebra linha
# sozinho, entao funciona igual para 1, 3, 6 ou 10 artigos no mesmo dia.
cards_html = "\n".join(home_card(a) for a in novos)

# Link "Ver todos" de Publicados Hoje aponta para a categoria com mais
# artigos publicados no dia (empate: primeira na ordem de AREAS).
contagem_area = defaultdict(int)
for a in novos:
    contagem_area[a["area"]] += 1
ordem_areas = list(AREAS.values())
area_principal = max(ordem_areas, key=lambda ar: (contagem_area[ar], -ordem_areas.index(ar)))
link_ver_todos = "categoria/" + CAT_SLUG[area_principal] + ".html"

secao = (
    '<hr class="divider">\n'
    '<section class="section">\n'
    '  <div class="sec-header">\n'
    '    <div class="sec-title">Publicados Hoje \u2014 ' + DATE_DISPLAY + '</div>\n'
    '    <a href="' + link_ver_todos + '" class="sec-link">Ver todos \u2192</a>\n'
    '  </div>\n'
    '  <div class="grid3">\n' + cards_html + '\n  </div>\n'
    '</section>\n\n'
)

html, n = re.subn(
    r'<hr class="divider">\s*<section class="section">\s*<div class="sec-header">\s*<div class="sec-title">Publicados Hoje.*?</section>\s*(?=<div class="captacao")',
    lambda m: secao,
    html, count=1, flags=re.DOTALL,
)
if n != 1:
    raise SystemExit("ERRO: secao Publicados Hoje nao encontrada")
print("\u2713 Publicados Hoje substituido")

# Carrosseis: prepend cards novos das areas afetadas
def car_card(a):
    return (
        '<div class="car-card" onclick="window.location.href=\'artigo/' + a["slug"] + '.html\'">'
        '<div class="art-tag">' + a["tag"] + '</div>'
        '<div class="art-title">' + a["titulo"] + '</div>'
        '<div class="art-excerpt">' + a["subtitulo"] + '</div>'
        '<div class="art-meta"><span>' + a["date_display"] + '</span><span>' + a["tempo_leitura"] + '</span></div>'
        '<span class="art-more">Ler artigo \u2192</span></div>'
    )

por_area = defaultdict(list)
for a in novos:
    por_area[a["area"]].append(a)

for area, arts in por_area.items():
    uid = CAR_IDS[area]
    marker = 'id="' + uid + '">'
    pos = html.find(marker)
    if pos == -1:
        raise SystemExit("ERRO: carrossel " + uid + " nao encontrado")
    # Escopo da checagem de duplicidade: so dentro deste carrossel
    # especifico (do marker ate o proximo "id=\"car-" ou fim do arquivo),
    # nunca a pagina inteira -- a secao Publicados Hoje usa o mesmo
    # formato de link e geraria falso positivo se checassemos tudo.
    fim_escopo = html.find('id="car-', pos + len(marker))
    if fim_escopo == -1:
        fim_escopo = len(html)
    escopo_atual = html[pos:fim_escopo]
    arts_novos = [a for a in arts if ("artigo/" + a["slug"] + ".html'") not in escopo_atual]
    puladas = len(arts) - len(arts_novos)
    cards = "".join(car_card(a) for a in arts_novos)
    if cards:
        html = html.replace(marker, marker + cards, 1)
    msg = "\u2713 " + uid + " +" + str(len(arts_novos)) + " cards"
    if puladas:
        msg += " (" + str(puladas) + " ja existiam, puladas)"
    print(msg)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\u2713 index.html atualizado")
