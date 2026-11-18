"""Build Bewie's static support/privacy pages in ten languages; no network access."""
from pathlib import Path
from html import escape
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
LANGS = ['en-us', 'en-gb', 'fr', 'es-es', 'es-mx', 'de', 'it', 'pt-br', 'ja', 'zh-hans']
HTML_LANG = {'en-us': 'en-US', 'en-gb': 'en-GB', 'es-es': 'es-ES', 'es-mx': 'es-MX', 'pt-br': 'pt-BR', 'zh-hans': 'zh-Hans'}
FLAGS = dict(zip(LANGS, ['🇺🇸', '🇬🇧', '🇫🇷', '🇪🇸', '🇲🇽', '🇩🇪', '🇮🇹', '🇧🇷', '🇯🇵', '🇨🇳']))
CONFIG = json.loads((ROOT / 'site-content/site.json').read_text())
CONTENT = {lang: json.loads((ROOT / f'site-content/{lang}.json').read_text().replace('{contact}', CONFIG['contact'])) for lang in LANGS}
ORIGIN = CONFIG['origin']
E = escape
STYLE = hashlib.sha256((DIST / 'style.css').read_bytes()).hexdigest()[:12]


def path(lang, page):
    return f'/{lang}/{page}'


def language_menu(lang, page):
    links = ''.join(f'<a href="{path(target, page)}" lang="{HTML_LANG.get(target, target)}" hreflang="{HTML_LANG.get(target, target)}" aria-label="{E(CONTENT[target]["name"])}"' + (' aria-current="true"' if target == lang else '') + f'><span aria-hidden="true">{FLAGS[target]}</span></a>' for target in LANGS)
    return f'<details class="languages"><summary aria-label="{E(CONTENT[lang]["language"])} · {E(CONTENT[lang]["name"])}"><span aria-hidden="true">{FLAGS[lang]}</span></summary><div class="language-list">{links}</div></details>'


def contact():
    email = E(CONFIG['contact'], quote=True)
    return f'<!--email_off--><a class="email" href="mailto:{email}">{email}</a><!--/email_off-->'


def page(lang, kind):
    d = CONTENT[lang]
    title = f'Bewie - Every Room Is Borrowed - {d[kind]}'
    description = d['intro'] if kind == 'support' else d['policyIntro']
    canonical = ORIGIN + path(lang, kind)
    alternates = ''.join(f'<link rel="alternate" hreflang="{HTML_LANG.get(target, target)}" href="{ORIGIN}{path(target, kind)}">' for target in LANGS)
    nav = ''.join(f'<a href="{path(lang, target)}"' + (' aria-current="page"' if target == kind else '') + f'>{E(d[target])}</a>' for target in ['support', 'privacy'])
    if kind == 'support':
        faq = ''.join(f'<div><dt>{E(title)}</dt><dd>{E(text)}</dd></div>' for title, text in d['faq'])
        body = f'<section class="intro"><p class="eyebrow">{E(d["tag"])}</p><h1>{E(d["title"])}</h1><p class="lead">{E(d["intro"])}</p></section><div class="content-grid"><section class="contact"><p class="eyebrow">{E(d["support"])}</p><h2>{E(d["contact"])}</h2><p>{E(d["contactText"])}</p>{contact()}<p class="small">{E(d["publisher"])}</p></section><section class="instructions"><h2>{E(d["listen"])}</h2><dl>{faq}</dl></section></div>'
    else:
        sections = ''.join(f'<section><h2>{E(title)}</h2><p>{E(text)}</p></section>' for title, text in d['policy'])
        body = f'<article class="policy"><h1>{E(d["privacy"])}</h1><p class="lead">{E(d["policyIntro"])}</p>{sections}<p class="provider-links"><a href="https://www.apple.com/legal/privacy/">Apple</a><a href="https://www.cloudflare.com/privacypolicy/">Cloudflare</a></p>{contact()}</article>'
    return f'''<!doctype html>
<html lang="{HTML_LANG.get(lang, lang)}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(description, quote=True)}">
<meta name="theme-color" content="#f2f1ec"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Bewie">
<meta property="og:title" content="{E(title, quote=True)}"><meta property="og:description" content="{E(description, quote=True)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{ORIGIN}/icon.png">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(title, quote=True)}"><meta name="twitter:description" content="{E(description, quote=True)}"><meta name="twitter:image" content="{ORIGIN}/icon.png">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}/{kind}">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon.png"><link rel="stylesheet" href="/style.css?v={STYLE}"><script type="module" src="/navigation.mjs"></script>
</head><body><a class="skip" href="#content">{E(d['skip'])}</a><div class="page">
<header class="site-header"><a class="brand" href="{path(lang, 'support')}"><img src="/icon.png" width="42" height="42" alt=""><span>Bewie</span></a><div class="header-actions"><nav aria-label="{E(d['nav'])}">{nav}</nav>{language_menu(lang, kind)}</div></header>
<main id="content">{body}</main><footer><span>© 2026 Benoit Cazenave</span><a href="{path(lang, 'privacy')}">{E(d['privacy'])}</a><span>{E(d['updated'])}</span></footer>
</div></body></html>'''


for lang in LANGS:
    folder = DIST / lang
    folder.mkdir(parents=True, exist_ok=True)
    for kind in ['support', 'privacy']:
        (folder / f'{kind}.html').write_text(page(lang, kind))
# Stable English entry points; requested languages are never redirected.
for kind in ['support', 'privacy']:
    (DIST / f'{kind}.html').write_text(page('en-us', kind))
(DIST / 'index.html').write_text(page('en-us', 'support'))
(DIST / '404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Bewie - 404</title><link rel="stylesheet" href="/style.css"></head><body><div class="page"><main><h1>404</h1><p><a href="/support">Bewie support</a></p></main></div></body></html>''')
(DIST / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{ORIGIN}{path(lang, kind)}</loc></url>\n' for lang in LANGS for kind in ['support', 'privacy']) + '</urlset>\n')
(DIST / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
print('Built 20 localized support/privacy pages and 3 English entry points.')
