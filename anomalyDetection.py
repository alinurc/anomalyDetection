import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sps

# safe_divide method
# definition: Prevents division to zero if any datum is zero
# args:       dividend, divisor
# returns:    division result
def safe_divide(x, y):
  if y == 0:
    y = 0.0000001
  return x / y

# get_mean method
# definition: Finds the mean value of all data
# args:       data array
# returns:    mean value
def get_mean(x):
  return sum(x) / len(x)

# window_mean method
# definition: Finds the mean value of a current window of data
# args:       data array, current index, window size
# returns:    mean value
def window_mean(x, idx, window):
  left_sum = 0
  left_num = 0
  # Left of index
  for j in range(max(idx - window, 0), idx):
    left_sum += x[j]
    left_num += 1

  right_sum = 0
  right_num = 0
  # Right of index
  for j in range(idx + 1, min(idx + window, len(x))):
    right_sum += x[j]
    right_num += 1
  return (left_sum + right_sum) / (left_num + right_num)

# deviated method
# definition: Finds whether a value is deviated from mean value
#             and this deviation exceeds a certain threshold
# args:       value, mean, deviation threshold
# returns:    True if threshold is exceeded, else false
def deviated(value, mean, threshold):
  return abs(safe_divide(max(value, mean), min(value, mean))) > threshold

# trend_direction method
# definition: Finds the direction of deviation trend
# args:       data array, current index, window size,
#             global mean value, deviation threshold
# returns:    1 if trend is upwards, -1 if trend is downwards
def trend_direction(x, idx, window, global_mean, threshold):
  num_increase = 0
  num_decrease = 0
  for j in range(idx + 1, min(idx + window, len(x))):
    if deviated(x[j], global_mean, threshold):
      if x[j] > global_mean:
        num_increase += 1
      else:
        num_decrease += 1
  if num_increase >= window - 1:
    return 1
  elif num_decrease >= window - 1:
    return -1
  return 0

# filter method
# definition: Filters the noisy data and toggles the LED
# args:       data array, window size, deviation threshold
# returns:    filtered data array
def filter(x, window, threshold):
  x = x.copy()
  # Remove the noise
  for i in range(len(x)):
    mean = window_mean(x, i, window)
    if deviated(x[i], mean, threshold):
      x[i] = mean
  
  # Find the trend and toggle the LED
  global_mean = get_mean(x)
  trend_window = 2
  led_indicator = False

  for i in range(len(x)):
    direction = trend_direction(x, i, trend_window, global_mean, threshold)
    if direction > 0 and led_indicator is False:
      led_indicator = True
      print("TURN ON LED", i)
    elif direction < 0 and led_indicator is True:
      led_indicator = False
      print("TURN OFF LED", i)
  return x

# Creating the data. I know, it's pretty lousy
np.random.seed(17863)
rand_x = np.random.randint(8, 10, 1500)
rand_x[250] = 7       # Ramp down start
rand_x[251] = 6
rand_x[252] = 7
rand_x[253] = 5
rand_x[254] = 4
rand_x[255] = 3
rand_x[256] = 2
rand_x[257] = 4
rand_x[258] = 2
rand_x[259] = 1
rand_x[260] = 3
rand_x[261] = 1
rand_x[262] = 0       # Ramp down end
rand_x[350] = 17      # Ramp up start
rand_x[351] = 16
rand_x[352] = 17
rand_x[353] = 15
rand_x[354] = 14
rand_x[355] = 13
rand_x[356] = 12
rand_x[357] = 14
rand_x[358] = 12
rand_x[359] = 11
rand_x[360] = 13
rand_x[361] = 11
rand_x[362] = 10      # Ramp up end
rand_x[400] = 0       # Noise
rand_x[450] = 0       # Noise
rand_x[150] = 15      # Noise
rand_x[1250] = 7       # Ramp down start
rand_x[1251] = 6
rand_x[1252] = 7
rand_x[1253] = 5
rand_x[1254] = 4
rand_x[1255] = 3
rand_x[1256] = 2
rand_x[1257] = 4
rand_x[1258] = 2
rand_x[1259] = 1
rand_x[1260] = 3
rand_x[1261] = 1
rand_x[1262] = 0       # Ramp down end
rand_x[1350] = 17      # Ramp up start
rand_x[1351] = 16
rand_x[1352] = 17
rand_x[1353] = 15
rand_x[1354] = 14
rand_x[1355] = 13
rand_x[1356] = 12
rand_x[1357] = 14
rand_x[1358] = 12
rand_x[1359] = 11
rand_x[1360] = 13
rand_x[1361] = 11
rand_x[1362] = 10      # Ramp up end
rand_x[1400] = 0       # Noise
rand_x[1450] = 0       # Noise
rand_x[1150] = 15      # Noise

# These are filters in SciPY and Pandas libraries
mov_avg = pd.DataFrame(rand_x).rolling(window = 11).mean()        # Moving Average Filter
x_sav_gol = sps.savgol_filter(rand_x, 11, 2)                       # Savitsky-Golay Filter
own_filter = filter(rand_x, 4, 1.3)

# Creating the graph
plt.xlabel('Day')
plt.ylabel('Servings of Beer')
plt.plot(rand_x, color = 'red', label = 'Data', linewidth = 0.5)
plt.plot(mov_avg, color = 'green', label = 'Moving Average', linewidth = 1.5)
plt.plot(x_sav_gol, color = 'purple', label = 'Savitsky-Golay', linewidth = 1.5)
plt.plot(own_filter, color = 'blue', label = 'My Filter', linewidth = 0.5)
plt.legend(loc = 'lower left')
plt.show()