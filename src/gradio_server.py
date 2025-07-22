import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from hacker_news_client import HackerNewsClient
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
hacker_news_client = HackerNewsClient()
subscription_manager = SubscriptionManager(config.subscriptions_file)

def generate_github_report(repo, days):
    llm = LLM(config)
    report_generator = ReportGenerator(llm, config.report_types)

    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_github_report(raw_file_path)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

def generate_hacker_news_report():
    llm = LLM(config)
    report_generator = ReportGenerator(llm, config.report_types)
    markdown_file_path = hacker_news_client.export_top_stories()
    report, report_file_path = report_generator.generate_hacker_news_report(markdown_file_path)

    return report, report_file_path

with gr.Blocks() as demo:
    with gr.Tab("GitHub 项目进展报告查询"):
        gr.Markdown("# GitHub 项目进展")
        subscription_repo = gr.Dropdown(
            subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
        )
        report_period = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天")
        button = gr.Button("生成报告")
        # 设置输出组件
        markdown_output = gr.Markdown()
        file_output = gr.File(label="下载报告")
        button.click(fn=generate_github_report, inputs=[subscription_repo, report_period], outputs=[markdown_output, file_output])
    with gr.Tab("Hacker News 热点话题"):
        gr.Markdown("# Hacker News 热点话题")
        button = gr.Button("生成最新热点话题")
        # 设置输出组件
        markdown_output = gr.Markdown()
        file_output = gr.File(label="下载报告")
        button.click(fn=generate_hacker_news_report, inputs=[], outputs=[markdown_output, file_output])

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))