# 导入必要的模块
from agno.agent import Agent  # Agent 类：用于创建智能体
from agno.models.openai import OpenAIChat  # OpenAI 的 GPT 模型
from agno.playground import Playground  # Playground 类：用于创建交互式界面
from agno.storage.sqlite import SqliteStorage  # SQLite 存储：用于持久化会话数据
from agno.tools.duckduckgo import DuckDuckGoTools  # DuckDuckGo 搜索工具

# ========== 配置存储路径 ==========
agent_storage: str = "tmp/agents.db"  # SQLite 数据库文件路径，用于存储所有智能体的会话

# ========== 创建网页搜索智能体 ==========
web_agent = Agent(
    name="Web Agent",  # 智能体名称
    model=OpenAIChat(id="gpt-4o"),  # 使用 OpenAI 的 GPT-4o 模型
    tools=[DuckDuckGoTools()],  # 配置 DuckDuckGo 搜索工具
    instructions=["Always include sources"],  # 指令：始终包含信息来源
    # 在 SQLite 数据库中存储智能体的会话
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    # 自动在指令中添加当前日期和时间
    add_datetime_to_instructions=True,
    # 将对话历史添加到消息中
    add_history_to_messages=True,
    # 添加最近 5 条历史响应到消息中
    num_history_responses=5,
    # 启用 Markdown 格式化输出
    markdown=True,
)

# ========== 创建新闻分析智能体 ==========
news_agent = Agent(
    name="News Agent",  # 智能体名称
    model=OpenAIChat(id="gpt-4o"),  # 使用 OpenAI 的 GPT-4o 模型
    tools=[DuckDuckGoTools(search=True, news=True)],  # 配置搜索和新闻工具
    instructions=["Always use tables to display data"],  # 指令：始终使用表格展示数据
    # 在 SQLite 数据库中存储智能体的会话
    storage=SqliteStorage(table_name="news_agent", db_file=agent_storage),
    # 自动在指令中添加当前日期和时间
    add_datetime_to_instructions=True,
    # 将对话历史添加到消息中
    add_history_to_messages=True,
    # 添加最近 5 条历史响应到消息中
    num_history_responses=5,
    # 启用 Markdown 格式化输出
    markdown=True,
)

# ========== 创建 Playground 应用 ==========
# Playground 提供一个交互式 Web 界面，用于与多个智能体交互
playground_app = Playground(agents=[web_agent, news_agent])
# 获取 FastAPI 应用实例
app = playground_app.get_app()

# ========== 主程序入口 ==========
if __name__ == "__main__":
    # 启动 Playground 服务器
    # 参数说明：
    # - "playground:app" 指定应用模块和变量名
    # - reload=True 启用热重载（代码改动时自动重启）
    playground_app.serve("playground:app", reload=True)
