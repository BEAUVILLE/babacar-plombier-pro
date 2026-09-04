from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
tag = '<script src="https://digiylyfe.com/assets/digiy-card-favorite-v1.js?v=20260904-v2"></script>'
if 'digiy-card-favorite-v1.js' not in text:
    if '</body>' not in text:
        raise SystemExit('</body> introuvable dans index.html')
    text = text.replace('</body>', tag + '\n</body>', 1)
    path.write_text(text, encoding='utf-8')
