import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

# 创建Gradio界面
progress_report = gr.Interface(
    fn=export_progress_by_date_range,  # 指定界面调用的函数
    inputs=[
        gr.Dropdown(
            subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
        ),  # 下拉菜单选择订阅的GitHub项目
        gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天"),
        # 滑动条选择报告的时间范围
    ],
    submit_btn="查询",
    clear_btn="清空",
    outputs=[gr.Markdown(), gr.File(label="下载报告")],  # 输出格式：Markdown文本和文件下载
)

def save_subscription(repo):
    if not repo:
        return "请输入要订阅的仓库，再点击添加按钮！"

    if "/" not in repo:
        return "要订阅的仓库格式不正确，请重新输入！"

    if repo not in subscription_manager.list_subscriptions():
        subscription_manager.add_subscription(repo)
        return f"新增 [{repo}] 仓库订阅成功！"

    return f"仓库 [{repo}] 已订阅！"

def delete_subscription(repo):
    if not repo:
        return "请选择/输入要订阅的仓库，再点击添加按钮！"

    if repo in subscription_manager.list_subscriptions():
        subscription_manager.remove_subscription(repo)
        return f"删除 [{repo}] 仓库订阅成功！"

    return f"仓库 [{repo}] 没有订阅！"

with gr.Blocks() as subscriptions_maintenance:
    subscription_repo = gr.Dropdown(
        subscription_manager.list_subscriptions(), label="订阅仓库", value="", allow_custom_value=True, info="仓库owner/仓库名称"
    )
    maintenance_result = gr.Textbox("", label="维护结果")

    add_subscription_btn = gr.Button("新增")
    delete_subscription_btn = gr.Button("删除")
    add_subscription_btn.click(fn=save_subscription, inputs=[subscription_repo], outputs=[maintenance_result], api_name="add_subscription")
    delete_subscription_btn.click(fn=delete_subscription, inputs=[subscription_repo], outputs=[maintenance_result], api_name="delete_subscription")

demo = gr.TabbedInterface([progress_report, subscriptions_maintenance], ["报告查询", "订阅列表维护"])

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))