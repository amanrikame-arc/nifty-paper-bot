
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NIFTY Paper Trader", layout="centered")

st.title("🤖 NIFTY Options Paper Trader")
st.warning("PAPER TRADING ONLY — no real orders are placed.")

st.write("This is your first rule-based trading simulator.")

capital = st.number_input(
    "Virtual starting capital (₹)",
    min_value=1000,
    max_value=10000,
    value=10000,
    step=1000
)

st.subheader("Trading rules")

fast = st.number_input("Fast EMA period", 2, 30, 9)
slow = st.number_input("Slow EMA period", 3, 60, 21)

stop_loss = st.slider("Stop-loss (%)", 5, 50, 20)
target = st.slider("Profit target (%)", 5, 100, 30)

st.subheader("Example signal calculator")

prices_text = st.text_area(
    "Enter sample NIFTY closing prices separated by commas",
    "26000,26010,26020,26015,26030,26045,26040,26060"
)

if st.button("Analyse sample prices"):
    try:
        prices = [
            float(x.strip())
            for x in prices_text.split(",")
            if x.strip()
        ]

        if len(prices) < slow:
            st.error(f"Enter at least {slow} prices for the selected slow EMA.")
        else:
            series = pd.Series(prices)
            fast_ema = series.ewm(
                span=int(fast), adjust=False
            ).mean()
            slow_ema = series.ewm(
                span=int(slow), adjust=False
            ).mean()

            st.metric("Latest NIFTY sample price", f"{prices[-1]:,.2f}")
            st.metric("Fast EMA", f"{fast_ema.iloc[-1]:,.2f}")
            st.metric("Slow EMA", f"{slow_ema.iloc[-1]:,.2f}")

            if fast_ema.iloc[-1] > slow_ema.iloc[-1]:
                st.success("Trend filter: bullish")
            elif fast_ema.iloc[-1] < slow_ema.iloc[-1]:
                st.info("Trend filter: bearish")
            else:
                st.info("Trend filter: neutral")

            st.caption(
                "This is a sample-price trend filter, not a trade instruction. "
                "No option prices or real market data are connected."
            )

    except ValueError:
        st.error("Please enter valid numbers separated by commas.")

st.divider()
st.subheader("Risk reminders")
st.write(f"Virtual capital: ₹{capital:,.0f}")
st.write(f"Illustrative stop-loss: {stop_loss}%")
st.write(f"Illustrative target: {target}%")
st.info(
    "This starter has no broker connection, no automatic orders, "
    "and no live market data. Results are educational only."
)
