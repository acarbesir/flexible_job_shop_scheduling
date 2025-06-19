import sys
from datetime import timedelta
import bisect

def split_ms(pb_instance, ms):
    jobs = []
    current = 0
    for index, job in enumerate(pb_instance['jobs']):
        jobs.append(ms[current:current+len(job)])
        current += len(job)
    return jobs

def get_processing_time(op_by_machine, machine_nb):
    for op in op_by_machine:
        if op['machine'] == machine_nb:
            return op['processingTime']
    print("[ERROR] Machine {} doesn't to be able to process this task.".format(machine_nb))
    sys.exit(-1)

def is_free(tab, start, duration):
    for k in range(start, start+duration):
        if not tab[k]:
            return False
    return True

def find_first_available_place(start_ctr, duration, machine_jobs):
    busy_intervals = []
    for job in machine_jobs:
        start, process_time = job[3], job[1]
        end = start + process_time
        bisect.insort(busy_intervals, (start, end))

    busy_intervals.append((float('inf'), float('inf')))

    current_time = start_ctr
    while True:
        i = bisect.bisect_left(busy_intervals, (current_time, current_time))
        if i == 0 or busy_intervals[i-1][1] <= current_time:
            if busy_intervals[i][0] >= current_time + duration:
                return current_time
            else:
                current_time = busy_intervals[i][1]
        else:
            current_time = busy_intervals[i-1][1]

def split_operation(job, indexes, o, ms_s, start_task_cstr, machine_operations):
    index_machine = ms_s[job][indexes[job]]
    prcTime = o[job][indexes[job]][index_machine]['processingTime']
    baca_order_id = o[job][indexes[job]][index_machine]['baca_order_id']
    operation_id = o[job][indexes[job]][index_machine]['operation_id']

    # Calculate number of splits needed
    splits = min(len(o[job][indexes[job]]), prcTime // 720 + (1 if prcTime % 720 else 0))
    split_prcTime = prcTime // splits
    remaining_time = prcTime

    # Ensure we have enough machines for split
    if splits > len(o[job][indexes[job]]):
        raise ValueError(f"Not enough machines to split the operation {operation_id}.")

    split_end_times = []

    for split in range(splits):
        machine_id = o[job][indexes[job]][split]['machine']
        if split == splits - 1:  # Last split takes remaining time
            split_prcTime = remaining_time
        remaining_time -= split_prcTime

        start_cstr = start_task_cstr[job]
        start = find_first_available_place(start_cstr, split_prcTime, machine_operations[machine_id - 1])

        name_task = "{}-{}-p{}".format(job, indexes[job] + 1, split + 1)
        label = "{}/{}-p{}".format(baca_order_id, operation_id, split + 1)

        machine_operations[machine_id - 1].append((name_task, split_prcTime, start_cstr, start, label))

        split_end_times.append(start + split_prcTime)

    indexes[job] += 1

    # Update start_task_cstr[job] to the maximum end time of all splits
    start_task_cstr[job] = max(split_end_times)
    return start_task_cstr[job]

def decode(pb_instance, os, ms):
    o = pb_instance['jobs']
    machine_operations = [[] for _ in range(pb_instance['machinesNb'])]
    operation_splits_info = {}

    ms_s = split_ms(pb_instance, ms) 

    indexes = [0] * len(ms_s)
    start_task_cstr = [0] * len(ms_s)
    job_completion_times = [0] * len(pb_instance['jobs'])

    for job in os:
        index_machine = ms_s[job][indexes[job]]
        machine = o[job][indexes[job]][index_machine]['machine']
        prcTime = o[job][indexes[job]][index_machine]['processingTime']
        operation_type = o[job][indexes[job]][index_machine]['operation_type']
        target_cycle_time = o[job][indexes[job]][index_machine]['target_cycle_time']
        operation_id = o[job][indexes[job]][index_machine]['operation_id']

        if prcTime > 720 and operation_type != 'Dış Proses':
            job_completion_times[job] = split_operation(job, indexes, o, ms_s, start_task_cstr, machine_operations)

            operation_splits_info[operation_id] = {
                'target_cycle_time': target_cycle_time,
                'splits': prcTime // 720 + (1 if prcTime % 720 else 0),
                'operation_id': operation_id,
                'operation_type': operation_type
            }

        else:
            start_cstr = start_task_cstr[job]
            start = find_first_available_place(start_cstr, prcTime, machine_operations[machine - 1])

            baca_order_id = o[job][indexes[job]][index_machine]['baca_order_id']
            name_task = "{}-{}-p1".format(job, indexes[job] + 1)
            label = "{}/{}-p1".format(baca_order_id, operation_id)

            machine_operations[machine - 1].append((name_task, prcTime, start_cstr, start, label))

            indexes[job] += 1
            start_task_cstr[job] = (start + prcTime)
            job_completion_times[job] = start + prcTime

            operation_splits_info[operation_id] = {
                'target_cycle_time': target_cycle_time,
                'splits': 1,
                'operation_id': operation_id,
                'operation_type': operation_type
            }

    return machine_operations, job_completion_times, operation_splits_info

def translate_decoded_to_gantt(machine_operations, machine_names):
    data = {}

    for idx, machine in enumerate(machine_operations):
        machine_name = machine_names[idx]
        operations = []
        for operation in machine:
            operations.append([operation[3], operation[3] + operation[1], operation[0], operation[4]])

        data[machine_name] = operations

    return data

def check_deadlines(job_completion_times, deadlines, baca_order_ids, product_codes):
    missed_deadlines = []
    for i, completion_time in enumerate(job_completion_times):
        if completion_time > deadlines[i]:
            missed_deadlines.append({
                'baca_order_id': baca_order_ids[i],
                'product_code': product_codes[i],
                'completion_time': completion_time,
                'deadline': deadlines[i],
                'exceeded_by': completion_time - deadlines[i]
            })

    return missed_deadlines

def find_idle_times(machine_operations):
    idle_times = []
    for idx, machine in enumerate(machine_operations):
        idle_periods = []
        if not machine:
            idle_times.append(idle_periods)
            continue

        sorted_operations = sorted(machine, key=lambda x: x[3])
        previous_end_time = 0

        for operation in sorted_operations:
            start_time = operation[3]
            if start_time > previous_end_time:
                idle_periods.append((previous_end_time, start_time))
            previous_end_time = start_time + operation[1]

        idle_times.append(idle_periods)

    return idle_times

def convert_to_datetime(start_time, minutes):
    start = start_time + timedelta(minutes=minutes[0])
    end = start_time + timedelta(minutes=minutes[1])
    return start.strftime("%d.%m.%Y,%H:%M"), end.strftime("%d.%m.%Y,%H:%M")