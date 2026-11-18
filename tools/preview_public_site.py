"""Local public-site preview with Pages-style clean HTML URLs and CSP."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def translate_path(self,path):
  p=Path(super().translate_path(path))
  if not p.exists() and not p.suffix and p.with_suffix('.html').exists():return str(p.with_suffix('.html'))
  return str(p)
 def end_headers(self):
  self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; img-src 'self'; style-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
  super().end_headers()
ThreadingHTTPServer(('127.0.0.1',4182),Handler).serve_forever()

