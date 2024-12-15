# mbo_core.py

import random

def generate_random_solution(num_items):
    """
    Generates a random binary solution for the knapsack problem.
    
    Parameters:
        num_items (int): Number of items in the knapsack.
    
    Returns:
        list: A binary list representing the solution.
    """
    return [random.randint(0, 1) for _ in range(num_items)]

def initialize_population(pop_size, num_items):
    """
    Initializes the population with random solutions.
    
    Parameters:
        pop_size (int): Number of solutions in the population.
        num_items (int): Number of items in the knapsack.
    
    Returns:
        list: A list of binary solutions.
    """
    return [generate_random_solution(num_items) for _ in range(pop_size)]

def fitness(solution, values, weights, capacity):
    """
    Evaluates the fitness of a solution.
    
    Parameters:
        solution (list): Binary list representing the solution.
        values (list): List of item values.
        weights (list): List of item weights.
        capacity (int): Maximum capacity of the knapsack.
    
    Returns:
        int: Total value if feasible, else 0.
    """
    total_value = sum(v for v, bit in zip(values, solution) if bit)
    total_weight = sum(w for w, bit in zip(weights, solution) if bit)
    if total_weight > capacity:
        return 0
    else:
        return total_value

def repair(solution, weights, capacity, values):
    """
    Repairs an infeasible solution by removing items until it's feasible.
    
    Parameters:
        solution (list): Binary list representing the solution.
        weights (list): List of item weights.
        capacity (int): Maximum capacity of the knapsack.
        values (list): List of item values.
    
    Returns:
        list: A feasible binary solution.
    """
    repaired = solution.copy()
    total_weight = sum(w for w, bit in zip(weights, repaired) if bit)
    
    if total_weight <= capacity:
        return repaired
    
    # Calculate value-to-weight ratio
    ratio = [(v / w, idx) for idx, (v, w) in enumerate(zip(values, weights)) if repaired[idx] == 1]
    # Sort items by ratio in ascending order
    ratio.sort()
    
    # Remove items with lowest ratio first
    for r, idx in ratio:
        repaired[idx] = 0
        total_weight -= weights[idx]
        if total_weight <= capacity:
            break
    return repaired

def split_population(population):
    """
    Splits the population into two subpopulations.
    
    Parameters:
        population (list): The current population.
    
    Returns:
        tuple: Two subpopulations.
    """
    mid = len(population) // 2
    return population[:mid], population[mid:]

def single_point_crossover(parent1, parent2):
    """
    Performs single-point crossover between two parents.
    
    Parameters:
        parent1 (list): First parent solution.
        parent2 (list): Second parent solution.
    
    Returns:
        tuple: Two child solutions.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of same length")
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def migration_phase(population):
    """
    Performs the migration phase using crossover between subpopulations.
    
    Parameters:
        population (list): The current population.
    
    Returns:
        list: Migrated population.
    """
    subpop_a, subpop_b = split_population(population)
    migrated = []
    
    # Perform crossover between corresponding pairs
    for i in range(len(subpop_a)):
        parent1 = subpop_a[i]
        parent2 = subpop_b[i % len(subpop_b)]  # Handle unequal subpop sizes
        child1, child2 = single_point_crossover(parent1, parent2)
        migrated.extend([child1, child2])
    
    # If population size was odd, handle the last element
    if len(population) % 2 != 0:
        migrated.append(population[-1])
    
    return migrated

def mutate(solution, mutation_rate):
    """
    Mutates a solution by flipping bits with a given probability.
    
    Parameters:
        solution (list): Binary solution to mutate.
        mutation_rate (float): Probability of flipping each bit.
    
    Returns:
        list: Mutated solution.
    """
    mutated = solution.copy()
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]  # Flip bit
    return mutated

def local_search(solution, values, weights, capacity):
    """
    Applies local search to improve a solution by adding items.
    
    Parameters:
        solution (list): Binary solution to improve.
        values (list): List of item values.
        weights (list): List of item weights.
        capacity (int): Maximum capacity of the knapsack.
    
    Returns:
        list: Improved solution.
    """
    improved = solution.copy()
    current_value = sum(v for v, bit in zip(values, improved) if bit)
    current_weight = sum(w for w, bit in zip(weights, improved) if bit)
    
    for i in range(len(improved)):
        if improved[i] == 0:
            new_weight = current_weight + weights[i]
            if new_weight <= capacity:
                new_value = current_value + values[i]
                # Check if adding this item improves the value
                if new_value > current_value:
                    improved[i] = 1
                    current_value = new_value
                    current_weight = new_weight
    return improved

def mutate_and_search(population, mutation_rate, values, weights, capacity):
    """
    Applies mutation and local search to the population.
    
    Parameters:
        population (list): Current population.
        mutation_rate (float): Mutation probability.
        values (list): List of item values.
        weights (list): List of item weights.
        capacity (int): Maximum capacity of the knapsack.
    
    Returns:
        list: Population after mutation and local search.
    """
    new_population = []
    for sol in population:
        mutated = mutate(sol, mutation_rate)
        repaired = repair(mutated, weights, capacity, values)
        searched = local_search(repaired, values, weights, capacity)
        new_population.append(searched)
    return new_population

def select_next_generation(population, fitness_values, pop_size):
    """
    Selects the top solutions to form the next generation.
    
    Parameters:
        population (list): Combined population.
        fitness_values (list): Fitness values of the combined population.
        pop_size (int): Desired population size.
    
    Returns:
        list: Selected next generation population.
    """
    # Combine population and fitness
    combined = list(zip(population, fitness_values))
    # Sort based on fitness in descending order
    combined.sort(key=lambda x: x[1], reverse=True)
    # Select top pop_size solutions
    selected = [sol for sol, fit in combined[:pop_size]]
    return selected

def calculate_diversity(population):
    """Calculate population diversity using Hamming distance"""
    if not population:
        return 0
    n = len(population)
    diversity = 0
    for i in range(n):
        for j in range(i + 1, n):
            diversity += sum(a != b for a, b in zip(population[i], population[j]))
    return diversity / (n * (n-1) / 2) if n > 1 else 0

def tournament_selection(population, fitness_values, tournament_size=5):
    """Select parents using tournament selection"""
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(range(len(population)), tournament_size)
        winner = max(tournament, key=lambda x: fitness_values[x])
        selected.append(population[winner].copy())
    return selected

def main_knapsack_mbo(values, weights, capacity, pop_size=50, max_generations=100, mutation_rate=0.01, verbose=True):
    """Enhanced MBO with adaptive mechanisms and diversity preservation"""
    num_items = len(values)
    population = initialize_population(pop_size, num_items)
    population = [repair(sol, weights, capacity, values) for sol in population]
    
    best_solution = None
    best_fitness = 0
    fitness_history = []
    diversity_history = []
    
    # Control parameters
    min_mutation = mutation_rate
    max_mutation = 0.1
    diversity_threshold = 0.3
    stagnation_limit = 20
    stagnation_counter = 0
    
    for generation in range(max_generations):
        # Calculate diversity
        diversity = calculate_diversity(population)
        diversity_history.append(diversity)
        
        # Adapt mutation rate
        current_mutation = min_mutation + (max_mutation - min_mutation) * (1 - diversity/1.0)
        
        # Evaluate fitness
        fitness_values = [fitness(sol, values, weights, capacity) for sol in population]
        current_best = max(fitness_values)
        
        # Update best solution
        if current_best > best_fitness:
            best_fitness = current_best
            best_solution = population[fitness_values.index(current_best)]
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        fitness_history.append(best_fitness)
        
        if verbose:
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}, Diversity = {diversity:.3f}")
        
        # Check for stagnation
        if stagnation_counter >= stagnation_limit:
            # Inject diversity
            num_refresh = pop_size // 4
            population[-num_refresh:] = initialize_population(num_refresh, num_items)
            stagnation_counter = 0
        
        # Enhanced migration with tournament selection
        parents = tournament_selection(population, fitness_values)
        migrated_population = migration_phase(parents)
        
        # Adaptive mutation and local search
        mutated_population = mutate_and_search(migrated_population, current_mutation, 
                                             values, weights, capacity)
        
        # Repair solutions
        repaired_population = [repair(sol, weights, capacity, values) for sol in mutated_population]
        
        # Elitism: preserve best solutions
        elite_size = pop_size // 10
        elite_indices = sorted(range(len(fitness_values)), 
                             key=lambda k: fitness_values[k], 
                             reverse=True)[:elite_size]
        elite = [population[i].copy() for i in elite_indices]
        
        # Combine populations
        combined_population = elite + repaired_population
        combined_fitness = ([fitness(sol, values, weights, capacity) 
                           for sol in combined_population])
        
        # Selection for next generation
        population = select_next_generation(combined_population, combined_fitness, pop_size)
    
    if verbose:
        print("\nOptimization Complete!")
        print(f"Best Fitness: {best_fitness}")
        print(f"Best Solution: {best_solution}")
        print(f"Final Diversity: {diversity:.3f}")
        total_weight = sum(w for w, bit in zip(weights, best_solution) if bit)
        print(f"Total Weight: {total_weight}")
    
    return best_solution, best_fitness, fitness_history, diversity_history
