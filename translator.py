import os
import xml.etree.ElementTree as ET
import urllib.request
from deep_translator import GoogleTranslator

# 1. Target Configurations
SOURCE_LANG = 'en'
TARGET_LANG = 'es' # Spanish
RSS_URL = 'http://bbci.co.uk' 
OUTPUT_FILE = 'NOTICIAS_TECH.md' # This creates a clean Markdown article file

def translate_text(text):
    if not text or not text.strip():
        return ""
    try:
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        print(f"Translation slip: {e}")
        return text

def main():
    print("Scraping real-time global tech feeds...")
    try:
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            rss_data = response.read()
            
        root = ET.fromstring(rss_data)
        articles = root.findall('.//item')[:5] # Grabs the top 5 articles
        
        # Build a beautiful, readable article page
        markdown_body = f"# 🚀 Actualización Semanal de Tecnología\n"
        markdown_body += f"*Generado automáticamente por tu motor de traducción artificial*\n\n"
        markdown_body += "---\n\n"
        
        for index, item in enumerate(articles, 1):
            title = item.find('title').text
            desc = item.find('description').text
            
            print(f"Translating story segment {index}...")
            trans_title = translate_text(title)
            trans_desc = translate_text(desc)
            
            markdown_body += f"## 🔥 {trans_title}\n"
            markdown_body += f"{trans_desc}\n\n"
            markdown_body += "---\n\n"
            
        # Save straight to the cloud repository file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(markdown_body)
            
        print(f"Complete routine finished. Saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Process checkpoint anomaly: {e}")

if __name__ == "__main__":
    main()
