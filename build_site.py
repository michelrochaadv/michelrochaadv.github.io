import json
import os
from datetime import datetime

GITHUB_USERNAME = "michelrochaadv"
WA_NUMBER = "5571981758097"
WA_MSG_DEFAULT = "Olá, Dr. Michel! Vim pelo blog e gostaria de falar com um advogado."

def wa_link(msg=None):
    from urllib.parse import quote
    m = msg or WA_MSG_DEFAULT
    return f"https://wa.me/{WA_NUMBER}?text={quote(m)}"

def build_article_page(article: dict) -> str:
    d = article["data"]
    tag = article["tag"]
    date_display = article["date_display"]
    area = article["area"]
    wa = wa_link(f"Olá, Dr. Michel! Li o artigo sobre '{d['titulo']}' e gostaria de uma consulta.")

    secoes_html = ""
    for sec in d.get("secoes", []):
        secoes_html += f"""
        <div class="article-section">
          <h2 class="sec-title">{sec['titulo']}</h2>
          <p>{sec['conteudo'].replace(chr(10), '</p><p>')}</p>
        </div>
        <div class="inline-cta">
          <span>Ficou com dúvida?</span>
          <a href="{wa}" target="_blank" class="btn-inline-wa">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            Falar com Advogado
          </a>
        </div>"""

    kw_str = ", ".join(d.get("palavras_chave", []))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['titulo']} | Michel Rocha Advocacia</title>
<meta name="description" content="{d['descricao_seo']}">
<meta name="keywords" content="{kw_str}">
<meta property="og:title" content="{d['titulo']}">
<meta property="og:description" content="{d['descricao_seo']}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Michel Rocha Advocacia e Consultoria">
<link rel="canonical" href="https://{GITHUB_USERNAME}.github.io/artigo/{article['slug']}.html">
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{d['titulo']}","author":{{"@type":"Person","name":"Michel Rocha","jobTitle":"Advogado"}},"publisher":{{"@type":"Organization","name":"Michel Rocha Advocacia e Consultoria"}},"datePublished":"{article['date']}","description":"{d['descricao_seo']}"}}
</script>
</head>
<body>
<header>
  <div class="header-inner">
    <a href="../index.html" class="logo-area">
      <img src="../logo.png" class="logo-img" alt="Michel Rocha Advocacia">
    </a>
    <nav>
      <a href="../index.html#artigos">Artigos</a>
      <a href="../index.html#captacao">Contato</a>
      <a href="{wa_link()}" target="_blank" class="nav-cta">
        <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Falar com Advogado
      </a>
    </nav>
  </div>
</header>

<main class="article-main">
  <div class="article-container">
    <div class="article-breadcrumb"><a href="../index.html">Início</a> › <span>{tag}</span></div>
    <div class="article-tag">{tag}</div>
    <h1 class="article-title">{d['titulo']}</h1>
    <p class="article-subtitle">{d['subtitulo']}</p>
    <div class="article-meta">
      <span>Dr. Michel Rocha</span>
      <span>·</span>
      <span>{date_display}</span>
      <span>·</span>
      <span>{d['tempo_leitura']} de leitura</span>
    </div>

    <div class="article-cta-top">
      <p><strong>Precisa de orientação jurídica sobre este tema?</strong></p>
      <a href="{wa}" target="_blank" class="btn-whatsapp">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Falar com Dr. Michel agora
      </a>
    </div>

    <div class="article-intro"><p>{d['introducao']}</p></div>

    <div class="article-body">
      {secoes_html}
    </div>

    <div class="article-conclusion">
      <p>{d['conclusao']}</p>
    </div>

    <div class="article-cta-bottom">
      <h3>Precisa de ajuda com este assunto?</h3>
      <p>Fale diretamente com o Dr. Michel Rocha pelo WhatsApp. Atendimento em todo o Brasil.</p>
      <a href="{wa}" target="_blank" class="btn-whatsapp large">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Falar com Advogado pelo WhatsApp
      </a>
      <p class="cta-note">Atendimento direto com o Dr. Michel Rocha · BA, CE, SP, RJ, MG e outros estados</p>
    </div>
  </div>
</main>

<div class="float-wrap">
  <div class="float-label">Falar com um advogado</div>
  <a href="{wa_link()}" target="_blank" class="float-btn" aria-label="WhatsApp">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>
</div>

<footer>
  <div class="foot-inner">
    <div class="foot-brand">Michel Rocha · Advocacia e Consultoria</div>
    <div class="foot-info">Atuação nacional · BA · CE · RJ · SP · MG · SC · PA · GO · RS · PE</div>
    <div class="foot-links">
      <a href="../index.html">Início</a>
      <a href="{wa_link()}" target="_blank" class="foot-wa">
        <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Falar com Advogado
      </a>
    </div>
  </div>
</footer>
</body>
</html>"""

def build_all_articles():
    """Reconstrói todas as páginas de artigos a partir dos JSONs."""
    os.makedirs("artigo", exist_ok=True)
    if not os.path.exists("artigos"):
        print("Nenhum artigo encontrado ainda.")
        return

    count = 0
    for fname in os.listdir("artigos"):
        if fname.endswith(".json") and fname != "index.json":
            with open(f"artigos/{fname}", 'r', encoding='utf-8') as f:
                article = json.load(f)
            html = build_article_page(article)
            out = f"artigo/{article['slug']}.html"
            with open(out, 'w', encoding='utf-8') as f:
                f.write(html)
            count += 1

    print(f"✓ {count} páginas de artigos geradas")

def build_sitemap():
    """Gera sitemap.xml para SEO."""
    index_file = "artigos/index.json"
    urls = [f"https://{GITHUB_USERNAME}.github.io/"]

    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        for a in index:
            urls.append(f"https://{GITHUB_USERNAME}.github.io/artigo/{a['slug']}.html")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f'  <url><loc>{url}</loc><changefreq>daily</changefreq><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'

    with open("sitemap.xml", 'w') as f:
        f.write(sitemap)
    print(f"✓ Sitemap gerado com {len(urls)} URLs")

if __name__ == "__main__":
    build_all_articles()
    build_sitemap()
