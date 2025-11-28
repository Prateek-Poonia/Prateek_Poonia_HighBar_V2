
def plan(user_query, data_summary, config):
    # simple planner: create subtasks based on query keywords and data summary
    restated = user_query
    subtasks = [
        {"id":"t1","task":"time_series_aggregate","reason":"visualize trend and compute rolling metrics"},
        {"id":"t2","task":"creative_performance_analysis","reason":"find creatives with low CTR"},
        {"id":"t3","task":"audience_fatigue_check","reason":"compare frequency and CTR signals"},
    ]
    expected = ["date","spend","impressions","clicks","ctr","purchases","revenue","roas"]
    return {"restated_query":restated,"subtasks":subtasks,"expected_data":expected,"stop_criteria":{"min_confidence":config.get('min_confidence',0.7)}}
