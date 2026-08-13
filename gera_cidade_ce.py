# -*- coding: utf-8 -*-
"""Gera páginas /cidade/{slug}.html para as cidades do Ceará, no mesmo padrão das páginas da Bahia."""
import urllib.parse

BASE = "https://michelrocha.adv.br"
WA = "5571981758097"

CIDADES_CE = [
    ("fortaleza", "Fortaleza",
     "Fortaleza, capital do Ceará e uma das maiores cidades do Brasil, conta com o suporte jurídico do escritório Michel Rocha Advocacia e Consultoria para moradores que precisam de orientação especializada com toda a praticidade do atendimento online.",
     ["Para moradores de Fortaleza, o atendimento online do escritório Michel Rocha significa acesso direto a orientação jurídica especializada sem enfrentar deslocamentos e filas. Com os processos tramitando pelos sistemas eletrônicos da Justiça, a atuação na capital cearense acontece com a mesma agilidade e qualidade do atendimento presencial, em todas as áreas do direito.",
      "Na área previdenciária, a capital concentra grande volume de segurados e de demandas contra o INSS: benefícios negados, aposentadorias com valores incorretos, auxílios cessados e pedidos parados nas agências. Cada caso exige análise individualizada do histórico contributivo e da documentação, trabalho que é feito integralmente à distância.",
      "Nas questões criminais, a defesa técnica alcança flagrantes, audiências de custódia e processos nas varas criminais da comarca de Fortaleza. Já na área de família, divórcios, guarda de filhos, pensão alimentícia e inventários são conduzidos de forma prática, com orientação clara desde o primeiro contato pelo WhatsApp."]),
    ("caucaia", "Caucaia",
     "Caucaia, segundo município mais populoso do Ceará e parte da região metropolitana de Fortaleza, conta com o suporte jurídico do escritório Michel Rocha Advocacia e Consultoria, com atendimento online que elimina deslocamentos até a capital.",
     ["Moradores de Caucaia encontram no atendimento online do escritório Michel Rocha uma forma prática de resolver questões jurídicas sem depender de idas a escritórios na capital. A atuação cobre todas as áreas do direito, com acompanhamento processual pelos sistemas eletrônicos da Justiça e comunicação direta pelo WhatsApp.",
      "No campo previdenciário, trabalhadores urbanos da região metropolitana acumulam históricos contributivos variados, e é comum o INSS negar benefícios ou pagar valores menores que o devido. A análise cuidadosa de vínculos, contribuições e documentos é o que permite corrigir essas situações, tudo sem necessidade de deslocamento.",
      "Na esfera criminal, a proximidade com os fóruns da capital torna a resposta rápida ainda mais importante em flagrantes e audiências de custódia. Nas questões de família, como divórcio, guarda e pensão, a orientação adequada desde o início evita desgastes e encaminha soluções mais rápidas para quem vive em Caucaia."]),
    ("juazeiro-do-norte", "Juazeiro do Norte",
     "Juazeiro do Norte, coração do Cariri e principal polo do interior cearense, conta com o suporte jurídico do escritório Michel Rocha Advocacia e Consultoria, que atende moradores de toda a região com a praticidade do atendimento online.",
     ["Para quem vive em Juazeiro do Norte e em todo o Cariri, o atendimento online do escritório Michel Rocha garante orientação jurídica especializada sem a necessidade de viajar até grandes centros. Os processos são acompanhados pelos sistemas eletrônicos da Justiça, o que permite atuação ágil em todas as áreas do direito.",
      "A demanda previdenciária na região é expressiva, com segurados urbanos e rurais que enfrentam negativas do INSS, dificuldades no reconhecimento de tempo de trabalho e benefícios pagos em valor incorreto. Cada história contributiva é única e merece análise técnica detalhada, feita integralmente à distância.",
      "Na área criminal, a comarca movimentada exige defesa técnica presente desde o flagrante e a audiência de custódia. Em família, divórcios, guarda de filhos e inventários são conduzidos com mínimo deslocamento, com orientação clara para que as famílias de Juazeiro do Norte tomem decisões seguras."]),
    ("maracanau", "Maracanaú",
     "Maracanaú, polo industrial da região metropolitana de Fortaleza e um dos municípios mais populosos do Ceará, conta com o suporte jurídico do escritório Michel Rocha Advocacia e Consultoria, com atendimento totalmente online.",
     ["Moradores de Maracanaú podem resolver questões jurídicas com agilidade por meio do atendimento online do escritório Michel Rocha, que atua em todas as áreas do direito com acompanhamento pelos sistemas eletrônicos da Justiça e contato direto pelo WhatsApp, sem burocracia e sem deslocamentos.",
      "O perfil industrial do município gera demandas previdenciárias específicas, como aposentadoria especial por exposição a agentes nocivos e benefícios por incapacidade decorrentes de acidentes e doenças ocupacionais. São casos que dependem de documentação técnica bem organizada e de análise minuciosa do histórico de trabalho.",
      "Nas questões criminais, a defesa técnica atua desde o primeiro momento, em flagrantes, custódias e processos em andamento. Já nas demandas de família e de consumo, a orientação especializada desde o início do problema evita prejuízos e encaminha soluções mais rápidas para as famílias de Maracanaú."]),
]

AREAS_HUB = [
    ("../criminalista/{slug}.html", "✦ Defesa Criminal", "Flagrantes, custódias e atendimento urgente"),
    ("../previdenciario/{slug}.html", "✦ Previdenciário", "INSS, benefícios negados e aposentadorias"),
    ("../categoria/familia.html", "✦ Família e Divórcio", "Divórcio, guarda e pensão alimentícia"),
    ("../categoria/consumidor.html", "✦ Consumidor", "Planos de saúde, bancos e indenizações"),
    ("../categoria/empresarial.html", "✦ Empresarial", "Contratos e assessoria para empresas"),
    ("../categoria/imobiliario.html", "✦ Imobiliário", "Locação, despejo e construtoras"),
]

SIDEBAR_AREAS = ["Previdenciário", "Direito Penal", "Família e Divórcio", "Consumidor", "Empresarial", "Imobiliário"]

def gerar():
    src = open("cidade/jequie.html", encoding="utf-8").read()
    header = src.split("<body>")[1].split("</header>")[0] + "</header>"
    tail = '<div class="float-wrap">' + src.split('<div class="float-wrap">')[1]
    ga_block = "<!-- Google tag (gtag.js) -->" + src.split("<!-- Google tag (gtag.js) -->")[1].split("</head>")[0]

    P = lambda t: f'<p style="font-size:14px;color:var(--text);line-height:1.9;margin-bottom:1.25rem">{t}</p>'

    for slug, nome, intro, paras in CIDADES_CE:
        desc = f"Advogado em {nome} CE. Michel Rocha atua em direito previdenciário, penal, consumidor e família com atendimento online. Consulte agora."
        wa_msg = urllib.parse.quote(f"Olá, Dr. Michel! Preciso de um advogado em {nome} e gostaria de conversar sobre meu caso.")

        sidebar = "".join(
            f'<div style="display:flex;align-items:center;gap:10px;font-size:12px;color:var(--muted)"><span style="color:var(--gold)">✦</span> {a}</div>'
            for a in SIDEBAR_AREAS
        )
        hub_cards = "".join(
            f'<a href="{href.format(slug=slug)}" style="display:block;background:var(--card);border:1px solid rgba(255,255,255,0.06);padding:1.25rem;text-decoration:none">\n'
            f'   <div style="color:var(--gold);font-size:13px;margin-bottom:6px">{titulo}</div>\n'
            f'   <div style="color:var(--muted);font-size:12px;line-height:1.6">{sub}</div>\n </a>'
            for href, titulo, sub in AREAS_HUB
        )

        head = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advogado em {nome}, CE | Michel Rocha Advocacia</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/cidade/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"Michel Rocha Advocacia e Consultoria","url":"{BASE}","telephone":"+{WA}","areaServed":"{nome}, CE","description":"{desc}"}}
</script>
{ga_block}
<link rel="icon" type="image/png" href="../favicon.png">
</head>
<body>
'''

        body = f'''<main>

<div style="max-width:1000px;margin:0 auto;padding:4rem 2rem">
  <div style="margin-bottom:3rem">
    <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1rem;display:flex;align-items:center;gap:14px">
      <span style="width:28px;height:1px;background:var(--gold);display:inline-block"></span>
      Atuação Local
    </div>
    <h1 style="font-family:var(--serif);font-size:2.8rem;color:var(--cream);font-weight:300;line-height:1.15;margin-bottom:1rem">Advogado em {nome}, CE</h1>
    <p style="font-size:14px;color:var(--muted);line-height:1.9;max-width:680px">{intro}</p>
  </div>

  <div style="display:grid;grid-template-columns:2fr 1fr;gap:3rem;align-items:start">
    <div>{''.join(P(t) for t in paras)}</div>
    <div style="position:sticky;top:90px">
      <div style="background:var(--dark);border:1px solid rgba(201,168,76,0.2);padding:2rem">
        <div style="font-size:9px;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:1.25rem">Áreas de Atuação</div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:2rem">{sidebar}</div>
        <a href="https://wa.me/{WA}?text={wa_msg}" target="_blank" class="btn-whatsapp" style="display:flex;width:100%;justify-content:center;gap:10px">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          Falar com Advogado
        </a>
        <p style="font-size:10px;color:var(--muted);text-align:center;margin-top:1rem;line-height:1.6">Atendimento online para {nome} e todo o Brasil</p>
      </div>
    </div>
  </div>
</div>

<div style="max-width:1000px;margin:0 auto;padding:0 2rem 3.5rem">
  <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1.1rem;display:flex;align-items:center;gap:14px"><span style="width:28px;height:1px;background:var(--gold);display:inline-block"></span>Atuação em {nome} por área</div>
  <div class="grid3" style="gap:1rem">{hub_cards}</div>
</div>
</main>

'''
        open(f"cidade/{slug}.html", "w", encoding="utf-8").write(head + header + body + tail)
        print(f"✓ cidade/{slug}.html")

if __name__ == "__main__":
    gerar()
