import pandas as pd
import os
import traceback
from src.agents import (
    data_agent,
    creative_generator,
    evaluator_agent,
    insight_agent,
    planner_agent 
)

def main(user_query, use_sample_data=True, sample_size=1000, min_confidence=0.6):
    """
    Main pipeline that orchestrates all agents:
    1. Load & summarize data
    2. Generate insights & hypotheses
    3. Generate creatives
    4. Evaluate creatives
    5. Plan next steps
    """
    reports = {
        "insights": {},
        "hypotheses": {},
        "creatives": [],
        "evaluations": [],
        "time_series_sample": [],
        "logs": []
    }

    try:
        # --- Step 1: Load and summarize data ---
        data_summary = data_agent.load_and_summarize(
            path=data_agent.config.get('data_path', 'data/synthetic_fb_ads_undergarments.csv'),
            sample_mode=use_sample_data,
            sample_size=sample_size
        )
        reports["time_series_sample"] = data_summary.get("time_series_sample", [])
        reports["logs"].append("Data loaded and summarized successfully.")

        # --- Step 2: Generate insights ---
        insights = insight_agent.generate_hypotheses(data_summary)
        reports["insights"] = insights
        reports["logs"].append(f"{len(insights.get('hypotheses', []))} insights generated.")

        # --- Step 3: Generate creatives ---
        top_phrases = creative_generator.extract_top_phrases(
            [c['creative_message'] for c in data_summary.get('creative_summary', [])]
        )
        reports["creatives"] = creative_generator.generate_candidates(
            low_ctr_campaign=None,  # optionally pass a specific campaign
            top_phrases=top_phrases,
            num=6
        )
        reports["logs"].append(f"{len(reports['creatives'])} creatives generated.")

        # --- Step 4: Evaluate creatives ---
        for creative in reports["creatives"]:
            eval_res = evaluator_agent.compare_top_bottom_creatives(
                pd.DataFrame(data_summary.get("creative_summary", []))
            )
            creative_eval = {
                "creative_id": creative.get("id"),
                "evaluation": eval_res
            }
            reports["evaluations"].append(creative_eval)
        reports["logs"].append(f"{len(reports['evaluations'])} creative evaluations completed.")

        # --- Step 5: Plan next steps ---
        plan_res = planner_agent.plan(user_query, data_summary, data_agent.config)
        reports["hypotheses"] = plan_res
        reports["logs"].append("Planning step completed.")

    except Exception as e:
        error_msg = f"Pipeline error: {e}\n{traceback.format_exc()}"
        reports["logs"].append(error_msg)

    # --- Convert sets to lists for JSON safety ---
    def convert(o):
        if isinstance(o, set):
            return list(o)
        return o

    return reports
