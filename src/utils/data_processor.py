import numpy as np
import pandas as pd


def calculate_ar_risk_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """计算应收账款（AR）指标与客户动态风险分级

    :param df: 包含客户交易与回款记录的 DataFrame
               必须字段: ['client_id', 'invoice_amount', 'due_date',
               'actual_payment_date', 'overdue_days']
    :return: 增加风险标签后的 DataFrame
    """
    df = df.copy()

    # 1. 计算实际回款周期与超期天数
    df["due_date"] = pd.to_datetime(df["due_date"])
    df["actual_payment_date"] = pd.to_datetime(df["actual_payment_date"])

    # 未回款的以今天计算逾期
    today = pd.Timestamp.today()
    df["effective_payment_date"] = df["actual_payment_date"].fillna(today)
    df["calculated_overdue_days"] = (
        df["effective_payment_date"] - df["due_date"]
    ).dt.days

    # 2. 客户粒度汇总分析 (计算重构后的精准回款天数 & 逾期率)
    client_summary = (
        df.groupby("client_id")
        .agg(
            total_invoice=("invoice_amount", "sum"),
            avg_overdue_days=("calculated_overdue_days", "mean"),
            max_overdue_days=("calculated_overdue_days", "max"),
            unpaid_count=("actual_payment_date", lambda x: x.isnull().sum()),
        )
        .reset_index()
    )

    # 3. 动态风险规则分级 (Rule-based Risk Classification)
    conditions = [
        (client_summary["max_overdue_days"] > 90)
        | (client_summary["unpaid_count"] >= 3),
        (client_summary["max_overdue_days"] > 30)
        | (client_summary["avg_overdue_days"] > 15),
        (client_summary["max_overdue_days"] <= 30),
    ]
    risk_levels = ["High Risk (高风险)", "Medium Risk (中风险)", "Low Risk (低风险)"]

    client_summary["risk_level"] = np.select(
        conditions, risk_levels, default="Unknown"
    )

    return client_summary


if __name__ == "__main__":
    # 模拟 ERP 提取的数据
    data = {
        "client_id": ["C001", "C001", "C002", "C003"],
        "invoice_amount": [50000, 30000, 120000, 80000],
        "due_date": ["2026-01-01", "2026-02-01", "2026-01-15", "2026-03-01"],
        "actual_payment_date": [
            "2026-01-10",
            None,
            "2026-04-20",
            "2026-03-02",
        ],
    }
    df_raw = pd.DataFrame(data)
    result_df = calculate_ar_risk_metrics(df_raw)
    print(result_df)
