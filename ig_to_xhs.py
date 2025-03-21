import os
import requests
from googletrans import Translator
from ig_scraper import InstagramScraper
from xhs_poster import XiaohongshuPoster
from config import INSTAGRAM_USERNAME_TO_SCRAPE, ONLY_POSTS_NEWER_THAN_DAYS, POST_LIMIT

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
    translator = Translator()
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
        translated_caption = translator.translate(caption, src="en", dest="zh-cn").text
        print(f'Translated caption: {translated_caption})')


        # Generate title (first 10 Chinese characters of the translated caption)
        title = translated_caption[:20]
        print(f'Title: {title}')

        #Login to Xiaohongshu
        print("Logging in to Xiaohongshu...")
        poster.login()
        # Post to Xiaohongshu
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
