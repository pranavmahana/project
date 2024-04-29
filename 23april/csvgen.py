import pandas as pd
import numpy as np

# Generate random data
num_samples = 100000
num_channels = 12  # 24 channels can also be used

# Create time column
time = np.linspace(0, 60, num_samples)

# Create data for channels
channels_data = {}
for i in range(num_channels):
    channel_name = f"Channel_{i + 1}"
    channel_data = np.random.rand(num_samples) * 100  # Random values
    channels_data[channel_name] = channel_data

# Create DataFrame
df = pd.DataFrame(data=channels_data)
df.insert(0, "Time", time)

# Save to CSV
df.to_csv("vibration_data.csv", index=False)

print("CSV file generated successfully!")
