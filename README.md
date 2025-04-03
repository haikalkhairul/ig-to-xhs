# Instagram to Xiaohongshu Automation

This project automates the process of scraping Instagram posts and publishing them to Xiaohongshu (Little Red Book). It uses the Apify platform to scrape Instagram data, Google Translate for caption translation, and Selenium for posting to Xiaohongshu.

## Features
- Scrape Instagram posts using the Apify platform.
- Translate Instagram captions to Chinese using Google Translate.
- Automatically post the translated captions and images to Xiaohongshu.

## Prerequisites
1. **Python**: Ensure Python 3.8+ is installed.
2. **Google Chrome**: Required for Selenium.
3. **ChromeDriver**: Ensure the ChromeDriver version matches your Chrome browser version.
4. **Apify Account**: Obtain an API token from [Apify](https://apify.com/).
5. **DeepL Account**: Obtain an API token from [DeepL](https://www.deepl.com/en/products/api).
6. **Xiaohongshu Account**: Ensure you have an account for posting.

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ig-to-xhs
   ```

2. Install the required Python packages (using a virtualenv is recommended):
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the project:
   - Copy `example.config.py` to `config.py`:
     ```bash
     cp example.config.py config.py
     ```
   - Edit `config.py` to set your Apify API token and Instagram username:
     ```python
     APIFY_API_TOKEN = 'your-apify-api-token'
     DEEPL_API_TOKEN='your-deepl-api-token'
     INSTAGRAM_USERNAME_TO_SCRAPE = 'your-instagram-username'
     ONLY_POSTS_NEWER_THAN_DAYS = 5  # Number of days to scrape posts from
     POST_LIMIT = 1  # Number of posts to scrape
     ```

4. Ensure `chromedriver` is in your system's PATH or specify its location in the Selenium setup.

## Quickstart
1. Run the script to scrape Instagram posts and post them to Xiaohongshu:
   ```bash
   python ig_to_xhs.py
   ```

2. The script will:
   - Scrape the latest posts from the specified Instagram account.
   - Translate the captions to Chinese.
   - Post the translated captions and images to Xiaohongshu.

## File Structure
- `ig_scraper.py`: Handles Instagram scraping using Apify.
- `xhs_poster.py`: Automates posting to Xiaohongshu using Selenium.
- `ig_to_xhs.py`: Main script to orchestrate scraping and posting.
- `config.py`: Configuration file for API tokens and settings.
- `requirements.txt`: List of required Python packages.

## Notes
- Ensure your Apify account has sufficient credits to run the Instagram scraper.
- Xiaohongshu login may require manual intervention if cookies or tokens are invalid.
- Images are downloaded to an `imgs` directory in the project root.

## Why?
- To broaden the audience by reaching a new platform and tailoring content to its primary language, ensuring better engagement and resonance with the target community.

## Troubleshooting
- If the Xiaohongshu login fails, ensure your cookies or token are valid.
- For Selenium issues, verify that your ChromeDriver version matches your Chrome browser version.

## To-do/Improvements
- [ ] **Track Uploaded Posts**: Implement functionality to track which Instagram posts have already been uploaded to Xiaohongshu. This will prevent duplicate posts when scraping for new content.
- [ ] **Background Scheduler**: Add a scheduling mechanism to periodically check for new Instagram posts. This will allow the program to run in the background and automatically create Xiaohongshu posts when new content is detected.
- [ ] **Topic Utilization**: Xiaohongshu has 'topics' as their platforms version of hashtags, however, it uses Chinese characters, which makes it slightly challenging to ensure correct translation for the topic.
- [ ] **Containerization**: Containerize the application using Docker to simplify deployment and ensure consistent runtime environments across different systems.
- [x] **Better Translation**: Utilize DeepL instead of Google Translate as the translation yields better accuracy

## License
This project is licensed under the MIT License.