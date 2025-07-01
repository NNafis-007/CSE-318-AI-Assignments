import matplotlib.pyplot as plt
import numpy as np

# Data extracted from the test results - Average Total Nodes
# Adult Dataset Results
adult_nodes_data = {
    'IG': {
        'depths': [2, 3, 4],
        'avg_nodes': [92, 1103, 4899]
    },
    'IGR': {
        'depths': [2, 3, 4],
        'avg_nodes': [240, 290, 525]
    },
    'NWIG': {
        'depths': [2, 3, 4],
        'avg_nodes': [127, 1307, 5278]
    }
}

# Iris Dataset Results
iris_nodes_data = {
    'IG': {
        'depths': [2, 3, 4],
        'avg_nodes': [20, 31, 35]
    },
    'IGR': {
        'depths': [2, 3, 4],
        'avg_nodes': [22, 25, 27]
    },
    'NWIG': {
        'depths': [2, 3, 4],
        'avg_nodes': [20, 30, 34]
    }
}

def plot_nodes_vs_depth_bars():
    """Create bar plots for each depth showing average total nodes of each criteria"""
    # Create subplots: 3 depths for each dataset
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Colors for each criteria
    colors = {'IG': '#1f77b4', 'IGR': '#ff7f0e', 'NWIG': '#2ca02c'}
    criterias = ['IG', 'IGR', 'NWIG']
    depths = [2, 3, 4]
    
    # Plot Adult Dataset (top row)
    for i, depth in enumerate(depths):
        ax = axes[0, i]
        
        # Get average nodes for this depth
        avg_nodes = [adult_nodes_data[criteria]['avg_nodes'][depth-2] for criteria in criterias]
        
        # Create bar chart
        bars = ax.bar(criterias, avg_nodes, 
                     color=[colors[c] for c in criterias],
                     alpha=0.8, 
                     edgecolor='black',
                     linewidth=1)
        
        # Add value labels on bars
        for j, (bar, nodes) in enumerate(zip(bars, avg_nodes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                   f'{nodes}',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.set_title(f'Adult Dataset - Depth {depth}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Total Nodes', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Use log scale for adult dataset due to large differences
        ax.set_yscale('log')
        
    # Plot Iris Dataset (bottom row)
    for i, depth in enumerate(depths):
        ax = axes[1, i]
        
        # Get average nodes for this depth
        avg_nodes = [iris_nodes_data[criteria]['avg_nodes'][depth-2] for criteria in criterias]
        
        # Create bar chart
        bars = ax.bar(criterias, avg_nodes, 
                     color=[colors[c] for c in criterias],
                     alpha=0.8, 
                     edgecolor='black',
                     linewidth=1)
        
        # Add value labels on bars
        for j, (bar, nodes) in enumerate(zip(bars, avg_nodes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{nodes}',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.set_title(f'Iris Dataset - Depth {depth}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Total Nodes', fontsize=12)
        ax.set_ylim(0, max(max(iris_nodes_data[c]['avg_nodes']) for c in criterias) * 1.2)
        ax.grid(True, alpha=0.3, axis='y')
    
    # Add overall title
    fig.suptitle('Average Total Nodes Comparison by Criteria and Depth', fontsize=16, fontweight='bold', y=0.95)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('nodes_bar_plots_by_depth.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_nodes_line_comparison():
    """Create line plots showing nodes vs depth for each criteria"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Colors and markers for each criteria
    colors = {'IG': '#1f77b4', 'IGR': '#ff7f0e', 'NWIG': '#2ca02c'}
    markers = {'IG': 'o', 'IGR': 's', 'NWIG': '^'}
    criterias = ['IG', 'IGR', 'NWIG']
    
    # Plot Adult Dataset
    ax1.set_title('Adult Dataset: Average Total Nodes vs Depth', fontsize=14, fontweight='bold')
    for criteria in criterias:
        depths = adult_nodes_data[criteria]['depths']
        avg_nodes = adult_nodes_data[criteria]['avg_nodes']
        
        # Plot line with markers
        ax1.plot(depths, avg_nodes, 
                color=colors[criteria], 
                marker=markers[criteria], 
                linewidth=3, 
                markersize=10, 
                label=criteria)
        
        # Add value labels on points
        for i, (depth, nodes) in enumerate(zip(depths, avg_nodes)):
            ax1.annotate(f'{nodes}', 
                        (depth, nodes), 
                        textcoords="offset points", 
                        xytext=(0,15), 
                        ha='center',
                        fontsize=10,
                        fontweight='bold')
    
    ax1.set_xlabel('Tree Depth', fontsize=12)
    ax1.set_ylabel('Average Total Nodes (log scale)', fontsize=12)
    ax1.set_xticks([2, 3, 4])
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_yscale('log')
    
    # Plot Iris Dataset
    ax2.set_title('Iris Dataset: Average Total Nodes vs Depth', fontsize=14, fontweight='bold')
    for criteria in criterias:
        depths = iris_nodes_data[criteria]['depths']
        avg_nodes = iris_nodes_data[criteria]['avg_nodes']
        
        # Plot line with markers
        ax2.plot(depths, avg_nodes, 
                color=colors[criteria], 
                marker=markers[criteria], 
                linewidth=3, 
                markersize=10, 
                label=criteria)
        
        # Add value labels on points
        for i, (depth, nodes) in enumerate(zip(depths, avg_nodes)):
            ax2.annotate(f'{nodes}', 
                        (depth, nodes), 
                        textcoords="offset points", 
                        xytext=(0,3), 
                        ha='center',
                        fontsize=10,
                        fontweight='bold')
    
    ax2.set_xlabel('Tree Depth', fontsize=12)
    ax2.set_ylabel('Average Total Nodes', fontsize=12)
    ax2.set_xticks([2, 3, 4])
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(15, 40)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('nodes_line_plots_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_combined_nodes_bar_comparison():
    """Create a combined bar plot comparing both datasets for each depth"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Colors
    colors = {'IG': '#1f77b4', 'IGR': '#ff7f0e', 'NWIG': '#2ca02c'}
    criterias = ['IG', 'IGR', 'NWIG']
    depths = [2, 3, 4]
    
    # Bar width and positions
    bar_width = 0.35
    x_pos = np.arange(len(criterias))
    
    for i, depth in enumerate(depths):
        ax = axes[i]
        
        # Get average nodes for this depth
        adult_nodes = [adult_nodes_data[criteria]['avg_nodes'][depth-2] for criteria in criterias]
        iris_nodes = [iris_nodes_data[criteria]['avg_nodes'][depth-2] for criteria in criterias]
        
        # Create grouped bar chart
        bars1 = ax.bar(x_pos - bar_width/2, adult_nodes, bar_width,
                      label='Adult Dataset', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x_pos + bar_width/2, iris_nodes, bar_width,
                      label='Iris Dataset', alpha=0.8, edgecolor='black')
        
        # Color bars according to criteria
        for j, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            bar1.set_color(colors[criterias[j]])
            bar2.set_color(colors[criterias[j]])
            bar2.set_alpha(0.6)  # Make iris bars slightly transparent
        
        # Add value labels on bars
        for j, (bar, nodes) in enumerate(zip(bars1, adult_nodes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                   f'{nodes}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        for j, (bar, nodes) in enumerate(zip(bars2, iris_nodes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.05,
                   f'{nodes}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_title(f'Depth {depth} - Node Count Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Total Nodes (log scale)', fontsize=12)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(criterias)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_yscale('log')
        
        if i == 0:  # Only show legend on first subplot
            ax.legend()
    
    # Add overall title
    fig.suptitle('Dataset Comparison: Average Total Nodes by Criteria and Depth', fontsize=16, fontweight='bold')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('combined_nodes_bar_comparison_by_depth.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_nodes_summary_table():
    """Create a summary table showing node statistics for each dataset"""
    print("=" * 80)
    print("AVERAGE TOTAL NODES SUMMARY")
    print("=" * 80)
    
    print("\nAdult Dataset:")
    print("-" * 50)
    print(f"{'Criteria':<8} {'Depth 2':<10} {'Depth 3':<10} {'Depth 4':<10}")
    print("-" * 50)
    for criteria in ['IG', 'IGR', 'NWIG']:
        nodes = adult_nodes_data[criteria]['avg_nodes']
        print(f"{criteria:<8} {nodes[0]:<10} {nodes[1]:<10} {nodes[2]:<10}")
    
    print("\nIris Dataset:")
    print("-" * 50)
    print(f"{'Criteria':<8} {'Depth 2':<10} {'Depth 3':<10} {'Depth 4':<10}")
    print("-" * 50)
    for criteria in ['IG', 'IGR', 'NWIG']:
        nodes = iris_nodes_data[criteria]['avg_nodes']
        print(f"{criteria:<8} {nodes[0]:<10} {nodes[1]:<10} {nodes[2]:<10}")
    
    # Growth analysis
    print(f"\nNode Growth Analysis:")
    print("-" * 50)
    print("Adult Dataset - Most nodes at depth 4:")
    adult_max_depth4 = max([adult_nodes_data[c]['avg_nodes'][2] for c in adult_nodes_data])
    for criteria in ['IG', 'IGR', 'NWIG']:
        if adult_nodes_data[criteria]['avg_nodes'][2] == adult_max_depth4:
            print(f"  {criteria}: {adult_max_depth4} nodes")
    
    print("Iris Dataset - Most nodes at depth 4:")
    iris_max_depth4 = max([iris_nodes_data[c]['avg_nodes'][2] for c in iris_nodes_data])
    for criteria in ['IG', 'IGR', 'NWIG']:
        if iris_nodes_data[criteria]['avg_nodes'][2] == iris_max_depth4:
            print(f"  {criteria}: {iris_max_depth4} nodes")

if __name__ == "__main__":
    print("Generating average total nodes vs depth plots...")
    
    # Create bar plots for each depth
    plot_nodes_vs_depth_bars()
    
    # Create line plots
    plot_nodes_line_comparison()
    
    # Create combined bar comparison
    plot_combined_nodes_bar_comparison()
    
    # Print summary
    create_nodes_summary_table()
    
    print("\nPlots saved as:")
    print("- nodes_bar_plots_by_depth.png (separate bar plots for each depth)")
    print("- nodes_line_plots_comparison.png (line plots comparison)")
    print("- combined_nodes_bar_comparison_by_depth.png (side-by-side bar comparison)")
