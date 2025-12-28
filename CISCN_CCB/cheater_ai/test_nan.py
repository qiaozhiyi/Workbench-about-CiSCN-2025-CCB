import numpy as np
import pandas as pd
from run_model_v2 import model

df_fraud = pd.read_csv('fraud_samples.csv')
sample = df_fraud.iloc[0].values[:-1].copy().astype(float)

print(f"Original probability: {model.predict_proba(sample)}")

for i in range(10):
    s = sample.copy()
    s[i] = np.nan
    p = model.predict_proba(s)
    print(f"Feature {i} set to NaN: Prob {p}")
