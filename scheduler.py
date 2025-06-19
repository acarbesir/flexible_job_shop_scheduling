import math
from src.utils import parser
import time
import multiprocessing as mp

from src.genetic import decoding, encoding
from src.genetic.objective import CalculateFitness

from src.genetic.operators.crossover import Crossover
from src.genetic.operators.mutation import Mutation
from src.genetic.operators.selection import Selection

class Scheduler:
    def __init__(self, parameters, config):
        self.parameters = parameters
        self.config = config

    def run(self):
        # 0 -> Minimize makespan
        # 1 -> Minimize deadline tardiness
        # 2 -> Maximize machine utilization
        # 3 -> Weighted
        method_index = int(self.config["objective_type"])

        parameters = parser.parse("input.json")

        if method_index == 3:
            weights = [float(self.config["weight_min_makespan"]),
                       float(self.config["weight_min_deadline_tardiness"]),
                       float(self.config["weight_max_machine_utilization"])]
        else:
            weights = [0, 0, 0, 0]

        t0 = time.time()

        population = encoding.initializePopulation(parameters, self.config)
        gen = 1

        fitness_values = []
        mean_fitness_values = []

        no_improvement_count = 0
        
        with mp.Pool(mp.cpu_count()) as pool:
            while gen <= self.config["max_gen"]:
                population = Selection(population, parameters, method_index, weights, self.config)
                population = Crossover(population, parameters, self.config)
                population = Mutation(population, parameters, self.config)

                fitness_results = pool.starmap(CalculateFitness, [(ind, parameters, method_index, weights) for ind in population])
                
                current_best_fitness = min(fitness_results)
                current_mean_fitness = sum(fitness_results) / len(fitness_results)

                fitness_values.append(current_best_fitness)
                mean_fitness_values.append(current_mean_fitness)

                if len(fitness_values) > 1:
                    previous_best_fitness = fitness_values[-2]
                    if abs(previous_best_fitness - current_best_fitness) < self.config["improvement_threshold"]:
                        no_improvement_count += 1
                    else:
                        no_improvement_count = 0

                    if no_improvement_count >= self.config["max_stagnant_step"]:
                        break
                
                print(f"Generation {gen} completed")
                gen += 1

        sortedPop = sorted(population, key=lambda cpl: CalculateFitness(cpl, parameters, method_index, weights))

        t1 = time.time()
        total_time = t1 - t0
        print("Finished in {0:.2f}s\n".format(total_time))

        machine_operations, job_completion_times, operation_splits_info = decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1])

        print("Required operators for operations:")
        B = 3

        for operation_id, info in operation_splits_info.items():
            if info['operation_type'] != 'Dış Proses':
                target_cycle_time = info['target_cycle_time']
                number_of_shifts = info['splits']
                
                EMPO = B / math.sqrt(target_cycle_time)
                RO = math.ceil(number_of_shifts / EMPO)
                if int(RO) != 1:
                    print(f"Operation {operation_id} requires {int(RO)} operators.")
                else:
                    print(f"Operation {operation_id} requires {int(RO)} operator.")
        print()

        missed_deadlines = decoding.check_deadlines(job_completion_times, parameters['deadlines'], parameters['baca_order_ids'], parameters['product_codes'])

        return {
            "machine_operations": machine_operations,
            "job_completion_times": job_completion_times,
            "operation_splits_info": operation_splits_info,
            "missed_deadlines": missed_deadlines,
            "fitness_values": fitness_values,
            "mean_fitness_values": mean_fitness_values
        }