import pandas as pd
import matplotlib.pyplot as plt

# Load performance data
df = pd.read_csv('heuristic_performance.csv')

# Define 6 distinct colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', 
          '#d62728', '#9467bd', '#8c564b']

# Metrics: (column, ylabel, prefix)
metrics = [
    ('Avg_Move_Time_s', 'Average Move Time (s)', 'move_time'),
    ('Win_Rate_%',      'Win Rate (%)',            'win_rate')
]

idx = 0
for column, ylabel, prefix in metrics:
    for depth in [2, 3, 4]:
        subset = df[df['Depth'] == depth]
        plt.figure()
        plt.bar(subset['Heuristic'], subset[column], color=colors[idx])
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(ylabel)
        plt.title(f'{ylabel} at Depth {depth}')
        plt.tight_layout()
        filename = f'depth{depth}_{prefix}.png'
        plt.savefig(filename)
        plt.close()
        print(f'Saved {filename}')
        idx += 1
