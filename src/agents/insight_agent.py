
def generate_hypotheses(data_summary):
    # heuristics-based hypotheses
    hyps = []
    # 1. audience fatigue if avg ctr trending down in time series
    ts = data_summary.get('time_series_sample',[])
    if len(ts)>=3:
        first = ts[0].get('ctr',0)
        last = ts[-1].get('ctr',0)
        if last < first:
            hyps.append({"id":"h1","title":"Audience fatigue","description":"CTR decreased over time while impressions stable/increasing","expected_signature":["ctr_down","impressions_up_or_stable"],"priority":1})
    # 2. creative underperformance if there are creatives with much lower ctr than median
    creatives = data_summary.get('creative_summary',[])
    if creatives:
        avg_ctrs = [c.get('avg_ctr',0) for c in creatives]
        if len(avg_ctrs)>0:
            median = sorted(avg_ctrs)[len(avg_ctrs)//2]
            low = [c for c in creatives if c.get('avg_ctr',0) < 0.6*median]
            if len(low)>0:
                hyps.append({"id":"h2","title":"Creative underperformance","description":"Some creative messages have substantially lower CTR than top creatives","expected_signature":["creative_low_ctr"],"priority":2,"examples":low[:5]})
    # 3. platform or country shift
    camps = data_summary.get('campaign_summary',[])
    if camps and len(camps)>1:
        hyps.append({"id":"h3","title":"Platform / country shift","description":"Changes in platform mix or country performance may explain ROAS moves","expected_signature":["platform_country_variation"],"priority":3})
    return {"hypotheses":hyps}
