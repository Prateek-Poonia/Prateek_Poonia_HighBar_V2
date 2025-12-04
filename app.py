import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from src.run import main  # Make sure src/__init__.py exists

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="Kasparro FB Analyst", layout="wide")
st.title("Kasparro — Agentic Facebook Performance Analyst")

# -------------------------
# Sidebar Inputs
# -------------------------
st.sidebar.header("Input Options")
metric_analysis = st.sidebar.text_input(
    "Enter analysis query:", "Analyze ROAS drop in last 7 days"
)
use_sample = st.sidebar.checkbox("Use sample data", value=True)
sample_size = st.sidebar.number_input(
    "Sample size", min_value=100, max_value=10000, value=1000
)
min_confidence = st.sidebar.slider(
    "Minimum confidence for hypotheses", 0.0, 1.0, 0.6
)

# Create folder to save reports and logs
os.makedirs("reports", exist_ok=True)

# -------------------------
# Helper: Make JSON serializable
# -------------------------
def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, set):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray, pd.Series)):
        return make_json_safe(obj.tolist())
    elif isinstance(obj, pd.DataFrame):
        return make_json_safe(obj.to_dict(orient='records'))
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    else:
        return obj

# -------------------------
# Run Agent Pipeline
# -------------------------
if st.button("Run Analysis"):
    with st.spinner("Generating insights, hypotheses, creatives, evaluations, and charts..."):
        try:
            reports = main(
                user_query=metric_analysis,
                use_sample_data=use_sample,
                sample_size=sample_size,
                min_confidence=min_confidence
            )
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            reports = {}

    # -------------------------
    # Display Insights
    # -------------------------
    insights_data = reports.get("insights", {})
    insights = insights_data.get("hypotheses", []) if isinstance(insights_data, dict) else []
    if insights:
        st.subheader("Insights")
        st.dataframe(pd.DataFrame(insights))
    else:
        st.info("No insights generated for this query.")

    # -------------------------
    # Display Creative Suggestions
    # -------------------------
    creatives = reports.get("creatives", [])
    if creatives:
        st.subheader("Creative Suggestions")
        st.dataframe(pd.DataFrame(creatives))
    else:
        st.info("No creative suggestions available.")

    # -------------------------
    # Display Hypotheses
    # -------------------------
    hypotheses_data = reports.get("hypotheses", {})
    hypotheses = hypotheses_data.get("hypotheses", []) if isinstance(hypotheses_data, dict) else []
    if hypotheses:
        st.subheader("Hypotheses & Confidence")
        st.dataframe(pd.DataFrame(hypotheses))
    else:
        st.info("No hypotheses generated.")

    # -------------------------
    # Display Evaluations
    # -------------------------
    evaluations = reports.get("evaluations", [])
    if evaluations:
        st.subheader("Evaluations / Validation")
        st.dataframe(pd.DataFrame(evaluations))
    else:
        st.info("No evaluations generated.")

    # -------------------------
    # Display Time Series Charts
    # -------------------------
    time_series = reports.get("time_series_sample", [])
    if time_series:
        try:
            df_ts = pd.DataFrame(time_series)
            if "date" in df_ts.columns:
                df_ts['date'] = pd.to_datetime(df_ts['date'])
                df_ts = df_ts.sort_values('date')

                if "ctr" in df_ts.columns:
                    st.subheader("CTR Trend (Last 30 Days)")
                    st.line_chart(df_ts.set_index("date")["ctr"])

                if "roas" in df_ts.columns:
                    st.subheader("ROAS Trend (Last 30 Days)")
                    st.line_chart(df_ts.set_index("date")["roas"])
        except Exception as e:
            st.warning(f"Time series chart could not be displayed: {e}")
    else:
        st.info("No time series data available.")

    # -------------------------
    # Display Agent Logs
    # -------------------------
    logs = reports.get("logs", [])
    if logs:
        st.subheader("Agent Logs")
        for log in logs:
            st.text(log)
    else:
        st.info("No agent logs available.")

    # -------------------------
    # Save JSON report safely
    # -------------------------
    report_file = os.path.join("reports", "latest_report.json")
    try:
        with open(report_file, "w") as f:
            json.dump(make_json_safe(reports), f, indent=2)
        st.success(f"Report saved to {report_file}")
    except Exception as e:
        st.error(f"Failed to save report: {e}")
