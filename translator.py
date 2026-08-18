import os
import xml.etree.ElementTree as ET
import urllib.request
from deep_translator import GoogleTranslator

# 1. Settings
SOURCE_LANG = 'en'
TARGET_LANG = 'es' # Change to 'fr', 'de', etc.
# Example: BBC Tech News RSS Feed
RSS_URL = 'http://bbci.co.uk' 
OUTPUT_FILE = 'latest_news_translated.txt'

def translate_text(text):
    if not text.strip():
        return ""
    try:
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        print(f"Error: {e}")
        return text

def main():
    print("Fetching latest news articles...")
    try:
        # Pull down the live web data
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            rss_data = response.read()
            
        # Parse the XML structure of the feed
        root = ET.fromstring(rss_data)
        articles = root.findall('.//item')[:5] # Grab the 5 latest articles
        
        print(f"Found {len(articles)} articles. Translating...")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(f"# Automated Translation Output ({TARGET_LANG.upper()})\n\n")
            
            for index, item in enumerate(articles, 1):
                title = item.find('title').text
                desc = item.find('description').text
                
                print(f"Translating article {index}...")
                translated_title = translate_text(title)
                translated_desc = translate_text(desc)
                
                # Write cleanly to our text file
                f.write(f"--- ARTICLE {index} ---\n")
                f.write(f"Title: {translated_title}\n")
                f.write(f"Description: {translated_desc}\n\n")
                
        print(f"Done! Saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Failed to fetch or process RSS: {e}")

if __name__ == "__main__":
    main()

