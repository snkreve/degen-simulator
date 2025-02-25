import numpy as np
import pandas as pd
import streamlit as st
import io

def casino_simulator(
    num_players=10000,
    house_edge=0.01,
    bonuses={"Weekly Bonus": 0.08, "Monthly Bonus": 0.05, "Rakeback": 0.10},
    loseback=0.02
):
    """
    赌场经营模拟器
    :param num_players: 模拟玩家数量
    :param house_edge: 赌场 House Edge（默认 1%）
    :param bonuses: 不同 Bonus 及其百分比（以 wager * HE 计算）
    :param loseback: 亏损返还比例（基于实际损失）
    """
    np.random.seed(42)
    
    # 生成玩家充值金额（对数正态分布，模拟小额到大额充值）
    deposit_amounts = np.random.lognormal(mean=6, sigma=1, size=num_players)
    
    # 生成 wager 倍数（随机分布在 10 倍, 100 倍, 1000 倍之间）
    wager_multipliers = np.random.choice([10, 100, 1000], size=num_players, p=[0.5, 0.3, 0.2])
    
    # 计算 wager 金额
    wager_amounts = deposit_amounts * wager_multipliers
    
    # 计算期望损失
    expected_losses = wager_amounts * house_edge
    
    # 模拟实际损失（正态分布，均值为 House Edge 1%）
    actual_losses = np.random.normal(loc=expected_losses, scale=expected_losses * 0.5)
    actual_losses = np.maximum(actual_losses, 0)  # 避免负损失
    
    # 计算各项 Bonus
    bonus_results = {name: wager_amounts * house_edge * percent for name, percent in bonuses.items()}
    
    # 计算 Loseback
    loseback_bonus = actual_losses * loseback
    
    # 计算总奖金发放
    total_bonus = sum(bonus_results.values()) + loseback_bonus
    
    # 计算赌场利润
    actual_profit = actual_losses - total_bonus
    expected_profit = expected_losses - sum(bonus_results.values())
    
    # 计算 RTP
    actual_rtp = 1 - (actual_profit.sum() / wager_amounts.sum())
    expected_rtp = 1 - house_edge
    
    # 计算盈利玩家
    profitable_players = (actual_profit < 0).sum()
    losing_players = num_players - profitable_players
    
    # 结果汇总
    results = {
        "Total Players": num_players,
        "Total Wager": wager_amounts.sum(),
        "Total Expected Loss": expected_losses.sum(),
        "Total Actual Loss": actual_losses.sum(),
        "Total Bonuses Paid": total_bonus.sum(),
        "Total Expected Profit": expected_profit.sum(),
        "Total Actual Profit": actual_profit.sum(),
        "Expected RTP": expected_rtp,
        "Actual RTP": actual_rtp,
        "Profitable Players": profitable_players,
        "Losing Players": losing_players,
        "Profitable Player Percentage": (profitable_players / num_players) * 100
    }
    
    return pd.DataFrame([results])

# Streamlit UI
st.set_page_config(page_title="赌场模拟经营器", layout="wide")
st.title("赌场模拟经营器 - 在线版")
num_players = st.number_input("模拟玩家数量", min_value=1000, max_value=100000, value=10000, step=1000)
house_edge = st.number_input("House Edge (赌场优势)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
loseback = st.number_input("Loseback (亏损返还比例)", min_value=0.0, max_value=0.2, value=0.02, step=0.01)

st.subheader("Bonus 设定")
weekly_bonus = st.slider("Weekly Bonus (%)", 0, 20, 8) / 100
monthly_bonus = st.slider("Monthly Bonus (%)", 0, 20, 5) / 100
rakeback = st.slider("Rakeback (%)", 0, 20, 10) / 100
bonuses = {"Weekly Bonus": weekly_bonus, "Monthly Bonus": monthly_bonus, "Rakeback": rakeback}

if st.button("运行模拟"):
    results_df = casino_simulator(num_players, house_edge, bonuses, loseback)
    st.write(results_df)

    # 允许用户下载 CSV（修正 Streamlit Cloud 兼容性）
    csv_buffer = io.BytesIO()
    results_df.to_csv(csv_buffer, index=False)
    st.download_button("下载模拟结果 CSV", csv_buffer.getvalue(), file_name="casino_simulation_results.csv", mime="text/csv")
