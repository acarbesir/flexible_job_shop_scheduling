import json
from datetime import datetime, timedelta

def generate_json(data):
    machines_data = [] 
    start_time = datetime.now()

    for machine, operations in sorted(data.items()):
        sum = 0
        machine_id = machine
        operations_list = []

        for op in operations:
            if len(op) >= 3 and len(op[2]) >= 3:
                nums = op[3].strip("[]'")
                job_id, operation_id = nums.split('/')
                start_hour = start_time + timedelta(minutes=op[0])
                end_hour = start_hour + timedelta(minutes=op[1] - op[0])
                start_str = start_hour.strftime('%d.%m.%Y,%H:%M')
                end_str = end_hour.strftime('%d.%m.%Y,%H:%M')
                target_cycle_time = op[1] - op[0]
                sum += target_cycle_time

                operations_list.append({
                    "op_ID": operation_id,
                    "order_ID": job_id,
                    "tct": target_cycle_time,
                    "st": start_str,
                    "et": end_str
                })
            else:
                print(f"Invalid operation format: {op}")

        idle_periods = []

        machine_data = {
            "line": machine_id,
            "tpt": sum,
            "ops": operations_list,
            "it": idle_periods
        }

        machines_data.append(machine_data)  

    with open("output.json", "w", encoding='utf-8') as json_file:
        json.dump(machines_data, json_file, indent=4)
    

def parse(path):
    with open(path, 'r') as file:
        data = json.load(file)

    machinesNb = len(data['machines'])
    machine_ids = [machine['machine_id'] for machine in data['machines']]
    return {
        'machinesNb': machinesNb,
        'machine_ids': machine_ids,
    }