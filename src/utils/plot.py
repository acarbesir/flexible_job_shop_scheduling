import matplotlib.pyplot as plt

def plot_deadlines_vs_completion(deadlines, completion_times, baca_order_ids, product_codes):
    job_labels = [f"{baca_order_ids[i]}/{product_codes[i]}" for i in range(len(baca_order_ids))]
    
    plt.figure(figsize=(10, 6))
    plt.plot(job_labels, deadlines, 'r-', marker='o', label='Deadline')
    
    plt.plot(job_labels, completion_times, 'b-', marker='o', label='Completion Time')
    
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Jobs')
    plt.ylabel('Time (minutes from now)')
    plt.title('Job Deadlines vs Completion Times')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('deadlines_vs_completion_times.png')
    plt.show()

def plot_generational_fitness(fitness_values, mean_fitness_values):
    generations = range(1, len(fitness_values) + 1)

    plt.plot(generations, fitness_values, label='best', color='b')
    plt.plot(generations, mean_fitness_values, label='mean', color='g')
    plt.title('Fitness Value over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('fitness_values_over_generations.png')  
    plt.show()