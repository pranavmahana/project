# import pandas as pd
# import numpy.random as np

# # Number of rows and columns in the CSV file
# num_rows = 1000
# num_columns = 2

# # Generate random data
# data = np.randint(0, 300, size=(num_rows, num_columns))

# # Create a DataFrame
# df = pd.DataFrame(data, columns=[f'Column{i}' for i in range(1, num_columns + 1)])

# # Specify the CSV file path
# csv_file_path = './random_data.csv'

# # Write the DataFrame to a CSV file
# df.to_csv(csv_file_path, index=False)

# print(f"Random CSV file generated at: {csv_file_path}")












import numpy as np

# Number of rows and columns in the CSV file
num_rows = 100000
num_columns = 4

# Generate random floating-point data between 0 and 1
data = np.random.uniform(0, 1, size=(num_rows, num_columns))

# Round the data to 8 decimal places
data = np.round(data, 8)

# Specify the CSV file path
csv_file_path = 'random_data.csv'

# Write data to the CSV file
np.savetxt(csv_file_path, data, delimiter=',', fmt='%.8f')

print(f"Random CSV file generated at: {csv_file_path}")

