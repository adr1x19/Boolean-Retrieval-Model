import wikipedia
import os

# CONFIGURATION
LANG = "hi"          # Change to 'ta', 'te', 'bn', etc.
NUM_ARTICLES = 1000   # How many you want
OUTPUT_DIR = "data2"  # Where to save

# 1. Setup
wikipedia.set_lang(LANG)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Get random articles to simulate a dataset
print(f"Downloading {NUM_ARTICLES} articles in {LANG}...")
titles = wikipedia.random(pages=NUM_ARTICLES * 2) # Get extra in case of errors

count = 0
for title in titles:
    if count >= NUM_ARTICLES:
        break
    
    try:
        # Fetch the page
        page = wikipedia.page(title)
        content = page.content
        
        # Save to file
        safe_title = "".join(x for x in title if x.isalnum() or x in " -_").strip()
        filename = f"{OUTPUT_DIR}/{count:04d}_{safe_title}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ Saved: {title}")
        count += 1
        
    except wikipedia.exceptions.DisambiguationError:
        print(f"⚠️ Skipped (Ambiguous): {title}")
    except wikipedia.exceptions.PageError:
        print(f"❌ Skipped (Not Found): {title}")
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\nDone! Check the '{OUTPUT_DIR}' folder.")