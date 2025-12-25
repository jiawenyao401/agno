# 导入必要的模块
from agno.agent import Agent  # Agent 类：用于创建单个智能体
from agno.models.anthropic import Claude  # Claude 模型：Anthropic 的 AI 模型
from agno.models.openai import OpenAIChat  # OpenAI 模型：OpenAI 的 GPT 系列模型
from agno.team.team import Team  # Team 类：用于创建多智能体团队
from agno.tools.duckduckgo import DuckDuckGoTools  # DuckDuckGo 搜索工具
from agno.tools.reasoning import ReasoningTools  # 推理工具：用于复杂推理任务

# ========== 创建网页搜索智能体 ==========
web_agent = Agent(
    name="Web Search Agent",  # 智能体名称
    role="Handle web search requests and general research",  # 智能体角色描述
    model=OpenAIChat(id="gpt-4.1"),  # 使用 OpenAI 的 GPT-4.1 模型
    tools=[DuckDuckGoTools()],  # 配置 DuckDuckGo 搜索工具
    instructions="Always include sources",  # 指令：始终包含信息来源
    add_datetime_to_instructions=True,  # 自动在指令中添加当前日期时间
)

# ========== 创建新闻分析智能体 ==========
news_agent = Agent(
    name="News Agent",  # 智能体名称
    role="Handle news requests and current events analysis",  # 智能体角色：处理新闻和时事分析
    model=OpenAIChat(id="gpt-4.1"),  # 使用 OpenAI 的 GPT-4.1 模型
    tools=[DuckDuckGoTools(search=True, news=True)],  # 配置搜索和新闻工具
    instructions=[
        "Use tables to display news information and findings.",  # 使用表格展示新闻信息
        "Clearly state the source and publication date.",  # 清楚地标注来源和发布日期
        "Focus on delivering current and relevant news insights.",  # 专注于提供当前和相关的新闻见解
    ],
    add_datetime_to_instructions=True,  # 自动添加当前日期时间到指令
)

# ========== 创建多智能体研究团队 ==========
reasoning_research_team = Team(
    name="Reasoning Research Team",  # 团队名称
    mode="coordinate",  # 协调模式：团队成员协作完成任务
    model=Claude(id="claude-sonnet-4-20250514"),  # 使用 Claude 模型作为团队协调者（推理能力强）
    members=[web_agent, news_agent],  # 团队成员：包含网页搜索和新闻分析智能体
    tools=[ReasoningTools(add_instructions=True)],  # 配置推理工具以支持复杂推理
    instructions=[
        "Collaborate to provide comprehensive research and news insights",  # 协作提供全面的研究和新闻见解
        "Consider both current events and trending topics",  # 考虑当前事件和热门话题
        "Use tables and charts to display data clearly and professionally",  # 使用表格和图表专业地展示数据
        "Present findings in a structured, easy-to-follow format",  # 以结构化、易于理解的格式呈现发现
        "Only output the final consolidated analysis, not individual agent responses",  # 仅输出最终综合分析，不输出单个智能体的响应
    ],
    markdown=True,  # 启用 Markdown 格式输出
    show_members_responses=True,  # 显示团队成员的响应
    enable_agentic_context=True,  # 启用智能体上下文
    add_datetime_to_instructions=True,  # 自动添加当前日期时间到指令
    success_criteria="The team has provided a complete research analysis with data, visualizations, trend assessment, and actionable insights supported by current information and reliable sources.",  # 成功标准：提供完整的研究分析
)

# ========== 主程序入口 ==========
if __name__ == "__main__":
    # 调用团队处理用户查询
    reasoning_research_team.print_response(
        """Research and compare recent developments in renewable energy:
        1. Get latest news about renewable energy innovations
        2. Analyze recent developments in the renewable sector
        3. Compare different renewable energy technologies
        4. Recommend future trends to watch""",  # 用户查询：研究可再生能源的最新发展
        stream=True,  # 启用流式输出（实时显示结果）
        show_full_reasoning=True,  # 显示完整的推理过程
        stream_intermediate_steps=True,  # 流式显示中间步骤
    )
