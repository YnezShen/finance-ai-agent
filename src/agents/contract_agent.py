import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# 1. 定义结构化输出数据模型 (Pydantic Schema)
class ContractRiskOutput(BaseModel):
    party_a: str = Field(description="甲方名称")
    party_b: str = Field(description="乙方名称")
    contract_amount: float = Field(description="合同总金额（元）")
    credit_period_days: int = Field(description="约定账期天数")
    has_risk_clause: bool = Field(description="是否存在高风险条款")
    risk_summary: str = Field(description="风险摘要及审核建议")


class ContractAgent:

    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        """初始化 Contract-Agent"""
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.0,  # 设为 0 极力降低随机性与幻觉
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
        ).with_structured_output(ContractRiskOutput)

        self.prompt_template = PromptTemplate(
            template="""
            你是一名专业的财务风控专家。请从以下合同文本中精确提取关键要素与风险点。
            如果文中未直接提到某个数值，请不要臆造。
            
            合同文本内容：
            {contract_text}
            """,
            input_variables=["contract_text"],
        )

        self.chain = self.prompt_template | self.llm

    def analyze_contract(self, contract_text: str) -> ContractRiskOutput:
        """执行合同解析与风控判断"""
        try:
            response = self.chain.invoke({"contract_text": contract_text})
            return response
        except Exception as e:
            print(f"[Error] 合同解析失败: {str(e)}")
            return None


# 测试运行代码
if __name__ == "__main__":
    mock_contract = """
    甲方：苏州某精密机械制造有限公司
    乙方：上海某自动化设备有限公司
    合同总价款为人民币 500,000 元整。
    付款方式：合同签署后支付 30% 预付款，发货后 60 天内付清余款。
    违约责任：如乙方逾期交货，按日支付合同总额 0.05% 的违约金。争议由甲方所在地法院管辖。
    """

    agent = ContractAgent()
    result = agent.analyze_contract(mock_contract)
    if result:
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
