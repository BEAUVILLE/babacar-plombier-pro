import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
URL="https://babacar-plombier-pro.digiylyfe.com/"
class DiscoveryTests(unittest.TestCase):
    def test_canonical(self):
        page=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('rel="canonical" href="'+URL+'"',page)
        self.assertIn('name="robots" content="index,follow',page)
    def test_sitemap(self):
        tree=ET.parse(ROOT/"sitemap.xml")
        self.assertEqual([e.text for e in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")],[URL])
    def test_robots(self):
        body=(ROOT/"robots.txt").read_text(encoding="utf-8")
        self.assertIn("Allow: /",body)
        self.assertIn("Sitemap: "+URL+"sitemap.xml",body)
if __name__=="__main__": unittest.main()
