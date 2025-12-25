# 导入必要的类型和模块
from typing import Iterator  # 用于类型提示的迭代器
from agno.agent import Agent  # Agent 类
from agno.run.agent import RunOutput  # 运行输出类
from agno.models.openai import OpenAIChat  # OpenAI 的 GPT 模型
from agno.utils.log import logger  # 日志记录工具
from agno.utils.pprint import pprint_run_response  # 格式化打印运行响应
from agno.workflow import Workflow  # 工作流基类


class CacheWorkflow(Workflow):
    """
    缓存工作流类：演示如何使用会话状态实现响应缓存
    - 第一次运行时：调用 AI 模型生成响应并缓存结果
    - 第二次运行时：直接从缓存返回结果，无需调用 AI 模型
    """
    
    # 在工作流中添加智能体作为属性
    agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))  # 创建使用 GPT-4o-mini 模型的智能体

    # 在 run() 方法中编写工作流逻辑
    def run(self, message: str) -> Iterator[RunOutput]:
        """
        执行工作流的主方法
        
        参数:
            message: 用户输入的消息
            
        返回:
            Iterator[RunOutput]: 运行输出的迭代器（支持流式输出）
        """
        logger.info(f"Checking cache for '{message}'")  # 记录日志：检查缓存
        
        # 检查输出是否已缓存
        if self.session_state.get(message):
            logger.info(f"Cache hit for '{message}'")  # 记录日志：缓存命中
            # 直接返回缓存的响应
            yield RunOutput(
                run_id=self.run_id, content=self.session_state.get(message)
            )
            return

        logger.info(f"Cache miss for '{message}'")  # 记录日志：缓存未命中
        
        # 运行智能体并流式输出响应
        yield from self.agent.run(message, stream=True)

        # 在响应输出后缓存结果
        self.session_state[message] = self.agent.run_response.content


if __name__ == "__main__":
    # ========== 主程序入口 ==========
    
    # 创建缓存工作流实例
    workflow = CacheWorkflow()
    
    # 第一次运行工作流（耗时约 1 秒，需要调用 AI 模型）
    response: Iterator[RunOutput] = workflow.run(message="Tell me a joke.")
    # 格式化打印响应
    pprint_run_response(response, markdown=True, show_time=True)
    
    # 第二次运行工作流（立即返回，因为结果已缓存）
    response: Iterator[RunOutput] = workflow.run(message="Tell me a joke.")
    # 格式化打印响应
    pprint_run_response(response, markdown=True, show_time=True)
