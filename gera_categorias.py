# -*- coding: utf-8 -*-
"""Regenera as 6 páginas de categoria no novo layout (hero + destaque + grid + captação)."""
import json, urllib.parse
from datetime import date

BASE = "https://michelrochaadv.github.io"
WA = "5571981758097"

AREAS = {
 "penal": {"nome": "Penal", "titulo": "Direito Penal",
  "desc": "Defesa criminal em todas as fases: flagrantes, audiências de custódia, execução penal e Tribunal do Júri. Atendimento urgente a familiares de pessoas presas.",
  "btn": "Falar com um Criminalista", "pergunta": "Um familiar foi preso ou você responde a processo?",
  "wa": "Olá, Dr. Michel! Preciso de um advogado criminalista, é urgente.",
  "seo": "Artigos sobre Direito Penal: flagrantes, audiências de custódia, execução penal e defesa criminal. Atendimento urgente pelo WhatsApp."},
 "previdenciario": {"nome": "Previdenciário", "titulo": "Direito Previdenciário",
  "desc": "Benefícios do INSS: concessões negadas, cortes indevidos, aposentadorias, auxílios e BPC. Estratégia administrativa e judicial para garantir a sua renda.",
  "btn": "Falar com um Advogado", "pergunta": "O INSS negou ou cortou o seu benefício?",
  "wa": "Olá, Dr. Michel! Preciso de ajuda com um benefício do INSS.",
  "seo": "Artigos sobre Direito Previdenciário: benefícios negados, cortes do INSS, aposentadorias e BPC. Saiba como agir e fale com um advogado."},
 "empresarial": {"nome": "Empresarial", "titulo": "Direito Empresarial",
  "desc": "Assessoria jurídica para empresas: contratos, cobranças, bloqueios judiciais e proteção do negócio. Prevenção e defesa para quem empreende.",
  "btn": "Falar com um Advogado", "pergunta": "Sua empresa enfrenta um problema jurídico?",
  "wa": "Olá, Dr. Michel! Preciso de assessoria jurídica para minha empresa.",
  "seo": "Artigos sobre Direito Empresarial: contratos, cobranças, bloqueios judiciais e assessoria para empresas. Fale com um advogado."},
 "consumidor": {"nome": "Consumidor", "titulo": "Direito do Consumidor",
  "desc": "Defesa do consumidor contra planos de saúde, bancos, concessionárias e companhias aéreas. Negativas abusivas, cobranças indevidas e indenizações.",
  "btn": "Falar com um Advogado", "pergunta": "Teve um direito negado por plano de saúde, banco ou empresa?",
  "wa": "Olá, Dr. Michel! Tive um problema como consumidor e preciso de orientação.",
  "seo": "Artigos sobre Direito do Consumidor: planos de saúde, cobranças indevidas, companhias aéreas e indenizações. Fale com um advogado."},
 "familia": {"nome": "Família", "titulo": "Família e Divórcio",
  "desc": "Divórcio, guarda, convivência com os filhos e pensão alimentícia. Condução técnica e humana para os momentos mais delicados da vida familiar.",
  "btn": "Falar com um Advogado", "pergunta": "Enfrentando um divórcio ou um conflito familiar?",
  "wa": "Olá, Dr. Michel! Preciso de orientação em uma questão de família.",
  "seo": "Artigos sobre Direito de Família: divórcio, guarda dos filhos, convivência e pensão alimentícia. Saiba como agir e fale com um advogado."},
 "imobiliario": {"nome": "Imobiliário", "titulo": "Direito Imobiliário",
  "desc": "Compra e venda, locação, despejo, usucapião e problemas com construtoras. Proteção jurídica para o seu patrimônio imobiliário.",
  "btn": "Falar com um Advogado", "pergunta": "Um problema com imóvel, aluguel ou construtora?",
  "wa": "Olá, Dr. Michel! Preciso de orientação em uma questão imobiliária.",
  "seo": "Artigos sobre Direito Imobiliário: locação, despejo, imóvel na planta e problemas com construtoras. Saiba como agir e fale com um advogado."},
}

CIDADES_LINK = [("salvador","Salvador"),("feira-de-santana","Feira de Santana"),("camacari","Camaçari"),("vitoria-da-conquista","Vitória da Conquista")]

def gerar():
    index = json.load(open("artigos/index.json", encoding="utf-8"))
    src = open("cidade/jequie.html", encoding="utf-8").read()
    header = src.split("<body>")[1].split("</header>")[0] + "</header>"
    tail = '<div class="float-wrap">' + src.split('<div class="float-wrap">')[1]
    hoje = date.today().strftime("%d/%m/%Y")

    for slug, A in AREAS.items():
        arts = [a for a in index if a["area"] == A["nome"]]
        destaque, resto = arts[0], arts[1:]
        wa_url = f"https://wa.me/{WA}?text={urllib.parse.quote(A['wa'])}"

        def card(a):
            return f'''    <div class="art-card" onclick="window.location.href='../artigo/{a["slug"]}.html'" style="cursor:pointer">
      <div class="art-tag">{a["tag"]}</div>
      <div class="art-title">{a["titulo"]}</div>
      <div class="art-excerpt">{a["subtitulo"]}</div>
      <div class="art-meta"><span>{a["date_display"]}</span><span>{a["tempo_leitura"]}</span></div>
      <span class="art-more">Ler artigo \u2192</span>
    </div>'''
        visiveis, ocultos = resto[:9], resto[9:]
        cards = "\n".join(card(a) for a in visiveis)
        extra = ""
        if ocultos:
            cards_ocultos = "\n".join(card(a) for a in ocultos)
            extra = f'''
  <div id="mais-artigos" style="display:none;margin-top:1.25rem" class="grid3">
{cards_ocultos}
  </div>
  <div style="text-align:center;margin-top:1.75rem">
    <a href="#" id="btn-mais" onclick="document.getElementById('mais-artigos').style.display='grid';this.parentElement.style.display='none';return false" style="color:var(--gold);font-size:13px;text-decoration:none;border:1px solid rgba(201,168,76,0.4);padding:12px 28px;display:inline-block">Ver todos os {len(arts)} artigos \u2193</a>
  </div>'''

        cidades_html = ""
        if slug == "penal":
            links = " \u00b7 ".join(f'<a href="../criminalista/{cs}.html" style="color:var(--gold);text-decoration:none">{cn}</a>' for cs, cn in CIDADES_LINK)
            cidades_html = f'''<div style="font-size:12px;color:var(--muted)">Atendimento criminal em:<br><span style="line-height:2">{links} \u00b7 <a href="../criminalista/jequie.html" style="color:var(--gold);text-decoration:none">e mais 10 cidades</a></span></div>'''
        else:
            cidades_html = '<div style="font-size:12px;color:var(--muted);line-height:1.8">Atendimento em Salvador,<br>em toda a Bahia e online<br>para todo o Brasil</div>'

        body = f'''
<div style="max-width:1080px;margin:0 auto;padding:4rem 2rem">

  <div style="display:grid;grid-template-columns:1.7fr 1fr;gap:2.5rem;align-items:start;margin-bottom:3.5rem">
    <div>
      <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1rem;display:flex;align-items:center;gap:14px">
        <span style="width:28px;height:1px;background:var(--gold);display:inline-block"></span>
        \u00c1rea de Atua\u00e7\u00e3o
      </div>
      <h1 style="font-family:var(--serif);font-size:3rem;color:var(--cream);font-weight:300;line-height:1.1;margin-bottom:1rem">{A["titulo"]}</h1>
      <p style="font-size:14px;color:var(--muted);line-height:1.9;max-width:620px;margin-bottom:1rem">{A["desc"]}</p>
      <div style="font-size:12px;color:var(--muted)">{len(arts)} artigos publicados &nbsp;\u00b7&nbsp; Atualizado em {hoje}</div>
    </div>
    <div style="padding-top:2.2rem">
      <a href="{wa_url}" target="_blank" class="btn-whatsapp" style="display:flex;justify-content:center;gap:10px;width:100%">{A["btn"]}</a>
      <p style="font-size:11px;color:var(--muted);text-align:center;margin-top:0.8rem">Atendimento pelo WhatsApp</p>
    </div>
  </div>

  <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1rem">Em Destaque</div>
  <div onclick="window.location.href='../artigo/{destaque["slug"]}.html'" style="cursor:pointer;background:var(--dark);border:1px solid rgba(201,168,76,0.25);border-left:5px solid var(--gold);padding:2rem 2.5rem;margin-bottom:3rem">
    <div class="art-tag">{destaque["tag"]} \u00b7 NOVO</div>
    <div style="font-family:var(--serif);font-size:1.9rem;color:var(--cream);font-weight:400;margin:0.6rem 0">{destaque["titulo"]}</div>
    <div style="font-size:14px;color:var(--text);line-height:1.8;margin-bottom:1rem">{destaque["subtitulo"]}</div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:12px;color:var(--muted)">{destaque["date_display"]} \u00b7 {destaque["tempo_leitura"]} de leitura</span>
      <span class="art-more">Ler artigo \u2192</span>
    </div>
  </div>

  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1rem">
    <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase">Todos os Artigos</div>
    <span style="font-size:12px;color:var(--muted)">{len(arts)} artigos</span>
  </div>
  <div class="grid3">
{cards}
  </div>
{extra}

  <div style="background:#100e0a;border:1px solid var(--gold);padding:2.5rem;margin-top:3.5rem;display:grid;grid-template-columns:2fr 1fr;gap:2rem;align-items:center">
    <div>
      <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:0.8rem">{("Precisa de defesa criminal?" if slug=="penal" else "Precisa de um advogado?")}</div>
      <div style="font-family:var(--serif);font-size:1.9rem;color:var(--cream);font-weight:400;margin-bottom:0.8rem">{A["pergunta"]}</div>
      <p style="font-size:13.5px;color:var(--text);line-height:1.8;margin-bottom:1.4rem">Cada caso tem suas particularidades. Fale agora e receba orienta\u00e7\u00e3o para a sua situa\u00e7\u00e3o.</p>
      <a href="{wa_url}" target="_blank" class="btn-whatsapp" style="display:inline-flex;gap:10px">Falar Agora no WhatsApp</a>
    </div>
    {cidades_html}
  </div>

</div>

'''
        head = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{A["titulo"]} | Artigos e Orienta\u00e7\u00e3o | Michel Rocha Advocacia</title>
<meta name="description" content="{A["seo"]}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/categoria/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7466469886799127" crossorigin="anonymous"></script>
</head>
<body>
'''
        open(f"categoria/{slug}.html", "w", encoding="utf-8").write(head + header + body + tail)
        print(f"\u2713 categoria/{slug}.html \u2192 destaque + {len(resto)} no grid")

if __name__ == "__main__":
    gerar()
