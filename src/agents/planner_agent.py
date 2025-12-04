
# def plan(user_query, data_summary, config):
#     # simple planner: create subtasks based on query keywords and data summary
#     restated = user_query
#     subtasks = [
#         {"id":"t1","task":"time_series_aggregate","reason":"visualize trend and compute rolling metrics"},
#         {"id":"t2","task":"creative_performance_analysis","reason":"find creatives with low CTR"},
#         {"id":"t3","task":"audience_fatigue_check","reason":"compare frequency and CTR signals"},
#     ]
#     expected = ["date","spend","impressions","clicks","ctr","purchases","revenue","roas"]
#     return {"restated_query":restated,"subtasks":subtasks,"expected_data":expected,"stop_criteria":{"min_confidence":config.get('min_confidence',0.7)}}
def plan(user_query, data_summary, config):
    """
    Generate a structured plan for analyzing marketing metric changes.

    Args:
        user_query (str): The analyst or system query to guide planning.
        data_summary (dict): Output from data_agent containing campaign, creative, and time-series summaries.
        config (dict): Configuration settings including min_confidence and thresholds.

    Returns:
        dict: Structured plan with subtasks, expected data, and stop criteria.
    """

    # Restate the user query for clarity
    restated_query = user_query.strip()

    # Define subtasks with reasoning and priority
    subtasks = [
        {
            "id": "t1",
            "task": "time_series_aggregate",
            "reason": "Visualize trends, compute rolling 7-day metrics, detect anomalies",
            "priority": 1
        },
        {
            "id": "t2",
            "task": "creative_performance_analysis",
            "reason": "Identify low-performing creatives and quantify CTR/ROAS deviations",
            "priority": 2
        },
        {
            "id": "t3",
            "task": "audience_fatigue_check",
            "reason": "Compare frequency and CTR signals to detect audience fatigue or saturation",
            "priority": 3
        },
        {
            "id": "t4",
            "task": "platform_country_shift",
            "reason": "Check campaign performance across platforms and countries for shifts",
            "priority": 4
        }
    ]

    # Define expected columns for downstream processing
    expected_data = [
        "date", "spend", "impressions", "clicks", "ctr",
        "purchases", "revenue", "roas", "creative_message",
        "campaign_name", "adset_name", "platform", "country"
    ]

    # Stop criteria driven by config
    stop_criteria = {
        "min_confidence": config.get("min_confidence", 0.7),
        "max_missing_columns_pct": config.get("max_missing_columns_pct", 0.1)
    }

    return {
        "restated_query": restated_query,
        "subtasks": subtasks,
        "expected_data": expected_data,
        "stop_criteria": stop_criteria
    }
