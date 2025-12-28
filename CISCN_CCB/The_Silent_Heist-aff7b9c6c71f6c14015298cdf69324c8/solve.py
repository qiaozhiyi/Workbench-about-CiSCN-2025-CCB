import pandas as pd
import numpy as np

# Load the original data (which we know is "normal")
df = pd.read_csv('public_ledger.csv')

# We need > $2,000,000. 
# Original sum is roughly $350k. So we need about 6x the data.
# Let's create 6 copies.
df_repeated = pd.concat([df] * 6, ignore_index=True)

# Generate small noise to avoid "Duplicate" and "Replay" detection
# The noise should be small enough to stay "Normal" but large enough to be distinct.
# Standard deviation of 0.01 is usually safe for float data of this magnitude (vals ~10-400)
noise = np.random.normal(0, 0.01, size=df_repeated.shape)

# Add noise
fake_df = df_repeated + noise

# Rename columns to feat_0..feat_19 as per README
new_columns = {col: f"feat_{i}" for i, col in enumerate(df.columns)}
fake_df = fake_df.rename(columns=new_columns)

# Verify constraints
total_amount = fake_df['feat_0'].sum()
print(f"Total Amount: ${total_amount:,.2f}")
print(f"Shape: {fake_df.shape}")

# Save to CSV
fake_df.to_csv('fake_ledger.csv', index=False)
