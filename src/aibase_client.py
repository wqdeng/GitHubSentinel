import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from logger import LOG

class AIBaseClient:
    def __init__(self):
        self.url = "https://news.aibase.com/news"

    def fetch_today_ai_trending(self):
        LOG.debug("Fetching Today's AI Trending from AIBase.")
        try:
            response = requests.get(self.url)
            # Check whether the request is successful
            response.raise_for_status()

            LOG.debug("Parsing AIBase HTML content.")
            beautifulsoup = BeautifulSoup(response.text, "html.parser")
            # Look for all tags that contain news <a>
            draft_today_ai_trending_nodes = beautifulsoup.find_all("a", class_="truncate")

            today_ai_trending = []
            for ai_trending_node in draft_today_ai_trending_nodes:
                link = ai_trending_node["href"]
                if link.startswith("/news/"):
                    title = ai_trending_node.text.strip()
                    today_ai_trending.append({"title": title, "link": f"https://news.aibase.com{link}"})

            LOG.info(f"Successfully parse {len(today_ai_trending)} AI Trending from AIBase")
            return today_ai_trending
        except Exception as e:
            LOG.error(f"Error fetching AIBase Today's AI Trending: {str(e)}")
            return []

    def export_today_ai_trending(self):
        LOG.debug("Export AIBase today's AI trending.")
        top_stories = self.fetch_today_ai_trending()

        if not top_stories:
            LOG.warning("No AI Trending found.")
            return None

        current_date = datetime.now().strftime("%Y-%m-%d")

        # storage path
        target_dir_path = os.path.join("ai_base")
        os.makedirs(target_dir_path, exist_ok=True)

        target_file_path = os.path.join("ai_base", f"{current_date}.md")
        with open(target_file_path, "w") as file:
            file.write(f"# AIBase Today's AI Trending ({current_date})\n\n")
            for index, story in enumerate(top_stories, start=1):
                file.write(f"{index}. [{story['title']}]({story['link']})\n")

        LOG.info(f"AIBase Today's AI Trending exported to {target_file_path}")
        return target_file_path

if __name__ == "__main__":
    client = AIBaseClient()
    client.export_today_ai_trending()