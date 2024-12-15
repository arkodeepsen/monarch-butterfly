# 🦋 Enhanced Monarch Butterfly Optimization Algorithm with Google Gemini AI Integration

## **Project Overview**
This project combines the Monarch Butterfly Optimization (MBO) algorithm with Google Gemini AI to address optimization problems such as the 0–1 Knapsack Problem. The MBO algorithm is enhanced for binary solutions, with Gemini AI generating problem statements, converting them into knapsack instances, and analyzing results. This integration improves solution quality, adaptability, and convergence rates.

---

## **Features**
- **Google Gemini AI Integration**: Automates problem generation, instance creation, and analytical insights.
- **Enhanced MBO Algorithm**: Tailored for discrete optimization with advanced mutation, migration, and local search.
- **Comprehensive Visualizations**: Includes fitness convergence plots and solution selection charts.
- **Scalable Implementation**: Supports large instances with high efficiency.

---

## **Project Structure**
```
mbo_knapsack_project/
├── mbo_core.py             # Core implementation of the Enhanced MBO algorithm
├── knapsack_problem.py     # Script to run the algorithm on knapsack instances
├── utils.py                # Utility functions for visualization and analysis
├── test_mbo_core.py        # Unit tests for the MBO algorithm
├── data/
│   └── knapsack_instances/ # Folder for knapsack instance files
│       ├── instance1.txt   # Example knapsack problem instance
│       └── ...             # Additional instances
├── results/
│   ├── graphs/             # Directory for output plots (fitness convergence, solutions)
│   └── logs/               # Logs for runtime and results
├── requirements.txt        # Python dependencies
├── LICENSE                 # Project license
└── README.md               # Project overview and instructions
```

---

## **Installation**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/arkodeepsen/Monarch-Butterfly.git
   cd mbo_knapsack_project
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**
### **Running the Knapsack Solver**
1. **Prepare Knapsack Instance**
   - Add your instance files in `data/knapsack_instances/` in the format:
     ```
     <capacity>
     <value1> <weight1>
     <value2> <weight2>
     ```

2. **Run the Solver**
   ```bash
   python knapsack_problem.py --instance data/knapsack_instances/instance1.txt --pop_size 50 --max_gen 100 --mutation_rate 0.05
   ```

3. **Parameters**
   - `--instance`: Path to the knapsack instance file.
   - `--pop_size`: Population size (default: 50).
   - `--max_gen`: Number of generations (default: 100).
   - `--mutation_rate`: Mutation probability (default: 0.01).
   - `--save_plots`: Save plots as images in `results/graphs/`.

---

## **Example**
```bash
python knapsack_problem.py --instance data/knapsack_instances/instance1.txt --pop_size 50 --max_gen 100 --mutation_rate 0.05 --save_plots
```
- **Output**:
  - Best solution, fitness, and runtime in the terminal.
  - Saved plots: 
    - `fitness_convergence_<instance_name>.png`
    - `knapsack_solution_<instance_name>.png`
    - `solution_plot.png`
    - `fitness_history.png`

---

## **Unit Testing**
Run tests to validate the core functionality:
```bash
python -m unittest test_mbo_core.py
```

---

## **Visualization**
- **Fitness Convergence**: Tracks fitness improvements over generations.

![Fitness History](fitness_history.png)

- **Knapsack Solution**: Highlights selected items and their weights.

![Solution Plot](solution_plot.png)

---

## **Contributing**
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Acknowledgements**
Special thanks to the faculty of JIS College of Engineering for their guidance and support throughout this project.