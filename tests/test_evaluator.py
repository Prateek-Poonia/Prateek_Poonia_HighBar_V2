
# import pandas as pd
# from src.agents import evaluator_agent
# def test_compare_top_bottom_creatives_smoke():
#     df = pd.DataFrame({
#         'creative_message':['a','a','b','b','c','c'],
#         'impressions':[100,200,100,100,50,50],
#         'clicks':[10,30,5,5,1,2]
#     })
#     res = evaluator_agent.compare_top_bottom_creatives(df, top_pct=0.33)
#     assert 'conclusion' in res
import pandas as pd
import pytest
from src.agents import evaluator_agent

def test_compare_top_bottom_creatives_smoke():
    # Sample dataset
    df = pd.DataFrame({
        'creative_message': ['a', 'a', 'b', 'b', 'c', 'c'],
        'impressions': [100, 200, 100, 100, 50, 50],
        'clicks': [10, 30, 5, 5, 1, 2]
    })
    
    # Run evaluator
    res = evaluator_agent.compare_top_bottom_creatives(df, top_pct=0.33)
    
    # Assertions
    assert isinstance(res, dict)
    assert 'conclusion' in res
    assert 'test' in res
    assert 'confidence' in res

def test_frequency_vs_ctr_smoke():
    # Sample dataset
    df = pd.DataFrame({
        'adset_name': ['x', 'x', 'y', 'y'],
        'impressions': [100, 150, 200, 250],
        'ctr': [0.05, 0.06, 0.04, 0.03]
    })
    
    res = evaluator_agent.test_frequency_vs_ctr(df)
    
    # Assertions
    assert isinstance(res, dict)
    assert 'conclusion' in res
    assert 'statistic' in res or 'error' in res
    assert 'confidence' in res

if __name__ == "__main__":
    pytest.main([__file__])
