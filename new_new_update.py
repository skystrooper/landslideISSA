import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

ls = pd.read_csv('Landslides.csv')

size = len(ls)

for x in range(size):
    lan_day = ls['Day'][x]
    lan_mon = ls['Month'][x]
    lan_year = ls['Year'][x]

    lan_day_no = dt.datetime(lan_year, lan_mon, lan_day).timetuple().tm_yday

    df = pd.read_csv(f'Years/{lan_year}.csv')

    # ... (existing code remains unchanged)
    rainfall = df[f'Day_{lan_day_no}'].to_numpy().tolist()
    rain_prev_1 = df[f'Day_{lan_day_no - 1}'].to_numpy().tolist()
    rain_prev_2 = df[f'Day_{lan_day_no - 2}'].to_numpy().tolist()
    rain_prev_3 = df[f'Day_{lan_day_no - 3}'].to_numpy().tolist()
    rain_prev_4 = df[f'Day_{lan_day_no - 4}'].to_numpy().tolist()
    rain_prev_5 = df[f'Day_{lan_day_no - 5}'].to_numpy().tolist()
    rain_prev_6 = df[f'Day_{lan_day_no - 6}'].to_numpy().tolist()
    rain_prev_7 = df[f'Day_{lan_day_no - 7}'].to_numpy().tolist()

    rainfall_3_days = [0] * 11
    rainfall_7_days = [0] * 11

    for x in range(11):
        rainfall_3_days[x] = rainfall[x] + rain_prev_1[x] + rain_prev_2[x] + rain_prev_3[x]
        rainfall_7_days[x] = rainfall[x] + rain_prev_1[x] + rain_prev_2[x] + rain_prev_3[x] + rain_prev_4[x] + \
                             rain_prev_5[x] + rain_prev_6[x] + rain_prev_7[x]

    pd.set_option('display.max_columns', None)
    res = pd.DataFrame({'Day': lan_day, 'Month': lan_mon, 'Year': lan_year, 'Prec_on_day': rainfall, 'Prec_day_before': rain_prev_1, '3_days_combined': rainfall_3_days, '7_days_combined': rainfall_7_days})

    # Change the row names/index to custom values
    custom_row_names = ['27.25,88.25', '27.25,88.5', '27.25,88.75', '27.5,88.25', '27.5,88.5', '27.5,88.75', '27.75,88.25', '27.75,88.5', '27.75,88.75', '28,88.5', '28,88.75']  # Replace with your desired row names
    res.index = custom_row_names

    graph = pd.DataFrame({'rain_day': rainfall, 'rain_before': rain_prev_1, '3_days_combined': rainfall_3_days, '7_days_combined': rainfall_7_days})

    plt.figure(figsize=(12, 8))

    for col in ['Prec_on_day', 'Prec_day_before', '3_days_combined', '7_days_combined']:
        plt.plot(res.loc[:, col], label=col.replace('_', ' ').title(), marker='o')

    plt.xlabel('Lat, Long')
    plt.ylabel('Rainfall')
    plt.title(f'{lan_day}/{lan_mon}/{lan_year}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    res.to_csv(f'result.csv', index=True)
