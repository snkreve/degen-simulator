import numpy as np
import pandas as pd
import streamlit as st

def casino_simulator(
    num_players=1,
    house_edge=0.01,
    bonuses={"Weekly Bonus": 0.08, "Monthly Bonus": 0.05, "Rakeback": 0.10},
    loseback=0.02
):
    """
    Casino Simulator
    :param num_players: Number of simulated players
    :param house_edge: House Edge (default 1%)
    :param bonuses: Different bonus types calculated as wager * HE * percentage
    :param loseback: Loss rebate percentage (based on actual losses)
    """
    np.random.seed(42)
    
    # Generate deposit amounts (log-normal distribution simulating small to large deposits)
    deposit_amounts = np.random.lognormal(mean=6, sigma=1, size=num_players)
    
    # Generate wager multipliers (random choice of 10x, 100x, 1000x)
    wager_multipliers = np.random.choice([10, 100, 1000], size=num_players, p=[0.5, 0.3, 0.2])
    
    # Calculate wager amounts
    wager_amounts = deposit_amounts * wager_multipliers
    
    # Calculate expected losses
    expected_losses = wager_amounts * house_edge
    
    # Simulate actual losses (normal distribution with mean at House Edge 1%)
    actual_losses = np.random.normal(loc=expected_losses, scale=expected_losses * 0.5)
    actual_losses = np.maximum(actual_losses, 0)  # Prevent negative losses
    
    # Calculate Bonuses
    bonus_results = {name: wager_amounts * house_edge * percent for name, percent in bonuses.items()}
    
    # Calculate Loseback
    loseback_bonus = actual_losses * loseback
    
    # Calculate total bonuses paid
    total_bonus = sum(bonus_results.values()) + loseback_bonus
    
    # Calculate casino profit
    actual_profit = actual_losses - total_bonus
    expected_profit = expected_losses - sum(bonus_results.values())
    
    # Calculate RTP
    actual_rtp = 1 - (actual_profit.sum() / wager_amounts.sum())
    expected_rtp = 1 - house_edge
    
    # Count profitable players
    profitable_players = (actual_profit < 0).sum()
    losing_players = num_players - profitable_players
    
    # Summary results
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
st.set_page_config(page_title="Casino Simulator", layout="wide")
st.image("https://imgur.com/aaA0DRe.png", width=200)
st.title("Casino Simulator - Online Version")
num_players = st.number_input("Number of Players", min_value=1, max_value=100000, value=10000, step=1)
house_edge = st.number_input("House Edge", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
loseback = st.number_input("Loseback Percentage", min_value=0.0, max_value=0.2, value=0.02, step=0.01)

st.subheader("Bonus Settings")
weekly_bonus = st.slider("Weekly Bonus (%)", 0, 20, 8) / 100
monthly_bonus = st.slider("Monthly Bonus (%)", 0, 20, 5) / 100
rakeback = st.slider("Rakeback (%)", 0, 20, 10) / 100
bonuses = {"Weekly Bonus": weekly_bonus, "Monthly Bonus": monthly_bonus, "Rakeback": rakeback}

if st.button("Run Simulation"):
    results_df = casino_simulator(num_players, house_edge, bonuses, loseback)
    st.write(results_df)

    # Allow user to download CSV
    csv_buffer = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Simulation Results (CSV)", csv_buffer, file_name="casino_simulation_results.csv", mime="text/csv")

st.subheader("Casino Simulator - How It Works")
st.write("""
### Summary Calculation Formulas
- **Total Expected Loss** = ∑ (Wager × House Edge)
- **Total Actual Loss** = Randomized loss based on normal distribution around expected loss
- **Total Bonuses Paid** = ∑ (Wager × House Edge × Bonus Percentage) + ∑ (Actual Loss × Loseback)
- **Total Expected Profit** = Total Expected Loss - Total Bonuses Paid
- **Total Actual Profit** = Total Actual Loss - Total Bonuses Paid
- **Expected RTP** = 1 - House Edge
- **Actual RTP** = 1 - (Total Actual Profit / Total Wager)
- **Profitable Player Percentage** = (Profitable Players / Total Players) × 100

**Cybet - Clear Your Mfer's Win**
""")
