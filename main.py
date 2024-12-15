import tkinter as tk
from tkinter import ttk, scrolledtext
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os, json, re, PIL.Image, io
from pathlib import Path
from knapsack_problem import main_knapsack_mbo, load_knapsack_instance
from utils import plot_fitness_history, plot_solution
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Configure Google AI
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-exp')
story = genai.GenerativeModel('gemini-1.5-flash-latest')

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.setup_ui()
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash-8b')
        Path('data/knapsack_instances').mkdir(parents=True, exist_ok=True)

    def setup_ui(self):
        # Left panel for controls
        left_panel = ttk.Frame(self.root, padding="10")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Generate problem button
        ttk.Button(left_panel, text="Generate Problem", command=self.generate_problem).pack(pady=5)
        
        # Parameters
        param_frame = ttk.LabelFrame(left_panel, text="Parameters", padding="5")
        param_frame.pack(fill=tk.X, pady=5)
        
        self.pop_size = tk.StringVar(value="50")
        self.max_gen = tk.StringVar(value="100")
        self.mutation_rate = tk.StringVar(value="0.05")
        
        ttk.Label(param_frame, text="Population Size:").pack()
        ttk.Entry(param_frame, textvariable=self.pop_size).pack()
        
        ttk.Label(param_frame, text="Max Generations:").pack()
        ttk.Entry(param_frame, textvariable=self.max_gen).pack()
        
        ttk.Label(param_frame, text="Mutation Rate:").pack()
        ttk.Entry(param_frame, textvariable=self.mutation_rate).pack()
        
        # Add capacity input
        ttk.Label(param_frame, text="Knapsack Capacity:").pack()
        self.capacity = tk.StringVar(value="50")
        ttk.Entry(param_frame, textvariable=self.capacity).pack()
        
        # Add additional prompt input
        ttk.Label(param_frame, text="Additional Prompt:").pack()
        self.additional_prompt = tk.StringVar()
        ttk.Entry(param_frame, textvariable=self.additional_prompt).pack()
        
        # Solve button
        ttk.Button(left_panel, text="Solve Problem", command=self.solve_problem).pack(pady=5)
        
        # Right panel for display
        right_panel = ttk.Frame(self.root, padding="10")
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Problem description
        self.problem_text = scrolledtext.ScrolledText(right_panel, width=150, height=10)
        self.problem_text.pack(pady=5)
        
        # Results
        self.result_text = scrolledtext.ScrolledText(right_panel, width=150, height=10)
        self.result_text.pack(pady=5)
        
        # Plots frame
        self.plots_frame = ttk.Frame(right_panel)
        self.plots_frame.pack(fill=tk.BOTH, expand=True)

    def generate_problem(self):
        additional_prompt = self.additional_prompt.get()
        prompt = f"""Create a complex knapsack problem scenario with these requirements:
        1. Write an engaging story about resource optimization
        2. Include 15-20 items with varying properties
        3. Items should have:
            - Monetary value (100-5000 range)
            - Weight (1-50 range)
            - Category (A/B/C priority)
            - Risk factor (1-10)
        4. Format each item as:
        1. ItemName - value: X, weight: Y, category: Z, risk: W
        
        Make values and weights have complex trade-offs.
        
        Additional instruction from user: {additional_prompt}"""
        
        response = story.generate_content(prompt)
        problem_text = response.text
        
        print("\nAI Generated Problem:")
        print("-" * 50)
        print(problem_text)
        
        self.problem_text.delete('1.0', tk.END)
        self.problem_text.insert('1.0', self.format_markdown(problem_text))
        
        self.create_instance_files(problem_text)

    def format_markdown(self, text):
        # Simple markdown to plain text conversion
        text = text.replace('**', '').replace('*', '')
        return text

    def create_instance_files(self, problem_text):
        prompt = """Extract items from this text and return a clean JSON object in this exact format (no extra text):
        {"items":[{"name":"name","value":1000,"weight":10,"category":"A","risk":5}]}"""
    
        try:
            # Get AI response
            response = self.ai_model.generate_content([prompt, problem_text])
            response_text = response.text.strip()
            
            # Clean response - remove markdown formatting if present
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            response_text = response_text.strip()
            
            print("\nAI Response (cleaned):")
            print("-" * 50)
            print(response_text)
            
            # Parse JSON
            parsed_data = json.loads(response_text)
            items = parsed_data['items']
            
            if not items:
                raise ValueError("No items found in AI response")
                
            # Log parsed items
            print("\nParsed Items:")
            print("-" * 50)
            for item in items:
                print(f"{item['name']}: value={item['value']}, weight={item['weight']}, "
                      f"category={item['category']}, risk={item['risk']}")
            
            # Extract properties
            values = [item['value'] for item in items]
            weights = [item['weight'] for item in items]
            categories = [item['category'] for item in items]
            risks = [item['risk'] for item in items]
            
            # Create instance files
            capacity = int(self.capacity.get())
            total_weight = sum(weights)
            
            for i, (items_percent, cap_percent) in enumerate(
                zip([0.4, 0.6, 0.8], [0.4, 0.5, 0.6]), 1):
                
                num_items = int(len(values) * items_percent)
                filename = f'data/knapsack_instances/instance{i}.txt'
                
                with open(filename, 'w') as f:
                    adjusted_capacity = int(total_weight * cap_percent)
                    f.write(f"{adjusted_capacity}\n")
                    
                    selected_items = list(zip(values[:num_items], weights[:num_items],
                                           categories[:num_items], risks[:num_items]))
                    
                    for v, w, c, r in selected_items:
                        risk_mult = 1 + (r/10)
                        cat_mult = {'A': 1.2, 'B': 1.0, 'C': 0.8}[c]
                        final_value = int(v * risk_mult * cat_mult)
                        f.write(f"{final_value} {w}\n")
                
                print(f"\nCreated instance file: {filename}")
                print(f"Items: {num_items}, Capacity: {adjusted_capacity}")
            
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', 
                f"Successfully generated {len(items)} items\n"
                f"Value range: {min(values)}-{max(values)}\n"
                f"Weight range: {min(weights)}-{max(weights)}\n"
                f"Created {i} instance files")
                
        except Exception as e:
            error_msg = f"Error processing items: {str(e)}\nResponse: {response_text}"
            print(error_msg)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', error_msg)

    def explain_results(self, plot_path, graph_path, data):
        try:
            # Open and convert images to PIL format
            plot_image = PIL.Image.open(plot_path)
            graph_image = PIL.Image.open(graph_path)
            
            # Prepare prompt for AI
            prompt = f"""Analyze the optimization results and explain:
            1. Quality of the solution found
            2. Convergence behavior
            3. Population diversity trends
            4. Key insights about the solution
            NOTE: You are playing the role of an AI analyst here. No need for salutations or greetings. DIRECTLY provide the analysis.
            Data: {data}"""
            
            # Send prompt and images to AI
            response = model.generate_content([prompt, plot_image, graph_image])
            
            # Display AI response
            explanation = response.text
            print("\nAI Explanation:")
            print("-" * 50)
            print(explanation)
            
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', self.format_markdown(explanation))
            
        except Exception as e:
            error_msg = f"Error explaining results: {str(e)}"
            print(error_msg)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', error_msg)

    def solve_problem(self):
        # Load instance
        values, weights, capacity = load_knapsack_instance('data/knapsack_instances/instance1.txt')
        
        # Run MBO
        best_sol, best_fit, fitness_history, diversity_history = main_knapsack_mbo(
            values, weights, capacity,
            pop_size=int(self.pop_size.get()),
            max_generations=int(self.max_gen.get()),
            mutation_rate=float(self.mutation_rate.get())
        )
        
        # Display results
        result = f"Best Fitness: {best_fit}\n"
        result += f"Best Solution: {best_sol}\n"
        result += f"Total Weight: {sum(w for w, bit in zip(weights, best_sol) if bit)}"
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', result)
        
        # Clear old plots
        for widget in self.plots_frame.winfo_children():
            widget.destroy()
        
        # Create new plots
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        plot_fitness_history(fitness_history, ax=ax1)
        canvas1 = FigureCanvasTkAgg(fig1, self.plots_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        plot_path = 'fitness_history.png'
        fig1.savefig(plot_path)
        
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        plot_solution(best_sol, values, weights, capacity, ax=ax2)
        canvas2 = FigureCanvasTkAgg(fig2, self.plots_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        graph_path = 'solution_plot.png'
        fig2.savefig(graph_path)
        
        # Prepare data for explanation
        data = {
            "best_fitness": best_fit,
            "best_solution": best_sol,
            "total_weight": sum(w for w, bit in zip(weights, best_sol) if bit),
            "fitness_history": fitness_history,
            "diversity_history": diversity_history
        }
        
        # Explain results using AI
        self.explain_results(plot_path, graph_path, data)

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()