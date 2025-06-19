from src.genetic import decoding

def WeightedFitness(os_ms, pb_instance, weights):
    makespan = MinMakespan(os_ms, pb_instance)
    deadline_penalty = MinDeadlineTardiness(os_ms, pb_instance)
    utility = MaxMachineUtilization(os_ms, pb_instance)

    weighted_fitness = (
        weights[0] * makespan +
        weights[1] * deadline_penalty +
        weights[2] * utility
    )

    return weighted_fitness

# Only deadline considered
def MinDeadlineTardiness(os_ms, pb_instance):
    (os, ms) = os_ms
    decoded, job_completion_times, operation_splits_info = decoding.decode(pb_instance, os, ms)

    deadlines = pb_instance['deadlines']
    penalty = 0

    job_end_times = [0] * len(deadlines)

    for machine in decoded:
        for job in machine:
            job_id = int(job[0].split('-')[0])
            end = job[3] + job[1]
            job_end_times[job_id] = max(job_end_times[job_id], end)

    for job_id, end_time in enumerate(job_end_times):
        if end_time > deadlines[job_id]:
            penalty += (end_time - deadlines[job_id])
    
    return penalty

# Only maksepan considered
def MinMakespan(os_ms, pb_instance):
    (os, ms) = os_ms
    decoded, job_completion_times, operation_splits_info = decoding.decode(pb_instance, os, ms)

    max_per_machine = []

    for machine in decoded:
        max_d = 0
        for job in machine:
            end = job[3] + job[1]
            if end > max_d:
                max_d = end
        max_per_machine.append(max_d)

    return max(max_per_machine)

def MaxMachineUtilization(os_ms, pb_instance):
    (os, ms) = os_ms
    decoded, job_completion_times, operation_splits_info = decoding.decode(pb_instance, os, ms)
    
    machine_utilities = []
    for machine in decoded:
        if machine:
            total_processing_time = sum(job[1] for job in machine)
            max_end_time = max(job[3] + job[1] for job in machine)
            utility = max_end_time - total_processing_time if max_end_time > 0 else 0
            machine_utilities.append(utility)
    
    return sum(machine_utilities) if machine_utilities else 0

# Method to select which function will be used (makespan, deadline, utilization)
def CalculateFitness(os_ms, pb_instance, methodIndex, weights):
    if methodIndex == 0:
        return MinMakespan(os_ms, pb_instance)
    elif methodIndex == 1:
        return MinDeadlineTardiness(os_ms, pb_instance)
    elif methodIndex == 2:
        return MaxMachineUtilization(os_ms, pb_instance)
    elif methodIndex == 4:
        return WeightedFitness(os_ms, pb_instance, weights)