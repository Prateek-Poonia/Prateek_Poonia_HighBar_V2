
# import pandas as pd
# import numpy as np
# def load_and_summarize(path, sample_mode=True, sample_size=1000):
#     df = pd.read_csv(path, parse_dates=['date'])
#     if sample_mode and len(df)>sample_size:
#         df = df.sample(sample_size, random_state=42)
#     # basic validation
#     expected_cols = ['campaign_name','adset_name','date','spend','impressions','clicks','ctr','purchases','revenue','roas','creative_type','creative_message','audience_type','platform','country']
#     missing = [c for c in expected_cols if c not in df.columns]
#     schema = {"rows":len(df),"missing_columns":missing}
#     # global summary
#     global_summary = {
#         "start_date": str(df['date'].min()),
#         "end_date": str(df['date'].max()),
#         "total_spend": float(df['spend'].sum()),
#         "total_revenue": float(df['revenue'].sum()),
#         "avg_ctr": float(df['ctr'].dropna().mean()),
#         "median_roas": float(df['roas'].dropna().median())
#     }
#     # by campaign
#     camp = df.groupby('campaign_name').agg(
#         start_date=('date','min'),
#         end_date=('date','max'),
#         avg_ctr=('ctr','mean'),
#         median_roas=('roas','median'),
#         total_revenue=('revenue','sum'),
#         total_spend=('spend','sum'),
#         impressions=('impressions','sum'),
#         clicks=('clicks','sum')
#     ).reset_index()
#     campaign_summary = camp.to_dict(orient='records')
#     # creatives
#     creative = df.groupby('creative_message').agg(
#         avg_ctr=('ctr','mean'),
#         impressions=('impressions','sum'),
#         clicks=('clicks','sum'),
#         revenue=('revenue','sum')
#     ).reset_index().sort_values('avg_ctr',ascending=False)
#     creative_summary = creative.head(50).to_dict(orient='records')
#     # rolling metrics for a sample campaign
#     ts_sample = df.groupby('date').agg(impressions=('impressions','sum'),clicks=('clicks','sum'),spend=('spend','sum'),revenue=('revenue','sum')).reset_index()
#     ts_sample['ctr'] = ts_sample['clicks']/ts_sample['impressions']
#     ts_sample['roas'] = ts_sample['revenue']/(ts_sample['spend'].replace(0,1))
#     ts_sample = ts_sample.sort_values('date')
#     ts_sample['ctr_7d'] = ts_sample['ctr'].rolling(7,min_periods=1).mean()
#     ts_sample['roas_7d'] = ts_sample['roas'].rolling(7,min_periods=1).mean()
#     time_series_sample = ts_sample.tail(30).to_dict(orient='records')
#     return {"schema_validation":schema,"global_summary":global_summary,"campaign_summary":campaign_summary,"creative_summary":creative_summary,"time_series_sample":time_series_sample,"raw_df_rows":len(df)}
import pandas as pd
import numpy as np
import os

# -------------------------
# Global configuration
# -------------------------
config = {
    "data_path": "data/synthetic_fb_ads_undergarments.csv",
    "sample_size": 1000
}

# -------------------------
# Load and summarize data
# -------------------------
def load_and_summarize(path=None, sample_mode=True, sample_size=None):
    """
    Load campaign data, optionally sample it, and summarize key metrics.

    Args:
        path (str): Path to CSV file. Uses config['data_path'] if None.
        sample_mode (bool): Whether to sample data for quick testing.
        sample_size (int): Number of rows to sample if sample_mode is True.

    Returns:
        dict: Structured summary including schema validation, global, campaign,
              creative summaries, and time-series metrics.
    """
    if path is None:
        path = config.get("data_path")
    if sample_size is None:
        sample_size = config.get("sample_size", 1000)

    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found at path: {path}")

    try:
        df = pd.read_csv(path, parse_dates=['date'])
    except Exception as e:
        raise ValueError(f"Failed to load CSV: {e}")

    # Optional sampling
    if sample_mode and len(df) > sample_size:
        df = df.sample(sample_size, random_state=42)

    # -------------------------
    # Schema validation
    # -------------------------
    expected_cols = [
        'campaign_name','adset_name','date','spend','impressions','clicks','ctr','purchases',
        'revenue','roas','creative_type','creative_message','audience_type','platform','country'
    ]
    missing_cols = [c for c in expected_cols if c not in df.columns]
    schema_validation = {
        "rows": len(df),
        "missing_columns": missing_cols
    }

    # -------------------------
    # Global summary
    # -------------------------
    try:
        global_summary = {
            "start_date": str(df['date'].min()),
            "end_date": str(df['date'].max()),
            "total_spend": float(df['spend'].sum()),
            "total_revenue": float(df['revenue'].sum()),
            "avg_ctr": float(df['ctr'].dropna().mean()),
            "median_roas": float(df['roas'].dropna().median())
        }
    except KeyError as e:
        global_summary = {"error": f"Missing column: {e}"}

    # -------------------------
    # Campaign-level summary
    # -------------------------
    try:
        camp_summary = (
            df.groupby('campaign_name')
            .agg(
                start_date=('date','min'),
                end_date=('date','max'),
                avg_ctr=('ctr','mean'),
                median_roas=('roas','median'),
                total_revenue=('revenue','sum'),
                total_spend=('spend','sum'),
                impressions=('impressions','sum'),
                clicks=('clicks','sum')
            )
            .reset_index()
        )
        campaign_summary = camp_summary.to_dict(orient='records')
    except KeyError as e:
        campaign_summary = [{"error": f"Missing column: {e}"}]

    # -------------------------
    # Creative-level summary (top 50 by avg CTR)
    # -------------------------
    try:
        creative_summary = (
            df.groupby('creative_message')
            .agg(
                avg_ctr=('ctr','mean'),
                impressions=('impressions','sum'),
                clicks=('clicks','sum'),
                revenue=('revenue','sum')
            )
            .reset_index()
            .sort_values('avg_ctr', ascending=False)
            .head(50)
            .to_dict(orient='records')
        )
    except KeyError as e:
        creative_summary = [{"error": f"Missing column: {e}"}]

    # -------------------------
    # Rolling metrics over time (7-day)
    # -------------------------
    try:
        ts_sample = (
            df.groupby('date')
            .agg(
                impressions=('impressions','sum'),
                clicks=('clicks','sum'),
                spend=('spend','sum'),
                revenue=('revenue','sum')
            )
            .reset_index()
            .sort_values('date')
        )
        ts_sample['ctr'] = ts_sample['clicks'] / ts_sample['impressions'].replace(0, np.nan)
        ts_sample['roas'] = ts_sample['revenue'] / ts_sample['spend'].replace(0, np.nan)
        ts_sample['ctr_7d'] = ts_sample['ctr'].rolling(7, min_periods=1).mean()
        ts_sample['roas_7d'] = ts_sample['roas'].rolling(7, min_periods=1).mean()
        time_series_sample = ts_sample.tail(30).to_dict(orient='records')
    except KeyError as e:
        time_series_sample = [{"error": f"Missing column: {e}"}]

    # -------------------------
    # Return all summaries
    # -------------------------
    return {
        "schema_validation": schema_validation,
        "global_summary": global_summary,
        "campaign_summary": campaign_summary,
        "creative_summary": creative_summary,
        "time_series_sample": time_series_sample,
        "raw_df_rows": len(df)
    }
