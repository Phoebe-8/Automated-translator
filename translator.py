import os
from deep_translator import GoogleTranslator

# 1. Configuration
SOURCE_LANG = 'en'
TARGET_LANG = 'es' # Spanish (Change to any code you want, e.g., 'fr', 'de')
INPUT_FILE = 'english_strings.py'
OUTPUT_FILE = f'translated_{TARGET_LANG}.py'

def translate_text(text):
    try:
        # Uses the free web-browser translation engine safely
        return GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG).translate(text)
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def main():
    # Example input data structure inside your python file
    # In a real scenario, you can import this or read it as a text file
    data_to_translate = {
        "welcome_message": "Hello and welcome to our application!",
        "goodbye_message": "Thank you for visiting us today.",
        "error_alert": "Something went wrong. Please try again later."
    }
    
    translated_data = {}
    
    print("Starting automated translation...")
    for key, value in data_to_translate.items():
        print(f"Translating: {key}...")
        translated_data[key] = translate_text(value)
        
    # Save the output to a brand new file automatically
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Generated automatically by your free translation script\n")
        f.write("translated_strings = {\n")
        for key, val in translated_data.items():
            f.write(f' "{key}": "{val}",\n')
        f.write("}\n")
        
    print(f"Success! Finished file saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
