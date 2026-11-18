import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
LANGS = ['en-us', 'en-gb', 'fr', 'es-es', 'es-mx', 'de', 'it', 'pt-br', 'ja', 'zh-hans']
ORIGIN = 'https://bewie.atelierindustriel.be'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.lang = None; self.links = []; self.alternates = {}; self.canonical = []; self.scripts = []; self.h1 = 0; self.events = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])
        if tag == 'link' and a.get('rel') == 'alternate': self.alternates[a['hreflang']] = a['href']
        if tag == 'script': self.scripts.append(a.get('src'))
        for key in ['href', 'src']:
            if key in a: self.links.append(a[key])
        self.events.extend(key for key in a if key.startswith('on'))

class PublicPagesTests(unittest.TestCase):
    def test_all_twenty_translated_pages_have_correct_identity_and_canonicals(self):
        for lang in LANGS:
            for kind in ['support', 'privacy']:
                file = DIST / lang / f'{kind}.html'; text = file.read_text(); page = Page(text)
                self.assertEqual(page.lang.lower(), lang)
                self.assertEqual(page.h1, 1)
                self.assertEqual(page.canonical, [f'{ORIGIN}/{lang}/{kind}'])
                self.assertIn('mailto:bewie.app@cazenave.fr', page.links)
                self.assertIn('Bewie', text)
                self.assertNotIn('{contact}', text)
                self.assertNotIn('Perle', text)
                self.assertNotIn('perle.app', text)
                self.assertNotIn('SSID', text)
                self.assertNotIn('D1', text)
                self.assertEqual(page.scripts, ['/navigation.mjs'])
                self.assertFalse(page.events)
    def test_language_menu_preserves_page_kind_and_all_ten_languages(self):
        for lang in LANGS:
            for kind in ['support', 'privacy']:
                page = Page((DIST / lang / f'{kind}.html').read_text())
                expected = {f'{ORIGIN}/{target}/{kind}' for target in LANGS} | {f'{ORIGIN}/{kind}'}
                self.assertEqual(set(page.alternates.values()), expected)
                for target in LANGS: self.assertIn(f'/{target}/{kind}', page.links)
    def test_every_local_link_resolves(self):
        for file in DIST.rglob('*.html'):
            for link in Page(file.read_text()).links:
                url = urlsplit(link)
                if url.netloc or url.scheme or not url.path: continue
                target = DIST / url.path.lstrip('/')
                self.assertTrue(target.is_file() or target.with_suffix('.html').is_file() or (target / 'index.html').is_file(), (file, link))
    def test_english_entry_points_are_static_and_no_language_redirects_exist(self):
        for kind in ['support', 'privacy']:
            self.assertEqual((DIST / f'{kind}.html').read_bytes(), (DIST / f'en-us/{kind}.html').read_bytes())
        self.assertEqual((DIST / 'index.html').read_bytes(), (DIST / 'support.html').read_bytes())
        self.assertNotIn('localStorage', (DIST / 'navigation.mjs').read_text())
        self.assertFalse((DIST / '_redirects').exists())
    def test_sitemap_security_and_no_private_services(self):
        urls = [element.text for element in ET.parse(DIST / 'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(set(urls), {f'{ORIGIN}/{lang}/{kind}' for lang in LANGS for kind in ['support', 'privacy']})
        self.assertEqual(len(urls), 20)
        self.assertIn("script-src 'self'", (DIST / '_headers').read_text())
        self.assertFalse(any(p.suffix in ['.p8', '.key', '.pem'] for p in DIST.rglob('*')))
        for name in ['enrollment.json', 'travelpack', 'admin', 'api']: self.assertFalse((DIST / name).exists())
    def test_sources_cover_all_languages_without_guide_registration_policies(self):
        for lang in LANGS:
            data = json.loads((ROOT / f'site-content/{lang}.json').read_text())
            self.assertEqual(len(data['policy']), 6)
            self.assertEqual(len(data['faq']), 8)
        config = json.loads((ROOT / 'site-content/site.json').read_text())
        self.assertEqual(config['origin'], ORIGIN)
        self.assertEqual(config['contact'], 'bewie.app@cazenave.fr')

if __name__ == '__main__': unittest.main()
