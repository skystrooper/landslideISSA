import matplotlib.pyplot as plt
import pandas as pd
from threshold_new import threshold_range

# Set the threshold values
lower_threshold, upper_threshold = threshold_range

# Coordinates for each place
places = ['27.25,88.25', '27.25,88.5', '27.25,88.75', '27.5,88.25', '27.5,88.5', '27.5,88.75', '27.75,88.25', '27.75,88.5', '27.75,88.75', '28,88.5', '28,88.75']

# Create a plot for all places
plt.figure(figsize=(12, 8))

# Iterate over all years from 2009 to 2021
for year in range(2009, 2022):
    # Read data from CSV file for the current year
    df = pd.read_csv(f'../Rainpredict/Years/{year}.csv' )

    for index, row in df.iterrows():
        place_label = places[index]
        plt.plot(row.index, row.values, marker='o', linestyle='', label=f'{place_label} - {year}')

# Add horizontal lines at both lower and upper thresholds
plt.axhline(y=lower_threshold, color='r', linestyle='--', label=f'{lower_threshold}mm Lower Threshold')
plt.axhline(y=upper_threshold, color='b', linestyle='--', label=f'{upper_threshold}mm Upper Threshold')

plt.title('Rainfall for 11 Places (2009-2021)')
plt.xlabel('Day')
plt.ylabel('Rainfall')
plt.grid(False)
plt.tight_layout()

# Create a zoomed-in version
plt.figure(figsize=(8, 6))
for year in range(2009, 2022):
    df = pd.read_csv(f'../Rainpredict/Years/{year}.csv' )
    for index, row in df.iterrows():
        place_label = places[index]
        plt.plot(row.index, row.values, marker='o', linestyle='', label=f'{place_label} - {year}')

plt.axhline(y=lower_threshold, color='r', linestyle='--', label=f'{lower_threshold}mm Lower Threshold')
plt.axhline(y=upper_threshold, color='b', linestyle='--', label=f'{upper_threshold}mm Upper Threshold')

plt.title('Zoomed-In: Rainfall for 11 Places (2009-2021)')
plt.xlabel('Day')
plt.ylabel('Rainfall')
plt.grid(False)
plt.tight_layout()

# Set specific x and y-axis limits for the zoomed-in version
plt.xlim(150, 250)  # Adjust the x-axis limits as needed
plt.ylim(lower_threshold - 10, upper_threshold + 10)  # Add some padding to the y-axis limits

plt.show()

print("result has been printed")
