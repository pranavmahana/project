import numpy as np
import pandas as pd

def generate_random_data(num_samples, num_channels):
    # Sampling rate (Hz)
    sampling_rate = 25000
    
    # Generate time array
    time_array = np.arange(num_samples) / sampling_rate
    
    # Generate random data for each channel
    data = np.random.rand(num_samples, num_channels)
    
    # Combine time array and data into a DataFrame
    df = pd.DataFrame(np.column_stack([time_array] + [data[:, i] for i in range(num_channels)]), columns=['Time'] + [f'Channel_{i+1}' for i in range(num_channels)])
    
    return df

if __name__ == "__main__":
    num_samples = 10000  # Number of samples
    num_channels = 3     # Number of channels
    
    random_data = generate_random_data(num_samples, num_channels)
    random_data.to_csv('random_data.csv', index=False)
    print("Random data generated and saved to 'random_data.csv'.")
