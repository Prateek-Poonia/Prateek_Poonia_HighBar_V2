
import pandas as pd
from src.agents import evaluator_agent
def test_compare_top_bottom_creatives_smoke():
    df = pd.DataFrame({
        'creative_message':['a','a','b','b','c','c'],
        'impressions':[100,200,100,100,50,50],
        'clicks':[10,30,5,5,1,2]
    })
    res = evaluator_agent.compare_top_bottom_creatives(df, top_pct=0.33)
    assert 'conclusion' in res
