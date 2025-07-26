import os
import sys
from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aibase_client import AIBaseClient


class TestAIBaseClient(unittest.TestCase):
    def setUp(self):
        self.client = AIBaseClient()

    @patch("aibase_client.requests.get")
    def test_fetch_today_ai_trending_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <div class="flex items-center gap-[8px] h-[14px]">
          <div class="activeColor font600 min-w-[16px] text-[16px] text-center">1</div>
          <a href="/news/19838" class="text-[14px] leading-[14px] mainColor activeHover truncate">Google Gemini Advanced Version Makes a Stunning Debut! Wins Gold Medal at IMO 2025, the New Challenger in the Mathematical Olympiad!</a>
        </div>
        '''
        mock_get.return_value = mock_response

        today_ai_trending = self.client.fetch_today_ai_trending()
        self.assertEqual(len(today_ai_trending), 1)
        self.assertEqual(today_ai_trending[0]['title'], 'Google Gemini Advanced Version Makes a Stunning Debut! Wins Gold Medal at IMO 2025, the New Challenger in the Mathematical Olympiad!')
        self.assertEqual(today_ai_trending[0]['link'], 'https://news.aibase.com/news/19838')

    @patch("aibase_client.requests.get")
    def test_fetch_today_ai_trending_failure(self, mock_get):
        mock_get.side_effect = Exception("Read Timed Out.")

        today_ai_trending = self.client.fetch_today_ai_trending()
        self.assertEqual(today_ai_trending, [])

    @patch("aibase_client.requests.get")
    @patch("aibase_client.os.makedirs")
    @patch("aibase_client.open", new_callable=unittest.mock.mock_open)
    def test_export_today_ai_trending(self, mock_open, mock_makedirs, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <div class="flex items-center gap-[8px] h-[14px]">
          <div class="activeColor font600 min-w-[16px] text-[16px] text-center">1</div>
          <a href="/news/19838" class="text-[14px] leading-[14px] mainColor activeHover truncate">Google Gemini Advanced Version Makes a Stunning Debut! Wins Gold Medal at IMO 2025, the New Challenger in the Mathematical Olympiad!</a>
        </div>
        '''
        mock_get.return_value = mock_response

        # 调用导出方法
        file_path = self.client.export_today_ai_trending()

        # 验证目录和文件创建
        current_date = datetime.now().strftime("%Y-%m-%d")
        mock_makedirs.assert_called_once_with("ai_base", exist_ok=True)
        mock_open.assert_called_once_with("ai_base/2025-07-26.md", "w")

        # 验证文件内容
        mock_open().write.assert_any_call(f"# AIBase Today's AI Trending ({current_date})\n\n")
        mock_open().write.assert_any_call("1. [Google Gemini Advanced Version Makes a Stunning Debut! Wins Gold Medal at IMO 2025, the New Challenger in the Mathematical Olympiad!](https://news.aibase.com/news/19838)\n")

    @patch("aibase_client.requests.get")
    @patch("aibase_client.os.makedirs")
    @patch("aibase_client.open", new_callable=unittest.mock.mock_open)
    def test_export_today_ai_trending_null(self, mock_open, mock_makedirs, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        file_path = self.client.export_today_ai_trending()

        mock_makedirs.assert_not_called()
        mock_open.assert_not_called()
        self.assertIsNone(file_path)


if __name__ == '__main__':
    unittest.main()
