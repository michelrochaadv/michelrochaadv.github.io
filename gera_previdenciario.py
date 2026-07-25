# -*- coding: utf-8 -*-
"""Gera páginas /previdenciario/{cidade}.html com conteúdo variado por cidade."""
import os, urllib.parse

BASE = "https://michelrocha.adv.br"
WA = "5571981758097"
GA_TAG = ""  # preenchido no fim a partir de uma página existente

CIDADES = [
    ("salvador", "Salvador", "capital baiana, onde se concentram as agências do INSS e a Justiça Federal da região metropolitana"),
    ("feira-de-santana", "Feira de Santana", "segundo maior município da Bahia, com grande volume de segurados e demandas previdenciárias"),
    ("lauro-de-freitas", "Lauro de Freitas", "município da região metropolitana de Salvador, com população crescente de segurados do INSS"),
    ("castro-alves", "Castro Alves", "cidade do recôncavo baiano, onde o atendimento à distância evita deslocamentos desnecessários"),
    ("vitoria-da-conquista", "Vitória da Conquista", "terceiro maior município da Bahia e polo do sudoeste, com forte demanda em benefícios do INSS"),
    ("ilheus", "Ilhéus", "cidade da costa do cacau, com histórico de trabalho rural e urbano que gera casos previdenciários ricos em detalhes"),
    ("itabuna", "Itabuna", "polo do sul da Bahia, com milhares de segurados urbanos e rurais atendidos pelo INSS da região"),
    ("porto-seguro", "Porto Seguro", "polo do extremo sul baiano, onde trabalhadores do turismo e do comércio somam históricos contributivos variados"),
    ("jequie", "Jequié", "importante cidade do sudoeste baiano, cujos segurados contam com atendimento previdenciário completo à distância"),
    ("alagoinhas", "Alagoinhas", "polo do agreste baiano, com tradição ferroviária e industrial que gera aposentadorias com particularidades"),
    ("barreiras", "Barreiras", "principal cidade do oeste baiano, onde a distância dos grandes centros valoriza o atendimento digital"),
    ("santo-antonio-de-jesus", "Santo Antônio de Jesus", "centro do recôncavo sul, com comércio forte e grande número de contribuintes individuais"),
    ("camacari", "Camaçari", "sede do polo industrial baiano, com muitos casos de aposentadoria especial e benefícios por incapacidade"),
    ("simoes-filho", "Simões Filho", "município industrial da região metropolitana, com trabalhadores expostos a atividades que geram direitos especiais"),
    ("fortaleza", "Fortaleza", "capital do Ceará, onde se concentram as agências do INSS e a Justiça Federal da região metropolitana"),
    ("caucaia", "Caucaia", "segundo município mais populoso do Ceará, com grande volume de segurados urbanos na região metropolitana de Fortaleza"),
    ("juazeiro-do-norte", "Juazeiro do Norte", "polo do Cariri cearense, com milhares de segurados urbanos e rurais atendidos pelas agências do INSS da região"),
    ("maracanau", "Maracanaú", "polo industrial cearense, com muitos casos de aposentadoria especial e benefícios por incapacidade"),
]

UF = {"fortaleza": "CE", "caucaia": "CE", "juazeiro-do-norte": "CE", "maracanau": "CE"}

P1 = [
"Quando o INSS nega um benefício, corta um pagamento ou deixa um pedido parado por meses, a vida de quem depende daquela renda entra em suspenso. Em {c}, milhares de segurados enfrentam essa realidade, e a diferença entre aceitar a negativa e reverter a decisão costuma estar na condução técnica do caso, do entendimento do motivo real da recusa à construção da prova correta.",
"Benefício negado, pagamento cessado após revisão, perícia que não reconheceu a incapacidade, pedido em análise sem fim. As queixas dos segurados de {c} contra o INSS se repetem, e têm algo em comum: grande parte dessas situações pode ser revertida quando o caso é tratado com estratégia, prova bem organizada e conhecimento dos caminhos administrativos e judiciais.",
"A negativa do INSS não é o fim do caminho, é o começo de uma disputa na qual o segurado tem mais instrumentos do que imagina. Para os segurados de {c}, entender o fundamento exato da decisão, reunir a prova certa e escolher entre recurso, novo pedido ou ação judicial é o que separa a perda da renda do benefício concedido com valores retroativos.",
"Poucas coisas desestruturam uma família como a perda da renda que vinha do INSS, ou a espera sem fim por um benefício que não sai. Em {c}, como em todo o país, negativas mal fundamentadas, perícias superficiais e cadastros com vínculos faltando são rotina, e são exatamente os problemas que uma atuação previdenciária técnica existe para resolver.",
]
P2 = [
"A atuação do escritório cobre o ciclo completo dos benefícios: análise do motivo real da negativa ou do corte, organização da prova documental e médica, recursos administrativos, ações judiciais com perícia independente e revisões de benefícios concedidos com valor menor do que o devido. Aposentadorias, auxílios por incapacidade, BPC ao idoso e à pessoa com deficiência e pensões por morte estão entre os casos mais frequentes.",
"O trabalho previdenciário vai da estratégia inicial ao último recurso: conferência do extrato de vínculos e correção de períodos não reconhecidos, preparação para perícias, recursos contra indeferimentos, ações judiciais para concessão e restabelecimento, cobrança de pedidos parados além do prazo legal e revisões de renda mensal. Cada tipo de benefício tem regras e provas próprias, e o enquadramento correto desde o início encurta o caminho.",
"Da aposentadoria negada por suposta falta de tempo ao auxílio cessado após o pente-fino, cada caso previdenciário exige um diagnóstico próprio: o que o INSS alegou, o que a prova disponível demonstra e qual via resolve mais rápido, a administrativa ou a judicial. O escritório atua nas duas frentes, incluindo perícias, BPC, pensões por morte, revisões e o destravamento de pedidos parados há meses.",
"Cada carta de indeferimento do INSS conta uma história incompleta, e o trabalho técnico começa por completá-la: períodos de trabalho que o cadastro ignorou, laudos que a perícia não valorizou, requisitos que a análise administrativa aplicou errado. A partir desse diagnóstico, definem-se recursos, novos pedidos ou ações judiciais, sempre com atenção aos prazos e aos valores retroativos que a demora do INSS não pode apagar.",
]
P3 = [
"Todo o atendimento pode ser feito à distância, pelo WhatsApp e pelos sistemas eletrônicos do INSS e da Justiça Federal, sem que o segurado de {c} precise se deslocar. Documentos são recebidos digitalmente, e o acompanhamento é contínuo, com orientação clara em cada etapa sobre prazos, exigências e possibilidades reais, sem promessas de resultado.",
"Os processos do INSS e da Justiça Federal são eletrônicos, o que permite atender segurados de {c} integralmente à distância: envio de documentos pelo celular, acompanhamento do processo em tempo real e comunicação direta pelo WhatsApp. A distância deixou de ser obstáculo, o que importa é a qualidade técnica da condução do caso.",
"Para os segurados de {c}, todo o processo acontece sem deslocamentos: a análise dos documentos, o protocolo dos pedidos e recursos e o acompanhamento das ações judiciais são feitos pelos sistemas eletrônicos, com atualizações e orientações diretamente pelo WhatsApp, em linguagem clara, sobre cada passo e cada prazo do caso.",
"O atendimento previdenciário a {c} é feito de forma totalmente digital: primeiros esclarecimentos pelo WhatsApp, documentos enviados pelo celular e atuação nos sistemas eletrônicos do INSS e da Justiça. O segurado acompanha tudo de casa, com a tranquilidade de saber exatamente em que fase o caso está e o que esperar de cada etapa.",
]
F1 = [
"O primeiro passo é entender o fundamento exato da decisão do INSS, que consta na carta de indeferimento ou de cessação. A partir dele se define a estratégia: recurso administrativo, novo pedido com prova reforçada ou ação judicial. Agir dentro dos prazos preserva direitos e, nos casos de êxito, os valores retroativos desde o requerimento.",
"Antes de qualquer providência, é preciso ler a decisão do INSS com olhos técnicos: o motivo alegado define o caminho. Perícia desfavorável, falta de qualidade de segurado, carência e renda são fundamentos diferentes, com respostas diferentes. A escolha errada da via custa meses; a escolha certa, feita dentro dos prazos, preserva inclusive os atrasados.",
"Guardar a carta de decisão, não perder os prazos e evitar novos pedidos idênticos protocolados por ansiedade são cuidados que protegem o caso. O passo decisivo, porém, é o diagnóstico técnico: entender por que o INSS negou ou cortou, e montar a resposta certa, administrativa ou judicial, com a prova que faltou da primeira vez.",
"A pressa desorganizada é inimiga do segurado: pedidos repetidos, recursos genéricos e documentos soltos atrasam mais do que ajudam. O caminho eficiente começa pela identificação do fundamento da negativa e segue com a resposta adequada a ele, no prazo certo, com a prova certa, preservando a data do requerimento e os valores que dela decorrem.",
]

ARTIGOS = [
    ("inss-negou-auxilio-por-incapacidade", "INSS Negou Auxílio por Incapacidade, O Que Fazer Agora"),
    ("bpc-loas-negado-o-que-fazer", "BPC LOAS Negado, O Que Fazer Para Reverter a Decisão"),
    ("inss-cortou-beneficio-apos-revisao-o-que-fazer", "INSS Cortou Seu Benefício Após Revisão, O Que Fazer"),
    ("pedido-parado-no-inss-ha-meses-o-que-fazer", "Pedido Parado no INSS Há Meses, O Que Fazer Agora"),
    ("inss-nao-reconheceu-tempo-de-trabalho", "INSS Não Reconheceu Seu Tempo de Trabalho, O Que Fazer"),
]

DESCS = [
"Advogado previdenciário em {nome}. Benefícios do INSS negados, cortes indevidos, aposentadorias e BPC. Atendimento à distância pelo WhatsApp.",
"Advogado previdenciário em {nome}, {uf}. INSS negou ou cortou seu benefício? Atuação completa, sem necessidade de deslocamento.",
"INSS negou seu benefício em {nome}? Advogado previdenciário com atuação em aposentadorias, auxílios, BPC e revisões. Fale pelo WhatsApp.",
]

def gerar():
    src = open("cidade/jequie.html", encoding="utf-8").read()
    header = src.split("<body>")[1].split("</header>")[0] + "</header>"
    tail = '<div class="float-wrap">' + src.split('<div class="float-wrap">')[1]
    # reaproveitar o bloco GA de uma página existente
    ga = src.split("<!-- Google tag (gtag.js) -->")[1].split("</script>")[1]
    ga_block = "<!-- Google tag (gtag.js) -->" + src.split("<!-- Google tag (gtag.js) -->")[1].split("</head>")[0]

    os.makedirs("previdenciario", exist_ok=True)
    P = lambda t: f'<p style="font-size:14px;color:var(--text);line-height:1.9;margin-bottom:1.25rem">{t}</p>'
    H2 = lambda t: f'<h2 style="font-family:var(--serif);font-size:1.8rem;color:var(--cream);font-weight:300;margin:2.5rem 0 1rem">{t}</h2>'

    for i, (slug, nome, descr) in enumerate(CIDADES):
        uf = UF.get(slug, "BA")
        desc = DESCS[i % 3].format(nome=nome, uf=uf)
        wa_msg = urllib.parse.quote(f"Olá, Dr. Michel! Preciso de um advogado previdenciário em {nome}.")
        intro = (f"Atuação completa em benefícios do INSS para segurados de {nome}, {descr}, "
                 f"com atendimento à distância pelo WhatsApp e pelos sistemas eletrônicos, sem necessidade de deslocamento.")
        corpo = P(P1[i % 4].format(c=nome)) + P(P2[(i + 1) % 4]) + P(P3[(i + 2) % 4].format(c=nome))
        comeco = P(F1[(i + i // 4) % 4]) + P(
            "Cada caso tem suas particularidades, e nenhuma orientação genérica substitui a análise da sua decisão concreta. "
            "O que vale para todos: quanto antes o caso recebe tratamento técnico, menores os prazos perdidos e maiores as chances de reverter a posição do INSS.")
        links = "".join(
            f'<li style="margin-bottom:10px"><a href="../artigo/{s}.html" style="color:var(--gold);font-size:14px;text-decoration:none">{t}</a></li>'
            for s, t in ARTIGOS
        ) + '<li><a href="../categoria/previdenciario.html" style="color:var(--gold);font-size:14px;text-decoration:none">Todos os artigos de Direito Previdenciário \u2192</a></li>'
        areas = "".join(
            f'<div style="display:flex;align-items:center;gap:10px;font-size:12px;color:var(--muted)"><span style="color:var(--gold)">\u2726</span> {a}</div>'
            for a in ["Benefício Negado ou Cortado", "Aposentadorias", "Auxílio por Incapacidade",
                      "BPC ao Idoso e à Pessoa com Deficiência", "Pensão por Morte", "Revisões de Benefício", "Pedidos Parados no INSS"])

        body = f'''
<div style="max-width:1000px;margin:0 auto;padding:4rem 2rem">
  <div style="margin-bottom:3rem">
    <div style="font-size:9px;letter-spacing:4px;color:var(--gold);text-transform:uppercase;margin-bottom:1rem;display:flex;align-items:center;gap:14px"><span style="width:28px;height:1px;background:var(--gold);display:inline-block"></span>Direito Previdenci\u00e1rio \u00b7 INSS</div>
    <h1 style="font-family:var(--serif);font-size:2.8rem;color:var(--cream);font-weight:300;line-height:1.15;margin-bottom:1rem">Advogado Previdenci\u00e1rio em {nome}</h1>
    <p style="font-size:14px;color:var(--muted);line-height:1.9;max-width:680px">{intro}</p>
  </div>
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:3rem;align-items:start">
    <div>
      {corpo}
      {H2(f"INSS Negou ou Cortou Seu Benef\u00edcio em {nome}, Por Onde Come\u00e7ar")}
      {comeco}
      {H2("Conte\u00fado Sobre Direito Previdenci\u00e1rio")}
      <ul style="list-style:none;padding:0;margin:0">{links}</ul>
    </div>
    <div style="position:sticky;top:90px">
      <div style="background:var(--dark);border:1px solid rgba(201,168,76,0.2);padding:2rem">
        <div style="font-size:9px;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:1.25rem">Atua\u00e7\u00e3o Previdenci\u00e1ria</div>
        <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:2rem">{areas}</div>
        <a href="https://wa.me/{WA}?text={wa_msg}" target="_blank" class="btn-whatsapp" style="display:flex;width:100%;justify-content:center;gap:10px">Falar com um Advogado Agora</a>
        <p style="font-size:10px;color:var(--muted);text-align:center;margin-top:1rem;line-height:1.6">Atendimento pelo WhatsApp, sem necessidade de deslocamento</p>
      </div>
    </div>
  </div>
</div>

'''
        head = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advogado Previdenci\u00e1rio em {nome} | Michel Rocha Advocacia</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/previdenciario/{slug}.html">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
<link rel="icon" type="image/png" href="../favicon.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LegalService","name":"Michel Rocha Advocacia e Consultoria","url":"{BASE}","telephone":"+{WA}","areaServed":"{nome}, {uf}","description":"{desc}"}}
</script>
{ga_block}
</head>
<body>
'''
        open(f"previdenciario/{slug}.html", "w", encoding="utf-8").write(head + header + body + tail)
        print(f"\u2713 previdenciario/{slug}.html")

if __name__ == "__main__":
    gerar()
