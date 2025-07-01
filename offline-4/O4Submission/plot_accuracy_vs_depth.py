import matplotlib.pyplot as plt
import numpy as np

# Data extracted from the test results
# Adult Dataset Results
adult_data = {
    'IG': {
        'depths': [2, 3, 4],
        'accuracies': [81.98, 82.37, 82.05]
    },
    'IGR': {
        'depths': [2, 3, 4],
        'accuracies': [83.36, 83.35, 86.02]
    },
    'NWIG': {
        'depths': [2, 3, 4],
        'accuracies': [81.97, 82.27, 81.76]
    }
}

# Iris Dataset Results
iris_data = {
    'IG': {
        'depths': [2, 3, 4],
        'accuracies': [92.00, 91.67, 92.67]
    },
    'IGR': {
        'depths': [2, 3, 4],
        'accuracies': [93.67, 95.00, 94.67]
    },
    'NWIG': {
        'depths': [2, 3, 4],
        'accuracies': [92.00, 91.67, 92.67]
    }
}

def plot_accuracy_vs_depth_bars():
    """Create bar plots for each depth showing accuracy of each criteria"""
    # Create subplots: 3 depths for each dataset
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Colors for each criteria
    colors = {'IG': '#1f77b4', 'IGR': '#ff7f0e', 'NWIG': '#2ca02c'}
    criterias = ['IG', 'IGR', 'NWIG']
    depths = [2, 3, 4]
    
    # Plot Adult Dataset (top row)
    for i, depth in enumerate(depths):
        ax = axes[0, i]
        
        # Get accuracies for this depth
        accuracies = [adult_data[criteria]['accuracies'][depth-2] for criteria in criterias]
        
        # Create bar chart
        bars = ax.bar(criterias, accuracies, 
                     color=[colors[c] for c in criterias],
                     alpha=0.8, 
                     edgecolor='black',
                     linewidth=1)
        
        # Add value labels on bars
        for j, (bar, acc) in enumerate(zip(bars, accuracies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{acc:.2f}%',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        
        ax.set_title(f'Adult Dataset - Depth {depth}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_ylim(79, 87)
        ax.grid(True, alpha=0.3, axis='y')
        
    # Plot Iris Dataset (bottom row)
    for i, depth in enumerate(depths):
        ax = axes[1, i]
        
        # Get accuracies for this depth
        accuracies = [iris_data[criteria]['accuracies'][depth-2] for criteria in criterias]
        
        # Create bar chart
        bars = ax.bar(criterias, accuracies, 
                     color=[colors[c] for c in criterias],
                     alpha=0.8, 
                     edgecolor='black',
                     linewidth=1)
        
        # Add value labels on bars
        for j, (bar, acc) in enumerate(zip(bars, accuracies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{acc:.2f}%',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax.set_title(f'Iris Dataset - Depth {depth}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_ylim(89, 97)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Add overall title
    fig.suptitle('Accuracy Comparison by Criteria and Depth', fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('accuracy_bar_plots_by_depth.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_combined_bar_comparison():
    """Create a combined bar plot comparing both datasets for each depth"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Colors and patterns
    colors = {'IG': '#1f77b4', 'IGR': '#ff7f0e', 'NWIG': '#2ca02c'}
    criterias = ['IG', 'IGR', 'NWIG']
    depths = [2, 3, 4]
    
    # Bar width and positions
    bar_width = 0.35
    x_pos = np.arange(len(criterias))
    
    for i, depth in enumerate(depths):
        ax = axes[i]
        
        # Get accuracies for this depth
        adult_accuracies = [adult_data[criteria]['accuracies'][depth-2] for criteria in criterias]
        iris_accuracies = [iris_data[criteria]['accuracies'][depth-2] for criteria in criterias]
        
        # Create grouped bar chart
        bars1 = ax.bar(x_pos - bar_width/2, adult_accuracies, bar_width,
                      label='Adult Dataset', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x_pos + bar_width/2, iris_accuracies, bar_width,
                      label='Iris Dataset', alpha=0.8, edgecolor='black')
        
        # Color bars according to criteria
        for j, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            bar1.set_color(colors[criterias[j]])
            bar2.set_color(colors[criterias[j]])
            bar2.set_alpha(0.6)  # Make iris bars slightly transparent
        
        # Add value labels on bars
        for j, (bar, acc) in enumerate(zip(bars1, adult_accuracies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{acc:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        for j, (bar, acc) in enumerate(zip(bars2, iris_accuracies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                   f'{acc:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_title(f'Depth {depth} Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(criterias)
        ax.set_ylim(75, 100)
        ax.grid(True, alpha=0.3, axis='y')
        
        if i == 0:  # Only show legend on first subplot
            ax.legend()
    
    # Add overall title
    fig.suptitle('Dataset Comparison by Criteria and Depth', fontsize=16, fontweight='bold')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('combined_bar_comparison_by_depth.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_table():
    """Create a summary table showing best performance for each dataset"""
    print("=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    
    print("\nAdult Dataset:")
    print("-" * 40)
    for criteria in ['IG', 'IGR', 'NWIG']:
        max_acc = max(adult_data[criteria]['accuracies'])
        best_depth = adult_data[criteria]['depths'][adult_data[criteria]['accuracies'].index(max_acc)]
        print(f"{criteria:5} - Best: {max_acc:.2f}% at depth {best_depth}")
    
    print("\nIris Dataset:")
    print("-" * 40)
    for criteria in ['IG', 'IGR', 'NWIG']:
        max_acc = max(iris_data[criteria]['accuracies'])
        best_depth = iris_data[criteria]['depths'][iris_data[criteria]['accuracies'].index(max_acc)]
        print(f"{criteria:5} - Best: {max_acc:.2f}% at depth {best_depth}")
    
    # Overall best
    adult_best = max([max(adult_data[c]['accuracies']) for c in adult_data])
    iris_best = max([max(iris_data[c]['accuracies']) for c in iris_data])
    
    print(f"\nOverall Best Performance:")
    print(f"Adult Dataset: {adult_best:.2f}% (IGR at depth 4)")
    print(f"Iris Dataset: {iris_best:.2f}% (IGR at depth 3)")

if __name__ == "__main__":
    print("Generating accuracy vs depth bar plots...")
    
    # Create bar plots for each depth
    plot_accuracy_vs_depth_bars()
    
    # Create combined bar comparison
    plot_combined_bar_comparison()
    
    # Print summary
    create_summary_table()
    
    print("\nPlots saved as:")
    print("- accuracy_bar_plots_by_depth.png (separate bar plots for each depth)")
    print("- combined_bar_comparison_by_depth.png (side-by-side comparison)")
