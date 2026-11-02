"""Fiche Babacar : test des dix langues, sans changer contact direct ni QR."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
LANGS = ("fr", "en", "es", "pt", "it", "de", "nl", "ar", "wo", "zh")

class MemberFicheTenLanguages(unittest.TestCase):
    def test_selector_shows_all_ten_languages(self):
        block = HTML.split('<div class="lang" aria-label="Languages">', 1)[1].split("</div>", 1)[0]
        found = re.findall(r'data-lang="([^"]+)"', block)
        self.assertEqual(tuple(found), LANGS)
        self.assertIn('lang="zh-CN"', block)
        self.assertIn('lang="wo"', block)

    def test_both_dictionaries_have_full_independent_translation(self):
        m = re.search(r'const P=\\{\\nwo:(\\{.*?\\}),\\nzh:(\\{.*?\\}),\\nfr:', HTML, re.S)
        self.assertIsNotNone(m)
        wo, zh = json.loads(m.group(1)), json.loads(m.group(2))
        required = {
            "brand", "kicker", "lead", "official", "direct", "write", "call",
            "share", "services", "servicesLead", "items", "doctrine",
            "qr", "copy", "card", "copied", "prompt", "shareText", "wa",
            "footer", "hero", "contact", "detail", "back", "dockCall"
        }
        self.assertEqual(set(wo), required)
        self.assertEqual(set(zh), required)
        self.assertEqual(len(wo["items"]), 6)
        self.assertEqual(len(zh["items"]), 6)
        for d in (wo, zh):
            self.assertTrue(all(isinstance(v, str) and v.strip() for k, v in d.items() if k != "items"))
            self.assertTrue(all(v.strip() for v in d["items"]))
        self.assertNotEqual(wo["lead"], zh["lead"])
        self.assertIn('document.documentElement.lang=lang===\'zh\'?\'zh-CN\':lang', HTML)

    def test_lang_tags_and_critical_paths_stay(self):
        for lang in ("wo", "zh-CN"):
            self.assertIn('hreflang="' + lang + '"', HTML)
        self.assertIn('href="tel:+221776125124"', HTML)
        self.assertIn('https://wa.me/', HTML)
        self.assertIn('function setQr()', HTML)
        self.assertIn('function profileUrl()', HTML)
        self.assertIn('function ownerUrl()', HTML)
        self.assertIn("lang==='zh'||lang==='wo'?'fr':lang", HTML)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_inline_script_syntax(self):
        blocks = re.findall(r'<script(?:\\s[^>]*)?>(.*?)</script>', HTML, re.S)
        program = next((b for b in blocks if "const P={" in b), "")
        self.assertTrue(program, "i18n script not found")
        run = subprocess.run(["node", "--check"], input=program,
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)

if __name__ == "__main__":
    unittest.main()
