#!/usr/bin/env python3
"""
Script zum Aktualisieren der JSON-URL in index.html
Verwendung: python update_json_url.py DEINE_R2_URL
"""

import sys
import re

def update_json_url(new_url):
    # Lese index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Finde und ersetze die fetch URL
    pattern = r"const response = await fetch\('([^']+)',\s*\{"
    replacement = f"const response = await fetch('{new_url}', {{"
    
    updated_content = re.sub(pattern, replacement, content)
    
    # Schreibe zurück
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✓ URL erfolgreich aktualisiert zu: {new_url}")
    print(f"✓ index.html wurde gespeichert")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Fehler: Bitte gib die R2-URL als Parameter an")
        print("Verwendung: python update_json_url.py https://pub-XXXXX.r2.dev/catalog_master.json")
        sys.exit(1)
    
    new_url = sys.argv[1]
    
    if not new_url.startswith('http'):
        print("❌ Fehler: URL muss mit http:// oder https:// beginnen")
        sys.exit(1)
    
    update_json_url(new_url)
