import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Read the data ---
# Update the filename/path as needed
df = pd.read_csv('results.csv')

# Take only the first 10 rows
df_top10 = df.head(10)

# Extract the columns we need
instances     = df_top10['Name']
randomized    = df_top10['Randomized-1']
greedy        = df_top10['Greedy-1']
semi_greedy   = df_top10['Semi-Greedy-1']
local_search  = df_top10['LS Avg Value']
grasp         = df_top10['GRASP Result']

# --- Prepare the bar positions ---
x = np.arange(len(instances))
width = 0.15  # width of each bar

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(x - 2*width, randomized,   width, label='Randomized')
ax.bar(x -     width, greedy,     width, label='Greedy')
ax.bar(x +     0*width, semi_greedy, width, label='Semi-Greedy')
ax.bar(x +     width, local_search, width, label='Local Search')
ax.bar(x + 2*width,          grasp,     width, label='GRASP')

# --- Add horizontal grid lines at every 2000 ---
y_max = max(df_top10[['Randomized-1','Greedy-1','Semi-Greedy-1',
                     'LS Avg Value','GRASP Result']].max()) * 1.05
for y in np.arange(0, y_max + 1, 2000):
    ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)

# --- Labels, title, and legend ---
ax.set_xticks(x)
ax.set_xticklabels(instances)
ax.set_xlabel('Instance')
ax.set_ylabel('Cut Weight')
ax.set_title('Max Cut (Graph first 10)')
ax.legend()

plt.tight_layout()
plt.show()
