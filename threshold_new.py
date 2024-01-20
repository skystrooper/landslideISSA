import pandas as pd
import numpy as np

def calculate_threshold_and_validation(csv_filename='Landslides.csv', num_validation_values=3):
    # Read landslides data from CSV file
    df_landslides = pd.read_csv(csv_filename)

    # Drop rows with NaN values in date-related columns
    df_landslides = df_landslides.dropna(subset=['Day', 'Month', 'Year'])

    # Coordinates for the grid
    lats = [27.25, 27.5, 27.75, 28]
    lons = [88.25, 88.5, 88.75]

    # Create a meshgrid of latitudes and longitudes
    lons, lats = np.meshgrid(lons, lats)

    # Flatten the latitudes and longitudes
    flat_lats = lats.flatten()
    flat_lons = lons.flatten()

    # Exclude the specific coordinate (28, 88.25)
    mask = ~((flat_lats == 28) & (flat_lons == 88.25))
    flat_lats = flat_lats[mask]
    flat_lons = flat_lons[mask]

    # Ensure consistent lengths of all arrays
    num_points = len(flat_lats)
    rainfall = np.zeros(num_points)  # Create an array for rainfall data

    # Dictionary to store highest rainfall for each day
    highest_rainfall_dict = {}

    # Accumulate highest rainfall values for landslide days
    for i, (_, row) in enumerate(df_landslides.iterrows()):
        # Extract day, month, and year from the row
        day, month, year = row['Day'], row['Month'], row['Year']

        # Construct the date
        user_date = pd.to_datetime(f'{year}-{month}-{day}', format='%Y-%m-%d')

        # Determine the corresponding year based on the date
        year = user_date.year

        # Construct the filename for the CSV file based on the year
        csv_filename_year = f'Years/{year}.csv'

        try:
            # Read rainfall data from the corresponding CSV file
            df_rainfall = pd.read_csv(csv_filename_year)

            date_column = f'Day_{user_date.dayofyear}'  # Assuming the day is in the format 'YYYY-MM-DD'

            # Extract rainfall data for the specified date
            if date_column in df_rainfall.columns:
                rainfall = df_rainfall[date_column].values.flatten()

                # Save the highest rainfall value for this date
                highest_rainfall_dict[user_date] = rainfall.max()

        except FileNotFoundError:
            print(f"Error: CSV file '{csv_filename_year}' not found for year {year}.")

    # Include every year's highest rainfall day
    for year in range(df_landslides['Year'].min(), df_landslides['Year'].max() + 1):
        csv_filename_year = f'Years/{year}.csv'

        try:
            df_rainfall = pd.read_csv(csv_filename_year)
            highest_rainfall_day = df_rainfall.iloc[:, 1:].max(axis=1).idxmax()  # Assuming the columns start from index 1
            highest_rainfall_value = df_rainfall.iloc[highest_rainfall_day, 1:].max()
            highest_rainfall_dict[highest_rainfall_day] = highest_rainfall_value
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_filename_year}' not found for year {year}.")

    if highest_rainfall_dict:
        valid_values = [value for value in highest_rainfall_dict.values() if not np.isnan(value)]

        # Use a portion of values for validation
        validation_values = valid_values[:num_validation_values]
        valid_values = valid_values[num_validation_values:]

        # Calculate the threshold range based on percentiles
        lower_percentile = 60
        upper_percentile = 90
        lower_threshold = np.percentile(valid_values, lower_percentile)
        upper_threshold = np.percentile(valid_values, upper_percentile)

        print(f'Threshold range for landslides: {lower_threshold:.2f}-{upper_threshold:.2f} mm')
        print(f'Validation values: {validation_values}')

        # Check validation (True/False)
        validation_true_false = [lower_threshold <= value <= upper_threshold for value in validation_values]
        print(f'Validation values (True/False): {validation_true_false}')

        return lower_threshold, upper_threshold

    else:
        print('No valid rainfall values for landslides.')
        return None

# Example usage:

threshold_range = calculate_threshold_and_validation()
print("Threshold Range:", threshold_range)
