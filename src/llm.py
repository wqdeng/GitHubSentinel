# src/llm.py
import json
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI()
        # 加载提示词
        with open('prompts/report_prompt.txt', 'r', encoding='utf8') as prompt_file:
            self.system_prompt = prompt_file.read()

    def generate_daily_report(self, markdown_content, dry_run=False):
        messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content}
        ]
        if dry_run:
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(json.dumps(messages, indent=4, ensure_ascii=False))
            return "DRY RUN"

        print("Before call GPT")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print("After call GPT")
        print(response)
        return response.choices[0].message.content
