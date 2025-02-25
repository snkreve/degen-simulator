import numpy as np
import pandas as pd
import streamlit as st
import time
import random

def casino_simulator(
    num_players=1,
    house_edge=0.01,
    bonuses={"Weekly Bonus": 0.08, "Monthly Bonus": 0.05, "Rakeback": 0.10},
    loseback=0.02
):
    """
    Gambler Simulator
    """
    np.random.seed(42)
    deposit_amounts = np.random.lognormal(mean=6, sigma=1, size=num_players)
    wager_multipliers = np.random.choice([10, 100, 1000], size=num_players, p=[0.5, 0.3, 0.2])
    wager_amounts = deposit_amounts * wager_multipliers
    expected_losses = wager_amounts * house_edge
    actual_losses = np.random.normal(loc=expected_losses, scale=expected_losses * 0.5)
    actual_losses = np.maximum(actual_losses, 0)
    bonus_results = {name: wager_amounts * house_edge * percent for name, percent in bonuses.items()}
    loseback_bonus = actual_losses * loseback
    total_bonus = sum(bonus_results.values()) + loseback_bonus
    actual_profit = actual_losses - total_bonus
    expected_profit = expected_losses - sum(bonus_results.values())
    actual_rtp = 1 - (actual_profit.sum() / wager_amounts.sum())
    expected_rtp = 1 - house_edge
    profitable_players = (actual_profit < 0).sum()
    losing_players = num_players - profitable_players
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

st.set_page_config(page_title="Gambler Simulator", layout="wide")
st.image("https://i.imgur.com/meqsjO3.png", width=300)
st.markdown("<h4 style='text-align: center;'>Can't Yield? Bet Everything Today! 🎰😆</h10>", unsafe_allow_html=True)
st.title("Gambler Simulator - Online Version")
num_players = st.number_input("Number of Players", min_value=1, max_value=100000, value=10000, step=1)
house_edge = st.number_input("House Edge", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
loseback = st.number_input("Loseback Percentage", min_value=0.0, max_value=0.2, value=0.02, step=0.01)

st.subheader("Bonus Settings")
weekly_bonus = st.slider("Weekly Bonus (%)", 0, 20, 8) / 100
monthly_bonus = st.slider("Monthly Bonus (%)", 0, 20, 5) / 100
rakeback = st.slider("Rakeback (%)", 0, 20, 10) / 100
bonuses = {"Weekly Bonus": weekly_bonus, "Monthly Bonus": monthly_bonus, "Rakeback": rakeback}

if st.button("Run Simulation"):
    with st.spinner("Rolling the dice..."):
        time.sleep(2)
    results_df = casino_simulator(num_players, house_edge, bonuses, loseback)
    st.write(results_df)
    csv_buffer = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Simulation Results (CSV)", csv_buffer, file_name="casino_simulation_results.csv", mime="text/csv")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Casino Simulator - How It Works")
    st.write("""
    This Casino Simulator models a real-world gambling environment by simulating thousands of players with varying betting behaviors. It calculates casino profits, player winnings, and overall Return to Player (RTP) based on defined game conditions.

    ### How It Works
    **Player Simulation**  
    - Each player starts with a random deposit amount based on a log-normal distribution.
    - Players place bets at multipliers of 10x, 100x, or 1000x of their deposit.

    **House Edge Calculation**  
    - Every bet has a defined House Edge (default 1%), representing the casino's statistical advantage.
    - Expected losses are calculated as wager * house edge.

    **Actual Game Outcomes**  
    - Actual losses are randomly distributed around the expected value using a normal distribution.
    - Some players may lose less or more than expected due to natural variance.

    **Bonus System**  
    - Weekly Bonus, Monthly Bonus, Rakeback: Calculated as wager * house edge * bonus percentage.
    - Loseback: Based on actual player losses and refunded at a specified percentage.

    **Casino Profit & RTP Calculation**  
    - The total casino profit is calculated as actual losses - total bonuses paid.
    - RTP (Return to Player) is derived from the total winnings distributed to players.

    **Key Features**
    ✅ Supports custom number of players  
    ✅ Adjustable House Edge, Bonuses, and Loseback  
    ✅ Provides a detailed summary of casino performance  
    ✅ CSV export option for further analysis  

    **Summary Calculation Formula**
    - **Expected Loss** = Wager * House Edge
    - **Actual Loss** = Randomized loss (simulated variance)
    - **Bonus Calculation** = Wager * House Edge * Bonus Percentage
    - **Loseback Calculation** = Actual Loss * Loseback Percentage
    - **Total Bonus Paid** = Bonus + Loseback
    - **Expected Profit** = Expected Loss - Bonus
    - **Actual Profit** = Actual Loss - Total Bonus
    - **Expected RTP** = 1 - House Edge
    - **Actual RTP** = 1 - (Actual Profit / Wager)
    """)

with col2:
    st.image("https://i.imgur.com/NiEALyA.gif", width=500)
