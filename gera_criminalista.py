# -*- coding: utf-8 -*-
"""Gera páginas /criminalista/{cidade}.html com conteúdo variado por cidade."""
import os, re, urllib.parse

GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CP101P05NG"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());gtag('config','G-CP101P05NG');
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href*="wa.me"]'):null;if(a){gtag('event','whatsapp_click',{page_path:location.pathname});}});
</script>
"""
BASE = "https://michelrochaadv.github.io"
WA = "5571981758097"

CIDADES = [
    ("salvador", "Salvador", "capital baiana e maior centro jurídico do estado, onde se concentram as varas criminais, o Tribunal de Justiça e as principais unidades prisionais da região metropolitana"),
    ("feira-de-santana", "Feira de Santana", "segundo maior município da Bahia e principal entroncamento do estado, com intensa movimentação em suas varas criminais"),
    ("lauro-de-freitas", "Lauro de Freitas", "município da região metropolitana de Salvador, com demanda criminal crescente e proximidade dos fóruns da capital"),
    ("castro-alves", "Castro Alves", "cidade do recôncavo baiano, cujos moradores contam com atendimento criminal ágil sem precisar se deslocar até a capital"),
    ("vitoria-da-conquista", "Vitória da Conquista", "terceiro maior município da Bahia e polo do sudoeste, com comarca de grande movimento na área criminal"),
    ("ilheus", "Ilhéus", "cidade histórica da costa do cacau, onde famílias buscam defesa criminal qualificada com agilidade"),
    ("itabuna", "Itabuna", "polo comercial do sul da Bahia, com comarca movimentada e demanda constante por defesa criminal técnica"),
    ("porto-seguro", "Porto Seguro", "um dos principais destinos do extremo sul baiano, onde moradores e visitantes podem precisar de defesa criminal imediata"),
    ("jequie", "Jequié", "importante polo do sudoeste baiano, cujos moradores contam com atendimento criminal especializado à distância"),
    ("alagoinhas", "Alagoinhas", "polo do agreste baiano e entroncamento ferroviário histórico, com comarca ativa na área criminal"),
    ("barreiras", "Barreiras", "principal cidade do oeste baiano, onde a distância da capital torna o atendimento online ainda mais valioso"),
    ("santo-antonio-de-jesus", "Santo Antônio de Jesus", "centro comercial do recôncavo sul, com demanda constante por defesa criminal de qualidade"),
    ("camacari", "Camaçari", "sede do polo industrial e um dos municípios mais populosos da região metropolitana de Salvador"),
    ("simoes-filho", "Simões Filho", "município industrial da região metropolitana de Salvador, com atendimento criminal ágil e acessível"),
]

P1 = [
"Quando alguém é preso em {c}, a família entra em contagem regressiva sem saber. As primeiras 24 horas após uma prisão em flagrante concentram as decisões mais importantes de todo o processo: a lavratura do auto na delegacia, a comunicação ao juiz e a audiência de custódia, na qual se decide se a pessoa responderá ao processo presa ou em liberdade. Nesse intervalo curto, a presença de um advogado criminalista faz diferença real.",
"Uma prisão nunca avisa que vai acontecer. Em {c}, como em qualquer comarca, o período entre o flagrante e a audiência de custódia é curto e decisivo: é nele que o juiz avalia a legalidade da prisão e decide entre liberdade provisória, medidas cautelares ou prisão preventiva. Famílias que conseguem defesa técnica antes desse momento chegam à audiência com o caso preparado, e isso muda o cenário.",
"O momento mais crítico de um processo criminal costuma ser o seu início. Para quem tem um familiar detido em {c}, cada hora importa: o auto de prisão em flagrante, os depoimentos colhidos na delegacia e a audiência de custódia formam a base sobre a qual todo o processo será construído. Uma defesa presente desde a primeira hora identifica ilegalidades e prepara os argumentos que sustentam o pedido de liberdade.",
"Receber a notícia de que um parente foi preso em {c} gera desespero e dúvidas imediatas: onde ele está, o que vai acontecer, se é possível soltá-lo. A resposta a essas perguntas passa pela audiência de custódia, realizada pouco depois do flagrante, e pela qualidade da defesa apresentada nela. O que se faz ou se deixa de fazer nesse curto período acompanha o processo até o fim.",
]
P2 = [
"Na audiência de custódia, o juiz analisa se a prisão foi legal e se é necessário mantê-la. Vícios na abordagem policial, buscas sem fundada suspeita, entrada irregular em domicílio e falhas no auto de prisão são pontos que a defesa técnica pode levantar, e que passam despercebidos sem análise profissional. Além disso, documentos como comprovante de residência e de trabalho lícito, reunidos rapidamente pela família, ajudam a demonstrar os vínculos que pesam a favor da liberdade provisória.",
"A defesa criminal não se resume a comparecer a audiências. Ela começa na análise minuciosa do auto de prisão em flagrante, na verificação da legalidade da abordagem policial e na construção dos argumentos para a audiência de custódia. Comprovantes de residência fixa, de ocupação lícita e bons antecedentes, organizados a tempo pela família com orientação do advogado, são elementos concretos que o juiz considera ao decidir sobre a liberdade.",
"Cada prisão tem uma história, e é papel da defesa técnica examiná-la em detalhe: como foi a abordagem, se havia fundada suspeita, se a entrada na residência foi válida, se os direitos do preso foram respeitados na delegacia. Ilegalidades nesses pontos podem levar ao relaxamento da prisão e afetar as provas do processo. É um trabalho técnico que precisa começar imediatamente, enquanto os fatos ainda podem ser documentados.",
"Entre o flagrante e a audiência de custódia, a defesa tem um trabalho intenso a fazer: acessar o auto de prisão, conversar reservadamente com o preso, verificar a legalidade da abordagem e reunir com a família os documentos que demonstram vínculos com a cidade, trabalho e residência. É esse conjunto, apresentado tecnicamente ao juiz, que sustenta o pedido de liberdade provisória ou o relaxamento de prisões ilegais.",
]
P3 = [
"A atuação criminal do escritório abrange todas as fases: acompanhamento de flagrantes e audiências de custódia, defesa em inquéritos policiais e ações penais, pedidos de liberdade provisória e revogação de preventiva, habeas corpus, questões de execução penal como progressão de regime e monitoração eletrônica, acordos de não persecução penal e atuação no Tribunal do Júri.",
"O trabalho criminal vai do primeiro ao último ato do processo: presença em audiências de custódia, defesa durante o inquérito policial, resposta à acusação e instrução criminal, pedidos de liberdade, habeas corpus nos tribunais, acompanhamento da execução penal, incluindo progressão de regime e questões de tornozeleira eletrônica, e defesa perante o Tribunal do Júri nos crimes contra a vida.",
"O escritório atua em toda a extensão da defesa criminal: flagrantes e custódias, inquéritos e intimações policiais, ações penais em todas as fases, recursos, habeas corpus, execução penal com pedidos de progressão e defesa em incidentes de monitoração eletrônica, além de acordos de não persecução penal quando cabíveis ao caso.",
"Da delegacia ao tribunal, a defesa criminal exige atuação contínua: acompanhamento do flagrante e da audiência de custódia, estratégia durante o inquérito, defesa na ação penal, sustentações e recursos, habeas corpus, além das questões de execução penal que surgem após a condenação, como progressão de regime, livramento e monitoração eletrônica.",
]
P4 = [
"O atendimento é imediato pelo WhatsApp, inclusive para familiares que estão sabendo da prisão agora e não sabem por onde começar. Com os sistemas processuais eletrônicos, a atuação em {c} acontece com agilidade, e a orientação à família começa no primeiro contato: o que fazer, quais documentos reunir e quais os próximos passos do caso.",
"Famílias em {c} podem falar diretamente com o advogado pelo WhatsApp e receber orientação imediata sobre a situação: onde a pessoa está custodiada, o que acontece a seguir e o que a família pode providenciar desde já. O acompanhamento processual é feito pelos sistemas eletrônicos da Justiça, o que garante atuação rápida.",
"O primeiro contato pode ser feito agora mesmo pelo WhatsApp. Para famílias de {c} que acabaram de receber a notícia de uma prisão, a orientação inicial esclarece o que está acontecendo e organiza as providências urgentes, enquanto a atuação técnica no processo começa pelos sistemas eletrônicos da Justiça, sem depender de deslocamentos.",
"Em situações de prisão, esperar o horário comercial custa caro. O contato pelo WhatsApp permite que famílias de {c} recebam orientação de imediato, e o acesso do advogado aos autos pelos sistemas eletrônicos permite avaliar rapidamente a situação e agir dentro dos prazos curtos que esses casos impõem.",
]
F1 = [
"Mantenha a calma e reúna informações básicas: onde a pessoa foi detida, para qual delegacia foi levada e do que está sendo acusada. Em seguida, procure imediatamente um advogado criminalista, de preferência antes da audiência de custódia. Evite conversar sobre os fatos por telefone com o preso ou tomar decisões precipitadas por conta própria.",
"O primeiro passo é descobrir onde a pessoa está custodiada e acionar a defesa técnica o quanto antes. O advogado pode acessar o auto de prisão, conversar reservadamente com o preso e preparar a audiência de custódia. Enquanto isso, a família ajuda reunindo comprovante de residência, comprovante de trabalho e documentos pessoais.",
"Agir rápido e com orientação é o que a família pode fazer de mais importante. Localize a delegacia ou unidade em que a pessoa está, anote as informações disponíveis sobre a acusação e contate um criminalista imediatamente. Documentos que comprovem residência fixa e ocupação lícita devem ser separados desde já, pois pesam na decisão sobre a liberdade.",
"Antes de tudo, não assine nem aceite nada em nome do preso sem orientação. Identifique onde ele está, guarde toda informação sobre a ocorrência e busque defesa técnica imediatamente. A presença do advogado na audiência de custódia, com o caso já estudado, é o fator que a família consegue controlar nesse momento.",
]

HEAD = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advogado Criminalista em {nome} | Michel Rocha Advocacia</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{base}/criminalista/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<link rel="icon" type="image/png" href="../favicon.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"Michel Rocha Advocacia e Consultoria","url":"{base}","telephone":"+{wa}","areaServed":"{nome}, BA","description":"{desc}"}}
</script>
</head>
<body>
'''

DESCS = [
"Advogado criminalista em {nome}. Atendimento urgente em flagrantes, audiências de custódia e defesa criminal. Fale agora pelo WhatsApp.",
"Advogado criminalista em {nome}, BA. Defesa em flagrantes, custódias, habeas corpus e execução penal. Atendimento urgente pelo WhatsApp.",
"Familiar preso em {nome}? Advogado criminalista com atendimento urgente em flagrantes, audiências de custódia e defesa criminal.",
]

ARTIGOS_PENAIS = [
    ("preso-em-flagrante-abordagem-policial", "Preso em Flagrante em Abordagem Policial, E Agora?"),
    ("tornozeleira-eletronica-regras-e-riscos", "Tornozeleira Eletrônica, Regras, Violações e Riscos"),
    ("recebi-intimacao-policial-o-que-significa", "Recebi Intimação Policial, O Que Significa"),
    ("fui-indiciado-em-inquerito-policial-o-que-fazer", "Fui Indiciado em Inquérito Policial, O Que Fazer"),
]

# extrair header, float e footer da página de cidade existente
src = open("cidade/jequie.html", encoding="utf-8").read()
header = src.split("</header>")[0].split("<body>")[1] + "</header>"
tail = "<div class=\"float-wrap\">" + src.split('<div class="float-wrap">')[1]

os.makedirs("criminalista", exist_ok=True)

P = lambda t: f'<p style="font-size:14px;color:var(--text);line-height:1.9;margin-bottom:1.25rem">{t}</p>'
H2 = lambda t: f'<h2 style="font-family:var(--serif);font-size:1.8rem;color:var(--cream);font-weight:300;margin:2.5rem 0 1rem">{t}</h2>'

for i, (slug, nome, descr) in enumerate(CIDADES):
    desc = DESCS[i % 3].format(nome=nome)
    wa_msg = urllib.parse.quote(f"Olá, Dr. Michel! Preciso de um advogado criminalista em {nome}, é urgente.")
    intro = (f"{nome}, {descr}, conta com a atuação criminal do escritório Michel Rocha Advocacia e Consultoria, "
             f"com atendimento urgente pelo WhatsApp para casos de prisão em flagrante, audiências de custódia e defesa em processos criminais.")

    corpo = (
        P(P1[i % 4].format(c=nome)) + P(P2[(i + 1) % 4].format(c=nome)) +
        P(P3[(i + 2) % 4].format(c=nome)) + P(P4[(i + 3) % 4].format(c=nome))
    )
    familiar = P(F1[(i + i // 4) % 4]) + P(
        "Cada caso tem suas particularidades, e nenhuma orientação genérica substitui a análise do flagrante concreto. "
        "O que não muda é a regra de ouro: quanto antes a defesa técnica entra no caso, maiores as possibilidades de proteger a liberdade e os direitos do preso."
    )

    links = "".join(
        f'<li style="margin-bottom:10px"><a href="../artigo/{s}.html" style="color:var(--gold);font-size:14px;text-decoration:none">{t}</a></li>'
        for s, t in ARTIGOS_PENAIS
    ) + '<li style="margin-bottom:10px"><a href="../categoria/penal.html" style="color:var(--gold);font-size:14px;text-decoration:none">Todos os artigos de Direito Penal →</a></li>'

    areas = "".join(
        f'<div style="display:flex;align-items:center;gap:10px;font-size:12px;color:var(--muted)"><span style="color:var(--gold)">✦</span> {a}</div>'
        for a in ["Flagrantes e Custódias", "Liberdade Provisória", "Habeas Corpus", "Inquéritos e Intimações",
                  "Execução Penal e Progressão", "Tornozeleira Eletrônica", "Tribunal do Júri"]
    )

    body = f'''
<div style="max-width:1000px;margin:0 auto;padding:4rem 2rem">
  <div style="margin-bottom:3rem">
    <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1rem;display:flex;align-items:center;gap:14px">
      <span style="width:28px;height:1px;background:var(--gold);display:inline-block"></span>
      Defesa Criminal · Atendimento Urgente
    </div>
    <h1 style="font-family:var(--serif);font-size:2.8rem;color:var(--cream);font-weight:300;line-height:1.15;margin-bottom:1rem">Advogado Criminalista em {nome}</h1>
    <p style="font-size:14px;color:var(--muted);line-height:1.9;max-width:680px">{intro}</p>
  </div>

  <div style="display:grid;grid-template-columns:2fr 1fr;gap:3rem;align-items:start">
    <div>
      {corpo}
      {H2(f"Familiar Preso em {nome}, O Que Fazer Primeiro")}
      {familiar}
      {H2("Conteúdo Sobre Direito Penal")}
      <ul style="list-style:none;padding:0;margin:0">{links}</ul>
    </div>
    <div style="position:sticky;top:90px">
      <div style="background:var(--dark);border:1px solid rgba(201,168,76,0.2);padding:2rem">
        <div style="font-size:9px;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:1.25rem">Atuação Criminal</div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:2rem">{areas}</div>
        <a href="https://wa.me/{WA}?text={wa_msg}" target="_blank" class="btn-whatsapp" style="display:flex;width:100%;justify-content:center;gap:10px">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          Falar com Advogado Agora
        </a>
        <p style="font-size:10px;color:var(--muted);text-align:center;margin-top:1rem;line-height:1.6">Atendimento urgente pelo WhatsApp, inclusive para familiares de pessoas presas</p>
      </div>
    </div>
  </div>
</div>

'''
    html = (HEAD.format(nome=nome, desc=desc, base=BASE, slug=slug, wa=WA) + header + body + tail).replace("</head>", GA_TAG + "</head>", 1)
    with open(f"criminalista/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ criminalista/{slug}.html")

# link interno nas páginas de cidade correspondentes
for slug, nome, _ in CIDADES:
    path = f"cidade/{slug}.html"
    html = open(path, encoding="utf-8").read()
    if "criminalista/" in html:
        continue
    link_html = (f'<div style="max-width:1000px;margin:0 auto;padding:0 2rem 3rem">'
                 f'<div style="background:var(--dark);border:1px solid rgba(201,168,76,0.2);padding:1.5rem 2rem;font-size:14px;color:var(--text)">'
                 f'Precisa de defesa criminal urgente? Conheça a página '
                 f'<a href="../criminalista/{slug}.html" style="color:var(--gold)">Advogado Criminalista em {nome}</a>.'
                 f'</div></div>\n\n<div class="float-wrap">')
    html = html.replace('<div class="float-wrap">', link_html, 1)
    open(path, "w", encoding="utf-8").write(html)
print("✓ links internos inseridos nas 14 páginas de cidade")
