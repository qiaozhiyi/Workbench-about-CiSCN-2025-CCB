import numpy as np
import pandas as pd
from run_model import model

df_fraud = pd.read_csv('fraud_samples.csv')
sample = df_fraud.iloc[0].values[:-1].copy()

# Features to check: 3, 4, 5, 6, 7, 8, 9
for i in [3, 4, 5, 6, 7, 8, 9]:
    # What values to try?
    # Maybe 0, 1, -1, 1337, etc.
    # Or values that appear in the split conditions.
    pass

# Let's try setting each feature to 0
for i in range(10):
    s = sample.copy()
    s[i] = 0
    p = model.predict_proba(s)
    if p < 0.5:
        print(f"Feature {i} set to 0 triggers backdoor! Prob: {p}")

# Let's try setting each feature to a very large value
for i in range(10):
    s = sample.copy()
    s[i] = 999999
    p = model.predict_proba(s)
    if p < 0.5:
        print(f"Feature {i} set to 999999 triggers backdoor! Prob: {p}")

# Let's try values from the split conditions of the trees that used feature 3 or 5
# Tree 37 used feature 3 with cond 1.98181653
s = sample.copy()
s[3] = 1.981817
p = model.predict_proba(s)
print(f"Feature 3 set to 1.981817: {p}")
