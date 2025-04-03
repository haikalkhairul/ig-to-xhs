import os
import requests
from deepl import Translator
from ig_scraper import InstagramScraper
from xhs_poster import XiaohongshuPoster
from config import DEEPL_API_TOKEN, INSTAGRAM_USERNAME_TO_SCRAPE, ONLY_POSTS_NEWER_THAN_DAYS, POST_LIMIT
import re

def preprocess_caption(caption):
    # Rewrite this method to preprocess the caption as needed

    # Surround item names after food/drink emoji with <x>...</x>
    food_drink_emojis = [
        "🍎", "🍊", "🍌", "🍉", "🍇", "🍓", "🍒", "🍍", "🥭", "🥝", "🍅", "🥑", "🍆", "🥕", "🌽", "🥔", "🍠", "🥒", 
        "🥬", "🥦", "🧄", "🧅", "🍄", "🥜", "🌰", "🍞", "🥐", "🥖", "🥨", "🥯", "🧀", "🥚", "🍳", "🥞", "🧇", "🥓", 
        "🥩", "🍗", "🍖", "🌭", "🍔", "🍟", "🍕", "🥪", "🌮", "🌯", "🥗", "🥘", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", 
        "🍱", "🥟", "🍤", "🍙", "🍚", "🍘", "🍥", "🥠", "🥮", "🍢", "🍡", "🍧", "🍨", "🍦", "🥧", "🍰", "🎂", "🧁", 
        "🍮", "🍭", "🍬", "🍫", "🍿", "🧂", "🥤", "🧃", "🧉", "🧊", "🍺", "🍻", "🥂", "🍷", "🥃", "🍸", "🍹", "🍾", 
        "🍼", "☕", "🍵", "🫖", "🥛", "🍽️"
    ]
    caption = re.sub(
        rf"({'|'.join(map(re.escape, food_drink_emojis))} [^\n:]+)", 
        r"<x>\1</x>", 
        caption
    )
    return caption

def postprocess_caption(caption):
    # Rewrite this method to postprocess the caption as needed

    # Remove <x>...</x> tags
    caption = re.sub(r"<x>(.*?)</x>", r"\1", caption)
    return caption

def scrape_and_post(username, days, post_limit):
    # Create 'imgs' directory if it doesn't exist
    print("Creating 'imgs' directory...")
    imgs_dir = os.path.join(os.getcwd(), "imgs")
    os.makedirs(imgs_dir, exist_ok=True)

    # Initialize Instagram scraper
    print("Initializing Instagram scraper...")
    scraper = InstagramScraper(
        username=[username],
        only_posts_newer_than=f"{days} days",
        results_limit=post_limit,
        skip_pinned_posts=True
    )
    print("Running Instagram scraper...")
    run = scraper.run()

    # Initialize translator and Xiaohongshu poster
    translator = Translator(DEEPL_API_TOKEN)
    poster = XiaohongshuPoster()

    for item in scraper.client.dataset(run["defaultDatasetId"]).iterate_items():
        # Download images
        print(f"Downloading {len(item.get("images", []))} images for post {item['id']} from {item['timestamp']}...")
        image_paths = []
        for idx, image_url in enumerate(item.get("images", [])):
            response = requests.get(image_url)
            if response.status_code == 200:
                image_path = os.path.join(imgs_dir, f"{item['id']}_{idx}.jpg")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                image_paths.append(image_path)

        # Translate caption
        print("Translating caption...")
        caption = item.get("caption", "")
        print(f'Original caption: {caption}')
        caption = preprocess_caption(caption)
        print(f'Preprocessed caption: {caption}')
        translated_caption = translator.translate_text(
            caption,
            source_lang="EN",
            target_lang="ZH-HANS",
            preserve_formatting=True,
            model_type="prefer_quality_optimized",
            tag_handling="xml",
            ignore_tags="x",
            ).text
        translated_caption = postprocess_caption(translated_caption)
        print(f'Translated caption: {translated_caption})')

        title = translated_caption[:20]
        print(f'Title: {title}')

        print("Logging in to Xiaohongshu...")
        poster.login()
        print("Posting to Xiaohongshu...")
        poster.post_article(title=title, content=translated_caption, images=image_paths)

    # Close Xiaohongshu poster
    poster.close()

# Example usage
if __name__ == "__main__":
    username = INSTAGRAM_USERNAME_TO_SCRAPE
    days = ONLY_POSTS_NEWER_THAN_DAYS
    post_limit = POST_LIMIT
    print("Scraping Instagram and posting to Xiaohongshu...")
    print(f'Getting the latest {post_limit} post(s) from {username} in the last {days} day(s)')
    scrape_and_post(username, days, post_limit)
    print("Done!")
