import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
import geopandas as gpd
import numpy as np
from threshold_new import threshold_range

# Set the threshold value
lower_threshold, upper_threshold = threshold_range
threshold = lower_threshold

# Create a DataFrame to store details of dates exceeding the threshold
result_df = pd.DataFrame(columns=['Year', 'Date', 'Latitude', 'Longitude', 'Rainfall'])

# Iterate over all years from 2009 to 2026
for year in range(2009, 2026):
    # Read rainfall data from CSV file for the current year
    df = pd.read_csv(f'../Rainpredict/Years/{year}.csv' )

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

    # Iterate over all dates
    for user_date in range(1, 366):  # Assuming days range from 1 to 365
        date_column = f'Day_{user_date}'

        # Extract rainfall data for the specified date
        if date_column in df.columns:
            rainfall = df[date_column].values.flatten()

            # Check if any rainfall values exceed the threshold
            exceed_threshold_indices = np.where(rainfall > threshold)[0]

            if len(exceed_threshold_indices) > 0:
                # Plotting the map for the specified date
                plt.figure(figsize=(10, 8))
                ax = plt.axes(projection=ccrs.PlateCarree())

                # Adding Sikkim outline from shapefile
                sikkim = gpd.read_file('shpfile/Sikkim.shp')
                ax.add_geometries(sikkim['geometry'], crs=ccrs.PlateCarree(), edgecolor='black', facecolor='none')

                # Adding states/provinces as a feature
                states_provinces = NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines',
                                                       scale='10m', facecolor='none')
                ax.add_feature(states_provinces, edgecolor='black')

                # Set the extent of the map
                ax.set_extent([88.0, 88.9, 27.0, 28.2], crs=ccrs.PlateCarree())  # Adjust these values to fit the desired area

                # Scatter plot with rainfall data for the specified date
                sc = ax.scatter(flat_lons, flat_lats, c=rainfall, cmap='rainbow', transform=ccrs.PlateCarree(), s=100,
                                edgecolors='k')

                # Customizing the map
                ax.coastlines(resolution='10m')
                ax.gridlines(draw_labels=True)

                # Display rainfall value above each coordinate
                for index in range(num_points):
                    plt.text(flat_lons[index], flat_lats[index], f'{rainfall[index]:.2f}mm', ha='center', va='bottom', fontsize=8,
                             bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.3'))

                # Adjust colorbar
                cbar = plt.colorbar(sc, label=f'Rainfall on Day {user_date} (mm)')
                cbar.set_ticks([rainfall.min(), rainfall.max()])  # Set ticks to min and max values of rainfall data

                # Add the date information to the header
                plt.title(f'Rainfall in Sikkim on Day {user_date} ({year})\nDate: {pd.to_datetime(f"{year}-{user_date}", format="%Y-%j").strftime("%d%m%y")}')

                plt.tight_layout()
                plt.show()

                # Save details to the DataFrame
                for index in exceed_threshold_indices:
                    result_df = result_df.append({
                        'Year': year,
                        'Date': pd.to_datetime(f'{year}-{user_date}', format='%Y-%j').strftime('%d/%m/%y'),
                        'Latitude': flat_lats[index],
                        'Longitude': flat_lons[index],
                        'Rainfall': rainfall[index]
                    }, ignore_index=True)

# Save the DataFrame to an Excel file
result_df.to_excel('Dates_Exceeding_Threshold_All_Years.xlsx', index=False)
