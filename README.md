# Bewie privacy and support

Public support and privacy pages for **Bewie — Every Room Is Borrowed**.

- Website: https://bewie.atelierindustriel.be
- Support: https://bewie.atelierindustriel.be/support
- Privacy: https://bewie.atelierindustriel.be/privacy
- Contact: **bewie.app@cazenave.fr**
- App source: https://github.com/benoit/Bewie

## Languages and routes

Both pages are available in the same ten language variants as `benoit/perleappsite`:

| Language | Path |
| --- | --- |
| English (US) | `/en-us/support`, `/en-us/privacy` |
| English (UK) | `/en-gb/support`, `/en-gb/privacy` |
| Français | `/fr/support`, `/fr/privacy` |
| Español (España) | `/es-es/support`, `/es-es/privacy` |
| Español (México) | `/es-mx/support`, `/es-mx/privacy` |
| Deutsch | `/de/support`, `/de/privacy` |
| Italiano | `/it/support`, `/it/privacy` |
| Português (Brasil) | `/pt-br/support`, `/pt-br/privacy` |
| 日本語 | `/ja/support`, `/ja/privacy` |
| 简体中文 | `/zh-hans/support`, `/zh-hans/privacy` |

`/`, `/support` and `/privacy` serve static US English copies. Language menus keep
the selected page type. Requested languages are never replaced by browser-language
redirects. Pages remain readable without JavaScript. Canonicals, reciprocal
hreflang links, social metadata and the sitemap use the production origin.

## Source and build

`site-content/site.json` owns the name, origin, contact and update date.
`site-content/{language}.json` contains localized support and privacy copy. Contact
placeholders are resolved during the build. `dist/` is the checked-in public output.

```sh
python3 tools/build_public_site.py
python3 -m unittest discover -s tests -v
python3 tools/preview_public_site.py
```

Preview: http://127.0.0.1:4182. No package installation or Node.js is required to
build or serve the site. Commit source and generated pages together. The local tests check all 20 localized pages, internal links, language menus,
canonical URLs and security headers. Rebuilding should leave generated files
unchanged; verify with `git diff --exit-code -- dist`.

## Hosting

Cloudflare Pages project: `bewieappsite`. GitHub source: `benoit/bewieappsite`,
production branch `main`. Build command: empty. Output directory: `dist`.
Custom domain: `bewie.atelierindustriel.be`. Subsequent pushes deploy automatically.

Only `dist/` is published. Security headers restrict scripts and images to the same
origin. No analytics, cookies, stored language preferences, account system, private
guides, enrollment endpoints or push service are included.

## Scope and provenance

Adapted from the public support/privacy pages of `benoit/perleappsite` on
18 November 2026. Existing album support translations were renamed; Perle's guide,
Wi-Fi enrollment, registered-device and private-notification policies were removed.
Bewie-specific text describes optional map location, Apple music delivery,
local playback/data, Messages sharing, website hosting and support correspondence.

The original Bewie logo and current icon come from `benoit/Bewie`. Chalk background
is `#F2F1EC`, ink text is `#0B0C0B`. Store badges and Perle App Store IDs are omitted
until Bewie has its own record. This repository contains no music, private travel
packs, credentials or app build output.
