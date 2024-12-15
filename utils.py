import matplotlib.pyplot as plt

def plot_solution(solution, values, weights, capacity, save_path=None, ax=None):
    """
    Plots the selected items in the knapsack.
    
    Parameters:
        solution (list): Binary list representing the solution.
        values (list): List of item values.
        weights (list): List of item weights.
        capacity (int): Maximum capacity of the knapsack.
        save_path (str): Path to save the plot image. If None, displays the plot.
        ax (matplotlib.axes.Axes, optional): Axes object to plot on. If None, creates new figure.
    """
    selected_items = [i+1 for i, bit in enumerate(solution) if bit]
    total_value = sum(v for v, bit in zip(values, solution) if bit)
    total_weight = sum(w for w, bit in zip(weights, solution) if bit)
    
    print(f"\nSelected Items: {selected_items}")
    print(f"Total Value: {total_value}")
    print(f"Total Weight: {total_weight} / Capacity: {capacity}")
    
    # Create figure if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))
    
    # Bar Plot
    indices = range(1, len(solution) + 1)
    colors = ['green' if bit else 'red' for bit in solution]
    
    bars = ax.bar(indices, weights, color=colors, edgecolor='black')
    
    # Highlight selected items
    for bar, bit in zip(bars, solution):
        if bit:
            bar.set_edgecolor('gold')
            bar.set_linewidth(3)
    
    ax.axhline(y=capacity, color='blue', linestyle='--', label='Capacity')
    ax.set_title('Knapsack Items Selection')
    ax.set_xlabel('Item Number')
    ax.set_ylabel('Weight')
    ax.set_xticks(indices)
    ax.legend()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"Solution plot saved to {save_path}")
    elif ax is None:
        plt.show()

def plot_fitness_history(fitness_history, save_path=None, ax=None):
    """
    Plots the fitness history over generations.
    
    Parameters:
        fitness_history (list): List of best fitness values per generation.
        save_path (str): Path to save the plot image. If None, displays the plot.
        ax (matplotlib.axes.Axes, optional): Axes object to plot on. If None, creates new figure.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        
    ax.plot(range(1, len(fitness_history)+1), fitness_history, marker='o', linestyle='-', color='b')
    ax.set_title('Fitness Convergence Over Generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Best Fitness')
    ax.grid(True)
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"Fitness convergence plot saved to {save_path}")
    elif ax is None:
        plt.show()