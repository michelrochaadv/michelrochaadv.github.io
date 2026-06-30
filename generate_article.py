import anthropic
import json
import os
import re
from datetime import datetime
import random

# Configuração
GITHUB_USERNAME = "michelrochaadv"
REPO_NAME = f"{GITHUB_USERNAME}.github.io"

# Temas rotativos por área jurídica com palavras-chave SEO
TOPICS = [
    {"area": "Penal", "tag": "Direito Penal", "temas": [
        "habeas corpus como funciona e quando usar",
        "prisão preventiva requisitos e prazo",
        "crimes econômicos responsabilidade penal do empresário",
        "legítima defesa no direito penal brasileiro",
        "audiência de custódia direitos do preso",
        "inquérito policial como funciona",
        "fiança criminal como solicitar",
    ]},
    {"area": "Previdenciário", "tag": "Previdenciário", "temas": [
        "aposentadoria por incapacidade como requerer INSS 2026",
        "BPC LOAS quem tem direito benefício assistencial",
        "benefício negado INSS como recorrer",
        "aposentadoria especial atividade insalubre",
        "revisão da vida toda INSS como funciona",
        "auxílio doença INSS requisitos 2026",
        "pensão por morte INSS quem tem direito",
    ]},
    {"area": "Empresarial", "tag": "Empresarial", "temas": [
        "contratos empresariais cláusulas abusivas STJ",
        "responsabilidade do sócio dívidas empresa",
        "dissolução societária como funciona",
        "holding familiar vantagens e como constituir",
        "recuperação judicial como funciona para empresa",
        "contrato social alteração como fazer",
        "responsabilidade civil empresa por falha serviço",
    ]},
    {"area": "Consumidor", "tag": "Consumidor", "temas": [
        "tabela price juros abusivos financiamento",
        "negativação indevida SPC Serasa indenização",
        "desvio produtivo consumidor dano moral",
        "restituição em dobro cobrança indevida CDC",
        "cancelamento unilateral contrato fornecedor",
        "produto com defeito direitos do consumidor",
        "fraude financiamento veículo direitos",
    ]},
    {"area": "Família", "tag": "Família e Divórcio", "temas": [
        "divórcio consensual como fazer cartório 2026",
        "guarda compartilhada como funciona na prática",
        "pensão alimentícia como calcular e requerer",
        "inventário judicial e extrajudicial diferença",
        "união estável reconhecimento e direitos",
        "alienação parental como identificar e agir",
        "partilha de bens divórcio regime casamento",
    ]},
    {"area": "Imobiliário", "tag": "Imobiliário", "temas": [
        "compra imóvel cuidados jurídicos certidões",
        "usucapião tipos requisitos como requerer",
        "contrato aluguel direitos inquilino proprietário",
        "distrato imóvel na planta direitos comprador",
        "condomínio inadimplência cobrança taxa",
        "escritura imóvel como regularizar",
        "ação possessória reintegração posse",
    ]},
]

def get_today_topic():
    """Seleciona tema baseado no dia para garantir rotatividade."""
    day = datetime.now().day
    area_index = day % len(TOPICS)
    area = TOPICS[area_index]
    tema_index = (datetime.now().month + day) % len(area["temas"])
    return area, area["temas"][tema_index]

def generate_article(api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    area, tema = get_today_topic()
    today = datetime.now().strftime("%d/%m/%Y")
    today_iso = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r'[^a-z0-9]+', '-', tema.lower()).strip('-')[:60]

    prompt = f"""Você é um advogado especialista em {area['area']} escrevendo para o blog Michel Rocha Advocacia e Consultoria.

Escreva um artigo jurídico completo sobre: "{tema}"

REGRAS OBRIGATÓRIAS:
- Linguagem acessível para leigos, mas com autoridade jurídica
- Tom profissional e confiável
- Mencione legislação e jurisprudência real (STJ, STF, TJs)
- Ao final, sempre incentive o leitor a buscar orientação jurídica pelo WhatsApp
- Data de hoje: {today}
- NÃO use markdown com # ou ** — use texto puro com seções claras

ESTRUTURA OBRIGATÓRIA (retorne APENAS JSON válido):
{{
  "titulo": "Título SEO otimizado com a palavra-chave principal (máx 65 caracteres)",
  "subtitulo": "Subtítulo explicativo (máx 120 caracteres)",
  "descricao_seo": "Descrição para Google (máx 155 caracteres, inclua palavra-chave)",
  "tempo_leitura": "X min",
  "introducao": "Parágrafo de introdução envolvente (3-4 linhas)",
  "secoes": [
    {{"titulo": "Título da seção", "conteudo": "Conteúdo detalhado da seção (mínimo 150 palavras)"}},
    {{"titulo": "Título da seção 2", "conteudo": "Conteúdo..."}},
    {{"titulo": "Título da seção 3", "conteudo": "Conteúdo..."}},
    {{"titulo": "O que fazer agora", "conteudo": "Orientação prática e CTA para WhatsApp do Dr. Michel Rocha (71) 98175-8097"}}
  ],
  "conclusao": "Parágrafo de conclusão com CTA para contato",
  "palavras_chave": ["palavra1", "palavra2", "palavra3", "palavra4", "palavra5"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    # Limpar possível markdown
    raw = re.sub(r'```json\s*', '', raw)
    raw = re.sub(r'```\s*', '', raw)
    article_data = json.loads(raw.strip())

    return {
        "slug": slug,
        "area": area["area"],
        "tag": area["tag"],
        "date": today_iso,
        "date_display": today,
        "data": article_data
    }

def save_article(article: dict):
    """Salva o artigo como JSON no diretório de artigos."""
    os.makedirs("artigos", exist_ok=True)
    filename = f"artigos/{article['date']}-{article['slug']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    print(f"Artigo salvo: {filename}")
    return filename

def update_index(article: dict):
    """Atualiza o índice de artigos."""
    index_file = "artigos/index.json"
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = []

    entry = {
        "slug": article["slug"],
        "area": article["area"],
        "tag": article["tag"],
        "date": article["date"],
        "date_display": article["date_display"],
        "titulo": article["data"]["titulo"],
        "subtitulo": article["data"]["subtitulo"],
        "descricao_seo": article["data"]["descricao_seo"],
        "tempo_leitura": article["data"]["tempo_leitura"],
    }

    # Evitar duplicatas
    index = [a for a in index if a["slug"] != article["slug"]]
    index.insert(0, entry)
    # Manter últimos 90 artigos no índice
    index = index[:90]

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Índice atualizado: {len(index)} artigos")

if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY não definida")

    print(f"Gerando artigo para {datetime.now().strftime('%d/%m/%Y')}...")
    article = generate_article(api_key)
    save_article(article)
    update_index(article)
    print(f"✓ Artigo gerado: {article['data']['titulo']}")
