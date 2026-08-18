# finance-ai-agent
An AI-powered accounts receivable risk analysis and contract review system.
ai-ar-collection-risk-system/
├── .gitignore               # 忽略敏感文件和配置
├── README.md                # 核心项目说明文档
├── requirements.txt         # Python 依赖包清单
├── docs/                    # 存放架构图、工作流截图
│   ├── workflow_contract.jpg
│   ├── workflow_risk.jpg
│   └── multi_agent_coze.jpg
├── data/                    # 示例数据（必须进行脱敏处理！）
│   └── mock_contracts/      # 样例合同 PDF/Word
├── src/                     # 源码（如果写了纯 Python/LangChain 脚本）
│   ├── agents/              # Contract-Agent & Risk-Agent 代码
│   ├── rpa/                 # 影刀 RPA 相关的 SQL 提取或脚本
│   └── utils/               # 数据清洗 (Pandas) / Prompt 模版
└── prompts/                 # 独立存放精调后的结构化 Prompt
    ├── contract_extraction.txt
    └── risk_assessment.txt
