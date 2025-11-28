
import pandas as pd, numpy as np
def safe_pct(a,b):
    try:
        return 100.0*((a-b)/abs(b))
    except Exception:
        return None
