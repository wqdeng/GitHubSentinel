# src/report_generator.py

import os
from datetime import date, timedelta
from logger import LOG  # 导入日志模块，用于记录日志信息

class ReportGenerator:
    def __init__(self, llm, report_types):
        self.llm = llm  # 初始化时接受一个LLM实例，用于后续生成报告
        self.report_types = report_types
        self.prompts = {}

        ## 根据report_types加载prompts
        for report_type in self.report_types:
            prompt_file = f"prompts/{report_type}_prompt.txt"
            if not os.path.exists(prompt_file):
                LOG.info(f"{report_type} prompt file {prompt_file} not found.")
                raise FileNotFoundError(f"{report_type} prompt file {prompt_file} not found.")
            with open(prompt_file, "r", encoding="utf8") as prompt_file:
                self.prompts[report_type] = prompt_file.read()

    def generate_github_report(self, markdown_file_path):
        # 读取Markdown文件并使用LLM生成日报
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        github_prompt = self.prompts["github"]
        report = self.llm.generate_report(github_prompt, markdown_content)  # 调用LLM生成报告

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)  # 写入生成的报告

        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")

        return report, report_file_path

    def generate_hacker_news_report(self, markdown_file_path):
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        hacker_news_prompt = self.prompts['hacker_news']
        report = self.llm.generate_report(hacker_news_prompt, markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        LOG.info(f"Hacker News 热点话题报告已保存到 {report_file_path}")
        return report, report_file_path

    def generate_report_by_date_range(self, markdown_file_path, days):
        # 生成特定日期范围的报告，流程与日报生成类似
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + f"_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)
        
        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")

        return report, report_file_path

