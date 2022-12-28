from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import sys
import statistics
import appleHealth

# Number of seconds to subtract from start of walk (for putting phone away)
PHONE_DURATION_START = 20

# Number of seconds to subtract from end of walk (for putting phone away)
PHONE_DURATION_END = 10

# Duration of intervals that sensor data will be averaged into
GROUP_FREQUENCY = "500ms"

# Input file
record_1 = sys.argv[1]
record_2 = sys.argv[2]
if len(sys.argv) > 3:
    apple_record = sys.argv[3]

# Read csvs
data_left = pd.read_csv(record_1, parse_dates=["time"])
data_right = pd.read_csv(record_2, parse_dates=["time"])

# Sync beginning and ending timestamps
first_time = max(data_left['time'].iloc[0], data_right['time'].iloc[0])
last_time = min(data_left['time'].iat[-1], data_right['time'].iat[-1])
original_walk_duration = last_time - first_time

# Remove time from beginning and end to account for putting phone away
first_time = first_time + timedelta(seconds=PHONE_DURATION_START)
last_time = last_time - timedelta(seconds=PHONE_DURATION_END)
trimmed_walk_duration = last_time - first_time

# Make both datasets begin and end at same time
data_left = data_left.loc[data_left['time'] >= first_time]
data_left = data_left.loc[data_left['time'] <= last_time].reset_index(drop=True)

data_right = data_right.loc[data_right['time'] >= first_time]
data_right = data_right.loc[data_right['time'] <= last_time].reset_index(drop=True)

# Method 1: Find left/right variance and min/max variance and asymmetric variance % before combined
data_left_variance = statistics.variance(data_left['atotal'])
data_right_variance = statistics.variance(data_right['atotal'])
variance_min = data_right_variance if data_left_variance >= data_right_variance else data_left_variance
variance_max = data_left_variance if data_left_variance >= data_right_variance else data_right_variance
asymmetric_variance = (1 - (variance_min / variance_max)) * 100

# Define bins, group data by timestamps
group_left = data_left.groupby(pd.Grouper(key="time", freq=GROUP_FREQUENCY)).mean()
group_right = data_right.groupby(pd.Grouper(key="time", freq=GROUP_FREQUENCY)).mean()

# Combine the left and right datasets into one dataframe
group_combined = group_left
group_combined.drop(['ax', 'ay', 'az'], axis=1, inplace=True)
group_combined['right_atotal'] = group_right['atotal']
group_combined['sum_atotal'] = group_left['atotal'] + group_left['right_atotal']
group_combined.rename(columns={"atotal": "left_atotal"}, inplace=True)
group_combined['L'] = group_combined["left_atotal"] / group_combined["sum_atotal"]
group_combined['R'] = group_combined["right_atotal"] / group_combined["sum_atotal"]
group_combined["L - R"] = group_combined['L'] - group_combined['R']

# Drop NaN rows and count how many were dropped
size_before_drop = group_combined.size
group_combined.dropna(inplace=True)
size_after_drop = group_combined.size

# Convert date timestamps to elapsed walk duration
group_combined.index = (group_combined.index - group_combined.first_valid_index()).total_seconds()

# Method 2: Find left/right variance and min/max variance and asymmetric variance % after combined
data_left_variance = statistics.variance(group_combined['left_atotal'])
data_right_variance = statistics.variance(group_combined['right_atotal'])
variance_min = data_right_variance if data_left_variance >= data_right_variance else data_left_variance
variance_max = data_left_variance if data_left_variance >= data_right_variance else data_right_variance
asymmetric_variance_combined = (1 - (variance_min / variance_max)) * 100

# Method 3: Find average
avg_difference = group_combined["L - R"].mean() * 100

# Walking asymmetric % report from Apple Health
apple_health_analysis = None
if len(sys.argv) > 3:
    apple_health_analysis = appleHealth.analysis_data(apple_record)

# Prints
# print(group_combined)
print("\n ======= Summary =======")
print("Original walk duration: ", original_walk_duration)
print("Trimmed walk duration: ", trimmed_walk_duration)
print("# of dropped rows (NaN): ", size_before_drop - size_after_drop)
print("Left variance: ", data_left_variance)
print("Right variance: ", data_right_variance)
print("1. Asymmetric variance percentage before combined interval: {:.2f}%".format(asymmetric_variance))
print("2. Asymmetric variance percentage after combined interval: {:.2f}%".format(asymmetric_variance_combined))
print("3. Result: Average difference in percentage: {:.2f}%".format(avg_difference))
if (apple_health_analysis != None):
    print("4. Asymmetric percentage from Apple Health analysis: {:.2f}%".format(apple_health_analysis))
else:
    print("4. Asymmetric percentage from Apple Health analysis: N/A")

# Plots
# plt.plot(group_combined.index, group_combined['L - R'])
plt.plot(group_combined.index, group_combined['left_atotal'], label="left leg")
plt.plot(group_combined.index, group_combined['right_atotal'], label="right leg")
plt.title("Leg Accelerations vs. Time")
plt.xlabel("Elapsed Time of Walk (seconds)")
plt.ylabel("Acceleration total (m/s²)")
plt.legend(loc="upper right")
plt.show()