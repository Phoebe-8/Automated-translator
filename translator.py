import os
import urllib.request
import re
from deep_translator import GoogleTranslator

SOURCE_LANG = 'en'
TARGET_LANG = 'es' 
RSS_URL = 'http://bbci.co.uk' 

repo_dir = os.getenv('GITHUB_WORKSPACE', '.')
OUTPUT_FILE = os.path.join(repo_dir, 'index.html')

def translate_text(text):
    if not text or not text.strip():
        return ""
    try:
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        print(f"Translation slip: {e}")
        return text

def clean_html(text):
    return re.sub(r'<[^>]*>', '', text).strip()

def main():
    print("Scraping real-time global tech feeds...")
    try:
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            rss_text = response.read().decode('utf-8', errors='ignore')
            
        items = rss_text.split('<item>')[1:6] 
        
        # Opening web layout tags
        html_body = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Actualización Semanal de Tecnología</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }
        .article { margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        h2 { color: #ff6600; font-size: 20px; margin-top: 10px; }
        p { line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Actualización Semanal de Tecnología</h1>
        <p><em>Generado automáticamente por tu motor de traducción artificial</em></p>
        <hr>
"""
        
        # Loop through each news item, translate it, and actively write it into the HTML structure
        for index, item in enumerate(items, 1):
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.search(r'<title>(.*?)</title>', item)
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item) or re.search(r'<description>(.*?)</description>', item)
            
            title = clean_html(title_match.group(1)) if title_match else "Noticia"
            desc = clean_html(desc_match.group(1)) if desc_match else ""
            
            print(f"Translating story segment {index}...")
            trans_title = translate_text(title)
            trans_desc = translate_text(desc)
            
            # This directly appends the news contents straight inside the web containers!
            html_body += f' <div class="article">\n'
            html_body += f' <h2>🔥 {trans_title}</h2>\n'
            html_body += f' <p>{trans_desc}</p>\n'
            html_body += f' </div>\n'
            
        # Closing web layout tags
        html_body += """ </div>
</body>
</html>"""
            
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_body)
            
        print(f"Complete routine finished successfully. Saved content to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Process checkpoint anomaly: {e}")

if __name__ == "__main__":
    main()
