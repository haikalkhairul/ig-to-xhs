from apify_client import ApifyClient
from config import APIFY_API_TOKEN


class InstagramScraper:
    def __init__(self, username: list[str], only_posts_newer_than: str, results_limit: int, skip_pinned_posts: bool):
        self.username = username
        self.only_posts_newer_than = only_posts_newer_than
        self.results_limit = results_limit
        self.skip_pinned_posts = skip_pinned_posts
        # Prepare the Actor input
        self.run_input = {
            "onlyPostsNewerThan": self.only_posts_newer_than,
            "resultsLimit": self.results_limit,
            "skipPinnedPosts": self.skip_pinned_posts,
            "username": self.username
        }
        # Initialize the ApifyClient with your API token
        self.client = ApifyClient(APIFY_API_TOKEN)

    def run(self):
        # Run the Actor and wait for it to finish
        run = self.client.actor("nH2AHrwxeTRJoN5hX").call(run_input=self.run_input)
        return run



# --- Main Loop ---
# if __name__ == "__main__":
#     scraper = InstagramScraper(username=["natgeo"], only_posts_newer_than="5 days", results_limit=3, skip_pinned_posts=True)
#     run = scraper.run()
#     # Fetch and print Actor results from the run's dataset (if there are any)
#     for item in scraper.client.dataset(run["defaultDatasetId"]).iterate_items():
#         print(item)
