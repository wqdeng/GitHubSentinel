import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from logger import LOG

class HackerNewsClient:
    def __init__(self):
        # Hacker News网址
        self.url = "https://news.ycombinator.com/"

    def fetch_top_stories(self):
        LOG.debug("Fetching top stories from Hacker News.")
        try:
            response = requests.get(self.url)
            # Check whether the request is successful
            response.raise_for_status()

            LOG.debug("Parsing Hacker News HTML content.")
            beautifulsoup = BeautifulSoup(response.text, "html.parser")
            # Look for all tags that contain news <tr>
            draft_top_stories = beautifulsoup.find_all("tr", class_="athing")

            top_stories = []
            for story in draft_top_stories:
                title_tag = story.find("span", class_="titleline").find("a")
                if title_tag:
                    title = title_tag.text
                    link = title_tag["href"]
                    top_stories.append({"title": title, "link": link})
            LOG.info("Successfully parse {len(top_stories)} top stories from Hacker News.}")
            return top_stories
        except Exception as e:
            LOG.error(f"Error fetching Hacker News top stories: {str(e)}")

    def export_top_stories(self):
        LOG.debug("Export Hacker News top stories.")
        top_stories = self.fetch_top_stories()

        if not top_stories:
            LOG.warning("No top stories found.")
            return None

        current_date = datetime.now().strftime("%Y-%m-%d")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # storage path
        target_dir_path = os.path.join("hacker_news", current_date)
        os.makedirs(target_dir_path, exist_ok=True)

        target_file_path = os.path.join(target_dir_path, f"{current_datetime}.md")
        with open(target_file_path, "w", encoding="utf-8") as file:
            file.write(f"# Hacker News Top Stories ({current_datetime})\n\n")
            for index, story in enumerate(top_stories, start=1):
                file.write(f"{index}. [{story['title']}]({story['link']})\n")

        LOG.info(f"Hacker News top stories exported to {target_file_path}")
        return target_file_path

if __name__ == "__main__":
    client = HackerNewsClient()
    client.export_top_stories()
