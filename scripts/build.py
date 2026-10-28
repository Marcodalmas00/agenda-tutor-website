#!/usr/bin/env python3
"""Build static GitHub Pages resources with Python's standard library only."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
BASE = "https://marcodalmas00.github.io/agenda-tutor-website/"
EMAIL = "dev@marcodalmas00.com"
UPDATED = "2026-10-28"
ROUTES = {"it": {"home": "", "privacy": "privacy/", "support": "supporto/"},
          "en": {"home": "en/", "privacy": "en/privacy/", "support": "en/support/"}}
LABELS = {
    "it": {"home": "Informazioni", "privacy": "Privacy", "support": "Assistenza", "skip": "Vai al contenuto", "index": "In questa pagina", "date": "Aggiornato il 28 ottobre 2026", "contact": "Scrivi all’assistenza", "resources": "Risorse per Agenda Tutor", "language": "English", "other": "en", "sources": "Riferimenti", "beta": "App iPhone · Beta privata"},
    "en": {"home": "Overview", "privacy": "Privacy", "support": "Support", "skip": "Skip to content", "index": "On this page", "date": "Updated 28 October 2026", "contact": "Contact support", "resources": "Agenda Tutor resources", "language": "Italiano", "other": "it", "sources": "References", "beta": "iPhone app · Private beta"}
}

def document(language, key, page):
    labels = LABELS[language]
    route = ROUTES[language][key]
    depth = len([p for p in route.split("/") if p])
    prefix = "../" * depth or "./"
    local = lambda target: prefix + target
    href = lambda name: local(ROUTES[language][name])
    nav = "".join('<a href="{}"{}>{}</a>'.format(href(name), ' aria-current="page"' if name == key else '', labels[name]) for name in ("privacy", "support"))
    switch = local(ROUTES[labels["other"]][key])
    header = f'''<a class="skip" href="#main">{labels['skip']}</a>
<header class="header wrap"><a class="brand" href="{href('home')}" aria-label="Agenda Tutor · {labels['home']}"><picture><source media="(prefers-color-scheme: dark)" srcset="{local('assets/icon-dark.png')}"><img src="{local('assets/icon.png')}" width="44" height="44" alt=""></picture><span>Agenda Tutor</span></a><nav aria-label="{labels['resources']}">{nav}<a class="language" href="{switch}" lang="{labels['other']}" hreflang="{labels['other']}">{labels['language']}</a></nav></header>'''
    sections = "".join(f'<section id="section-{i}"><h2>{escape(section["title"])}</h2>' + "".join(f'<p>{escape(p)}</p>' for p in section['paragraphs']) + '</section>' for i, section in enumerate(page['sections'], 1))
    toc = "".join(f'<a href="#section-{i}">{escape(s["title"])}</a>' for i, s in enumerate(page['sections'], 1))
    sources = ''
    if key == 'privacy':
        sources = f'''<section class="sources"><h2>{labels['sources']}</h2><ul><li><a href="https://developer.apple.com/app-store/app-privacy-details/">Apple · App Privacy</a></li><li><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub · Privacy Statement</a></li><li><a href="https://www.edpb.europa.eu/sme/be-compliant/respect-individuals-rights_en">European Data Protection Board · GDPR</a></li></ul></section>'''
    if key == 'home':
        cards = f'''<div class="resource-grid"><a class="resource-card" href="{href('privacy')}"><span class="card-icon" aria-hidden="true">↗</span><h2>{labels['privacy']}</h2><p>{'Come sono gestiti i dati, i file e le scelte di condivisione.' if language == 'it' else 'How data, files and your sharing choices are handled.'}</p><span>{'Leggi l’informativa' if language == 'it' else 'Read the privacy notice'} <span aria-hidden="true">→</span></span></a><a class="resource-card" href="{href('support')}"><span class="card-icon" aria-hidden="true">↗</span><h2>{labels['support']}</h2><p>{'Risposte pratiche e un contatto diretto per ricevere aiuto.' if language == 'it' else 'Practical answers and a direct contact for help.'}</p><span>{'Trova una risposta' if language == 'it' else 'Find an answer'} <span aria-hidden="true">→</span></span></a></div>'''
        body = f'<main id="main" class="wrap"><div class="hero home-hero"><p class="eyebrow">{labels["beta"]}</p><h1>{escape(page["title"])}</h1><p class="lead">{escape(page["lead"])}</p></div>{cards}<article class="home-copy">{sections}</article></main>'
    else:
        if key == 'support':
            sections = "".join(f'<details id="section-{i}"><summary>{escape(s["title"])}</summary><div>' + "".join(f'<p>{escape(p)}</p>' for p in s['paragraphs']) + '</div></details>' for i, s in enumerate(page['sections'], 1))
        contact = f'<a class="button" href="mailto:{EMAIL}?subject=Agenda%20Tutor%20-%20{labels["support"]}">{labels["contact"]} <span aria-hidden="true">↗</span></a><a class="email" href="mailto:{EMAIL}">{EMAIL}</a>'
        body = f'<main id="main" class="wrap"><div class="hero"><p class="eyebrow">{labels["resources"]}</p><h1>{escape(page["title"])}</h1><p class="lead">{escape(page["lead"])}</p><p class="updated"><time datetime="{UPDATED}">{labels["date"]}</time></p></div><div class="reading-layout"><aside><nav class="toc" aria-label="{labels["index"]}"><h2>{labels["index"]}</h2>{toc}</nav></aside><article class="reading">{sections}{sources}<section class="contact"><h2>{labels["support"]}</h2>{contact}</section></article></div></main>'
    footer = f'<footer class="footer wrap"><p>© 2026 Marco Dal Mas</p><div><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{href("privacy")}">{labels["privacy"]}</a><a href="{href("support")}">{labels["support"]}</a></div></footer>'
    return f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><title>{escape(page['title'])} · Agenda Tutor</title><meta name="description" content="{escape(page['lead'], quote=True)}"><link rel="canonical" href="{BASE + route}"><link rel="alternate" hreflang="it" href="{BASE + ROUTES['it'][key]}"><link rel="alternate" hreflang="en" href="{BASE + ROUTES['en'][key]}"><link rel="icon" type="image/png" href="{local('assets/favicon.png')}"><link rel="apple-touch-icon" href="{local('assets/icon.png')}"><link rel="stylesheet" href="{local('assets/style.css')}"></head><body>{header}{body}{footer}</body></html>'''

def build():
    content = json.loads((ROOT / 'content.json').read_text())
    for language, pages in content.items():
        for key, page in pages.items():
            target = OUT / ROUTES[language][key] / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document(language, key, page))
    (OUT / '.nojekyll').touch()
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    urls = ''.join(f'<url><loc>{BASE + route}</loc><lastmod>{UPDATED}</lastmod></url>' for pages in ROUTES.values() for route in pages.values())
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (OUT / '404.html').write_text(f'<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Pagina non trovata · Agenda Tutor</title><link rel="stylesheet" href="/agenda-tutor-website/assets/style.css"><body><main class="wrap hero"><p class="eyebrow">Agenda Tutor</p><h1>Pagina non trovata</h1><p class="lead">Torna alle informazioni e alle risorse di assistenza.</p><a class="button" href="/agenda-tutor-website/">Vai alla pagina iniziale →</a></main></body></html>')
    print('Built 6 static HTML pages in docs/ for GitHub Pages')

if __name__ == '__main__':
    build()
