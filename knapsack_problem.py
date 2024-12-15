# knapsack_problem.py

from mbo_core import main_knapsack_mbo
from utils import plot_fitness_history, plot_solution
import os

def load_knapsack_instance(file_path):
    """
    Loads a knapsack problem instance from a file.
    
    Parameters:
        file_path (str): Path to the instance file.
    
    Returns:
        tuple: (values, weights, capacity)
    """
    values = []
    weights = []
    capacity = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
        capacity = int(lines[0].strip())
        for line in lines[1:]:
            if line.strip():  # Ensure the line is not empty
                v, w = map(int, line.strip().split())
                values.append(v)
                weights.append(w)
    return values, weights, capacity

def main():
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Enhanced MBO for 0–1 Knapsack Problem')
    parser.add_argument('--instance', type=str, required=True, help='Path to knapsack instance file')
    parser.add_argument('--pop_size', type=int, default=50, help='Population size')
    parser.add_argument('--max_gen', type=int, default=100, help='Number of generations')
    parser.add_argument('--mutation_rate', type=float, default=0.01, help='Mutation rate')
    parser.add_argument('--save_plots', action='store_true', help='Save plots instead of displaying them')
    args = parser.parse_args()

    # Load the instance
    values, weights, capacity = load_knapsack_instance(args.instance)
    
    print(f"Knapsack Capacity: {capacity}")
    print(f"Number of Items: {len(values)}")

    # Run MBO for Knapsack
    best_sol, best_fit, fitness_history = main_knapsack_mbo(
        values, weights, capacity, pop_size=args.pop_size, 
        max_generations=args.max_gen, mutation_rate=args.mutation_rate
    )

    # Define paths for saving plots
    base_name = os.path.splitext(os.path.basename(args.instance))[0]
    fitness_plot_path = os.path.join('results', 'graphs', f'fitness_convergence_{base_name}.png')
    solution_plot_path = os.path.join('results', 'graphs', f'knapsack_solution_{base_name}.png')

    # Ensure the results/graphs directory exists
    os.makedirs('results/graphs', exist_ok=True)

    if args.save_plots:
        # Save plots to files
        plot_fitness_history(fitness_history, save_path=fitness_plot_path)
        plot_solution(best_sol, values, weights, capacity, save_path=solution_plot_path)
    else:
        # Display plots interactively
        plot_fitness_history(fitness_history)
        plot_solution(best_sol, values, weights, capacity)

if __name__ == "__main__":
    main()
