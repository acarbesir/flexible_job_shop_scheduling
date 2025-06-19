from scheduler import Scheduler
from src.utils import parser, gantt, plot, latex
from src.genetic import decoding
from src import append
from src.config import read_config

def main():
    config = read_config("config.json")
    parameters = parser.parse("input.json")

    result = Scheduler(parameters, config).run()

    if result["missed_deadlines"]:
        print("Products that missed deadlines:")
        for entry in result["missed_deadlines"]:
            print("Product {}/{} exceeded the deadline by {} minutes.".format(entry['baca_order_id'], entry['product_code'], entry['exceeded_by']))
    else:
        print("No order missed their deadlines.")

    gantt_data = decoding.translate_decoded_to_gantt(result["machine_operations"], parameters['machine_names'])

    if config["latex_export"]:
        latex.export_latex(gantt_data)
        append.generate_json(gantt_data)
        gantt.draw_chart(gantt_data)
    else:
        gantt.draw_chart(gantt_data)
    
    plot.plot_deadlines_vs_completion(parameters['deadlines'], result["job_completion_times"], parameters['baca_order_ids'], parameters['product_codes'])
    plot.plot_generational_fitness(result["fitness_values"], result["mean_fitness_values"])

if __name__ == '__main__':
    main()