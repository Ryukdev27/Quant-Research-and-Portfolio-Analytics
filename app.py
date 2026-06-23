import streamlit as st
import pandas as pd

from config import TRAIN_START, TRAIN_END, TEST_START, TEST_END
from pipeline import run_pipeline


st.set_page_config(page_title="Quant Dashboard", layout="wide")

st.title("📊 Quant Research & Portfolio Analytics")


strategy = st.sidebar.selectbox(
    "Strategy",
    ["Equal Weight", "Top Decile", "Long Short"]
)

mode = st.sidebar.selectbox(
    "Mode",
    ["Train", "Test", "Full"]
)

run = st.sidebar.button("Run")


if mode == "Train":
    start, end = TRAIN_START, TRAIN_END
elif mode == "Test":
    start, end = TEST_START, TEST_END
else:
    start, end = TRAIN_START, TEST_END


if run:

    try:
        ret, eq, bench, alpha, m = run_pipeline(start, end, strategy)
    except ValueError as e:
        st.error(f"Pipeline error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error while running pipeline: {e}")
        st.stop()

    # =========================
    # METRICS (FULL)
    # =========================
    st.subheader("📊 Metrics")

    c1, c2, c3 = st.columns(3)
    c1.metric("Sharpe", round(float(m["sharpe"]), 3))
    c2.metric("Max Drawdown", round(float(m["max_drawdown"]), 3))
    c3.metric("Final Portfolio", round(float(m["final_value"]), 3))

    c4, c5, c6 = st.columns(3)
    c4.metric("VaR", round(float(m["var"]), 4))
    c5.metric("CVaR", round(float(m["cvar"]), 4))
    c6.metric("Hit Ratio", round(float(m["hit_ratio"]), 3))

    # =========================
    # EQUITY CURVES
    # =========================
    st.subheader("📈 Equity Curve")

    df = pd.DataFrame({
        "Strategy": eq,
        "Benchmark (NIFTY 50)": bench
    }).dropna()

    if df.empty:
        st.warning("No overlapping equity data to plot.")
    else:
        st.line_chart(df)

    # =========================
    # ALPHA
    # =========================
    st.subheader("📉 Alpha Curve")

    alpha_clean = alpha.dropna()
    if alpha_clean.empty:
        st.warning("No alpha data to plot.")
    else:
        st.line_chart(alpha_clean)

    # =========================
    # SUMMARY
    # =========================
    st.subheader("📋 Summary")

    st.dataframe(pd.DataFrame([m]))

else:
    st.info("Configure your strategy and mode in the sidebar, then click **Run**.")
