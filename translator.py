import os
import urllib.request
import re
from deep_translator import GoogleTranslator

SOURCE_LANG = 'en'
TARGET_LANG = 'es' 
RSS_URL = 'http://bbci.co.uk' 

repo_dir = os.getenv('GITHUB_WORKSPACE', '.')
OUTPUT_FILE = os.path.join(repo_dir, 'NOTICIAS_TECH.md')

def translate_text(text):
    if not text or not text.strip():
        return ""
    try:
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        print(f"Translation slip: {e}")
        return text

def clean_html(text):
    # Quick regex helper to strip out XML/HTML tags safely
    return re.sub(r'<[^>]*>', '', text).strip()

def main():
    print("Scraping real-time global tech feeds...")
    try:
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            # Decode using errors='ignore' to strip out any broken characters automatically
            rss_text = response.read().decode('utf-8', errors='ignore')
            
        # Split the text by <item> tags manually to completely bypass strict XML parsing errors
        items = rss_text.split('<item>')[1:6] # Grab up to 5 articles
        
        markdown_body = f"# 🚀 Actualización Semanal de Tecnología\n"
        markdown_body += f"*Generado automáticamente por tu motor de traducción artificial*\n\n"
        markdown_body += "---\n\n"
        
        for index, item in enumerate(items, 1):
            # Extract title and description using simple text boundary searches
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.search(r'<title>(.*?)</title>', item)
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item) or re.search(r'<description>(.*?)</description>', item)
            
            title = clean_html(title_match.group(1)) if title_match else "Noticia"
            desc = clean_html(desc_match.group(1)) if desc_match else ""
            
            print(f"Translating story segment {index}...")
            trans_title = translate_text(title)
            trans_desc = translate_text(desc)
            
            markdown_body += f"## 🔥 {trans_title}\n"
            markdown_body += f"{trans_desc}\n\n"
            markdown_body += "---\n\n"
            
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(markdown_body)
            
        print(f"Complete routine finished. Saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Process checkpoint anomaly: {e}")

if __name__ == "__main__":
    main()
