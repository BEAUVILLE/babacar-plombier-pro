"""Tests de non-régression de la carte animée de Babacar."""
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

class AnimatedCard(unittest.TestCase):
    def test_real_assets_and_dimensions(self):
        gif = (ROOT / "carte-babacar-animee-stop.gif").read_bytes()
        png = (ROOT / "carte-babacar-animee-finale.png").read_bytes()
        self.assertIn(gif[:6], (b"GIF87a", b"GIF89a"))
        self.assertEqual(struct.unpack("<HH", gif[6:10]), (507, 505))
        self.assertNotIn(b"NETSCAPE2.0", gif, "Ne pas programmer de boucle infinie")
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", png[16:24]), (507, 505))
    def test_anim_placed_only_on_babacar_page(self):
        self.assertIn('id="carte-animee"', HTML)
        self.assertIn('src="carte-babacar-animee-stop.gif"', HTML)
        self.assertIn('data-final-src="carte-babacar-animee-finale.png"', HTML)
        self.assertIn("setTimeout(()=>{if(digiyAnimated.isConnected)digiyAnimated.src=digiyAnimated.dataset.finalSrc},3200)", HTML)
        self.assertIn('loading="lazy"', HTML)
    def test_existing_contacts_and_qr_unchanged(self):
        self.assertIn('href="tel:+221776125124"', HTML)
        self.assertIn('https://wa.me/', HTML)
        self.assertIn('function setQr(){const url=profileUrl()', HTML)
        self.assertIn("QRCode.toDataURL(url,{width:320,margin:1}", HTML)
        self.assertIn('href="carte-babacar-plombier-pro-9x16.png"', HTML)
        self.assertIn('rel="canonical" href="https://babacar-plombier-pro.digiylyfe.com/"', HTML)
        self.assertIn("document.getElementById('shareAnimatedCard').onclick=share", HTML)
        self.assertIn("document.getElementById('shareTop').onclick=share", HTML)
        self.assertIn("navigator.share({title:'Babacar Plombier Pro — DIGIY BUILD'", HTML)
    def test_ten_languages_and_no_new_tracking(self):
        block=HTML.split("const ANIM_LABELS={",1)[1].split("\n};",1)[0]
        self.assertEqual(set(re.findall(r"^\s{2}(fr|wo|zh|en|es|pt|it|de|nl|ar):",block,re.M)),{"fr","wo","zh","en","es","pt","it","de","nl","ar"})
        self.assertNotIn("analytics",block.lower())
        self.assertNotIn("data:image/gif;base64",HTML)

if __name__ == "__main__":
    unittest.main()
