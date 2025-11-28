
import numpy as np, pandas as pd
from scipy import stats

def test_frequency_vs_ctr(df):
    # requires frequency column - if not present use impressions per adset as proxy
    if 'frequency' in df.columns:
        x = df['frequency']
    else:
        # approximate frequency = impressions / (impressions per user unknown). Use impressions normalized by max per adset
        x = df.groupby('adset_name')['impressions'].transform(lambda s: s/s.max())
    y = df['ctr'].fillna(0)
    if len(x.dropna())<3:
        return {"test":"pearson","statistic":None,"p_value":None,"conclusion":"inconclusive","confidence":0.0}
    try:
        r, p = stats.pearsonr(x.fillna(0), y)
        conclusion = "supported" if (p<0.05 and r<0) else ("inconclusive" if p>=0.05 else "supported")
        confidence = min(0.99, max(0.0, abs(r)))
        return {"test":"pearson","statistic":float(r),"p_value":float(p),"conclusion":conclusion,"confidence":float(confidence)}
    except Exception as e:
        return {"test":"pearson","error":str(e),"conclusion":"inconclusive","confidence":0.0}

def compare_top_bottom_creatives(df, top_pct=0.2):
    # group by creative_message, compute ctrs
    g = df.groupby('creative_message').agg(impressions=('impressions','sum'),clicks=('clicks','sum'))
    g = g[g['impressions']>0].copy()
    g['ctr'] = g['clicks']/g['impressions']
    if g.shape[0]<2:
        return {"test":"ttest","conclusion":"inconclusive","confidence":0.0}
    cutoff = g['ctr'].quantile(1-top_pct)
    top = g[g['ctr']>=cutoff]['ctr']
    bottom = g[g['ctr']<cutoff]['ctr']
    if len(top)<2 or len(bottom)<2:
        return {"test":"ttest","conclusion":"inconclusive","confidence":0.0}
    tstat, p = stats.ttest_ind(top, bottom, equal_var=False)
    effect = top.mean() - bottom.mean()
    confidence = min(0.99, max(0.0, abs(effect)/(top.std()+bottom.std()+1e-9)))
    conclusion = "supported" if p<0.05 else "inconclusive"
    return {"test":"ttest","tstat":float(tstat),"p_value":float(p),"effect_mean_diff":float(effect),"conclusion":conclusion,"confidence":float(confidence)}
