import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Read the data ---
df = pd.read_csv('results.csv')

# Parameters
batch_size = 10
num_batches = 5  # plots for rows 1-10, 11-20, ..., 41-50

for batch_idx in range(num_batches):
    start = batch_idx * batch_size
    end = start + batch_size
    df_batch = df.iloc[start:end]

    instances    = df_batch['Name']
    randomized   = df_batch['Randomized-1']
    greedy       = df_batch['Greedy-1']
    semi_greedy  = df_batch['Semi-Greedy-1']
    local_search = df_batch['LS Avg Value']
    grasp        = df_batch['GRASP Result']

    x = np.arange(len(instances))
    width = 0.15

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - 2*width, randomized,   width, label='Randomized')
    ax.bar(x -     width, greedy,      width, label='Greedy')
    ax.bar(x +     0*width, semi_greedy, width, label='Semi-Greedy')
    ax.bar(x +     width, local_search, width, label='Local Search')
    ax.bar(x + 2*width,          grasp,     width, label='GRASP')

    # horizontal grid lines every 2000
    y_max = max(df_batch[['Randomized-1','Greedy-1','Semi-Greedy-1',
                         'LS Avg Value','GRASP Result']].max()) * 1.05
    for y in np.arange(0, y_max + 1, 2000):
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(instances)
    ax.set_xlabel('Instance')
    ax.set_ylabel('Cut Weight')
    batch_label_start = start + 1
    batch_label_end = min(end, len(df))
    ax.set_title(f'Max Cut Results')
    ax.legend()
    plt.tight_layout()
    # Save each batch figure with a descriptive filename
    filename = f"maxcut_{batch_label_start}.png"
    fig.savefig(filename, dpi=300)
    plt.close(fig)  # Close the figure to free memory
