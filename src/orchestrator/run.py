
import argparse, json, yaml, os
from src.agents import planner, data_agent, insight_agent, evaluator_agent, creative_generator
from src.utils import helpers
import pandas as pd
import numpy as np
from datetime import datetime

CONFIG_PATH = 'config/config.yaml'
def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def main(query):
    cfg = load_config()
    # 1. Data agent
    data_path = cfg.get('data_path')
    summary = data_agent.load_and_summarize(data_path, sample_mode=cfg.get('sample_mode',True), sample_size=cfg.get('sample_size',1000))
    # 2. Planner
    plan = planner.plan(query, summary, cfg)
    # 3. Insight agent
    hyps = insight_agent.generate_hypotheses(summary)
    # 4. Evaluator: load full df for tests
    df = pd.read_csv(data_path, parse_dates=['date'])
    results = []
    for h in hyps.get('hypotheses',[]):
        if h['id']=='h1':
            res = evaluator_agent.test_frequency_vs_ctr(df)
        elif h['id']=='h2':
            res = evaluator_agent.compare_top_bottom_creatives(df)
        else:
            res = {"conclusion":"inconclusive","confidence":0.0}
        out = {"hypothesis":h,"evaluation":res}
        results.append(out)
    # 5. Creative generator: find low CTR campaigns
    low_ctr_campaigns = []
    g = df.groupby('campaign_name').agg(impressions=('impressions','sum'),clicks=('clicks','sum'))
    g['ctr'] = g['clicks']/g['impressions']
    overall_ctr = g['ctr'].median() if g.shape[0]>0 else 0.02
    for idx,row in g.iterrows():
        if row['ctr'] < 0.6*overall_ctr:
            low_ctr_campaigns.append({"campaign":idx,"ctr":float(row['ctr'])})
    # prepare creative recommendations
    creatives_result = []
    if low_ctr_campaigns:
        # collect messages from top creatives
        creative_msgs = df['creative_message'].dropna().astype(str).tolist()
        top_phrases = creative_generator.extract_top_phrases(creative_msgs, ngram_range=(1,2), top_n=20)
        for c in low_ctr_campaigns:
            candidates = creative_generator.generate_candidates(c, top_phrases, num=6)
            creatives_result.append({"campaign":c['campaign'],"creative_type":"mixed","recommendations":candidates})
    # 6. write outputs
    os.makedirs('reports', exist_ok=True)
    insights = {"query":query,"plan":plan,"hypotheses":results,"generated_at":str(datetime.utcnow())}
    with open('reports/insights.json','w') as f:
        json.dump(insights,f,indent=2)
    with open('reports/creatives.json','w') as f:
        json.dump(creatives_result,f,indent=2)
    # report.md
    lines = []
    lines.append("# Automated Ads Analysis Report")
    lines.append(f"Query: {query}")
    lines.append("\n## Summary")
    lines.append("Top hypotheses and validation:")
    for r in results:
        h = r['hypothesis']
        ev = r['evaluation']
        lines.append(f"- {h.get('title')}: conclusion={ev.get('conclusion')} confidence={ev.get('confidence')}")
    lines.append("\n## Creative Recommendations")
    if creatives_result:
        for c in creatives_result:
            lines.append(f"- Campaign {c['campaign']}: {len(c['recommendations'])} candidate creatives")
    else:
        lines.append("No low-CTR campaigns detected.")
    with open('reports/report.md','w') as f:
        f.write('\n'.join(lines))
    # logs
    os.makedirs('logs', exist_ok=True)
    log = {"run_at":str(datetime.utcnow()),"query":query,"insights_path":"reports/insights.json","creatives_path":"reports/creatives.json"}
    with open('logs/run_log.json','w') as f:
        json.dump(log,f,indent=2)
    print("Done. Outputs in reports/ and logs/")
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default="Analyze ROAS drop", help='User query')
    args = parser.parse_args()
    main(args.query)
