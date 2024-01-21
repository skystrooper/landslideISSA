import pandas as pd
from datetime import datetime, timedelta

def calculate_date(year, day_of_year):
    # Combine year and day_of_year to create a date string
    date_str = f'{year}-{day_of_year}'

    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%j').date()

    return date_obj

def get_coordinate_by_row(row_index):
    coordinates = [
        '27.25,88.25', '27.25,88.5', '27.25,88.75',
        '27.5,88.25', '27.5,88.5', '27.5,88.75',
        '27.75,88.25', '27.75,88.5', '27.75,88.75',
        '28,88.5', '28,88.75'
    ]
    return coordinates[row_index]

def process_rainfall_data_for_years(years, output_filename='high_rainfall_data.csv'):
    # Initialize an empty DataFrame to store high rainfall data
    high_rainfall_data = pd.DataFrame(columns=['Date', 'Rainfall', 'Coordinate'])

    for year in years:
        try:
            # Construct the input filename for the current year
            input_filename = f'Years/{year}.csv'

            # Read the input CSV file
            df = pd.read_csv(input_filename)

            # Extract the year from the input filename
            year = int(input_filename.split('/')[1].split('.')[0])

            # Iterate through each column (Day_x) and each row
            for index, row in df.iterrows():
                for column in df.columns[1:]:
                    if '_' in column:
                        # Extract day number, rainfall value, and coordinate
                        day_of_year = int(column.split('_')[1])
                        rainfall = row[column]
                        coordinate = get_coordinate_by_row(index)

                        # Check if rainfall is greater than 100mm
                        if rainfall > 100:
                            # Calculate the date
                            date = calculate_date(year, day_of_year)

                            # Append the data to the high rainfall DataFrame
                            high_rainfall_data = pd.concat(
                                [high_rainfall_data, pd.DataFrame({'Date': [date], 'Rainfall': [rainfall], 'Coordinate': [coordinate]})],
                                ignore_index=True)

            print(f"Processing for {year} complete.")

        except FileNotFoundError:
            print(f"Error: CSV file '{input_filename}' not found.")

    # Save the high rainfall data to a new CSV file
    high_rainfall_data.to_csv(output_filename, index=False)

    print(f"All years processed. High rainfall data saved to {output_filename}")

# Example usage:
years_list = list(range(2009, 2022))
process_rainfall_data_for_years(years_list)
