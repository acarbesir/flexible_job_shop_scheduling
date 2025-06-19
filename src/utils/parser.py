#!/usr/bin/env python

import json
from datetime import datetime

def parse(path):
    with open(path, 'r') as file:
        data = json.load(file)

    jobs = []
    deadlines = []
    baca_order_ids= []
    product_codes= []
    
    now = datetime.now()
    

    for job in data['orders']:
        operations = []
        deadline_str = job['deadline']
        deadline = datetime.strptime(deadline_str, '%d.%m.%Y')
        time_diff = deadline - now
        deadline_in_minutes = int(time_diff.total_seconds() / 60)
        deadlines.append(deadline_in_minutes)
        quantity = job['quantity']
        baca_order_id = job['baca_order_id']
        product_code = job['product_code']

        baca_order_ids.append(baca_order_id)
        product_codes.append(product_code)

        for operation in job['operations']:
            op = []
            operation_id = operation['operation_id']
            operation_type = operation['operation_type']
            new_machine = {
                    'machine_id': len(data['machines']) + 1,
                    'machine_name': f'EXTERNAL PROCESS {product_code}',
                    'machine_availability': True
                }

            for machine in operation['available_machines']:
                if operation_type == 'Dış Proses':
                    machine['machine_id'] = len(data['machines']) + 1
                    data['machines'].append(new_machine)
                    processing_time = machine['target_cycle_time'] #+ operation['setup_time']
                else:
                    processing_time = machine['target_cycle_time'] * quantity #+ operation['setup_time']
                op.append({
                    'machine': machine['machine_id'],
                    'processingTime': processing_time,
                    'target_cycle_time': machine['target_cycle_time'],
                    'baca_order_id': baca_order_id,
                    'operation_id': operation_id,
                    'operation_type': operation_type
                })
            operations.append(op)
        
        jobs.append(operations)
    
    machinesNb = len(data['machines'])
    machine_availabilities = [machine['machine_availability'] for machine in data['machines']]
    machine_names = [machine['machine_name'] for machine in data['machines']]


    return {
        'machinesNb': machinesNb,
        'jobs': jobs,
        'deadlines': deadlines,
        'baca_order_ids': baca_order_ids,
        'product_codes': product_codes,
        'machine_availabilities': machine_availabilities,
        'machine_names': machine_names,
    }

