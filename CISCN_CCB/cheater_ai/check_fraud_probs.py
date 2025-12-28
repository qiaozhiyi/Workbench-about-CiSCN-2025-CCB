import pandas as pd
from run_model_v2 import model

df_fraud = pd.read_csv('fraud_samples.csv')
for i in range(len(df_fraud)):
    sample = df_fraud.iloc[i].values[:-1].astype(float)
    p = model.predict_proba(sample)
    if p < 0.5:
        print(f"Fraud sample {i} is approved! Prob: {p}")
