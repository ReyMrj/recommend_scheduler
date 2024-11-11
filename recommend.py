def round_robin(processes, quantum):
    n = len(processes)
    remaining_burst_time = [p['burst_time'] for p in processes]
    turnaround_times = [0] * n
    waiting_times = [0] * n

    time = 0
    while True:
        done = True
        for i in range(n):
            if remaining_burst_time[i] > 0:
                done = False  # There is still a pending process
                if remaining_burst_time[i] > quantum:
                    time += quantum
                    remaining_burst_time[i] -= quantum
                else:
                    time += remaining_burst_time[i]
                    waiting_times[i] = time - processes[i]['burst_time']
                    turnaround_times[i] = time
                    remaining_burst_time[i] = 0

        if done:
            break

    avg_turnaround_time = sum(turnaround_times) / n
    avg_waiting_time = sum(waiting_times) / n
    throughput = n / time

    return throughput, avg_turnaround_time, avg_waiting_time


def calculate_metrics(processes, algorithm, quantum=None):
    n = len(processes)
    total_burst_time = sum(p['burst_time'] for p in processes)

    if algorithm == "SJF":
        processes = sorted(processes, key=lambda x: x['burst_time'])
    elif algorithm == "FCFS":
        pass  # FCFS doesn't need sorting
    elif algorithm == "EDF":
        processes = sorted(processes, key=lambda x: x['deadline'])
    elif algorithm == "WSJF":
        processes = sorted(processes, key=lambda x: (x['weight'] / x['burst_time']), reverse=True)
    elif algorithm == "Round Robin" and quantum:
        return round_robin(processes, quantum)

    turnaround_times = [0] * n
    waiting_times = [0] * n
    elapsed_time = 0

    for i, p in enumerate(processes):
        waiting_times[i] = elapsed_time
        turnaround_times[i] = waiting_times[i] + p['burst_time']
        elapsed_time += p['burst_time']

    avg_turnaround_time = sum(turnaround_times) / n
    avg_waiting_time = sum(waiting_times) / n
    throughput = n / elapsed_time

    return throughput, avg_turnaround_time, avg_waiting_time


def recommend_algorithm(processes, user_preference, quantum):
    scores = {}
    algorithms = ["FCFS", "SJF", "EDF", "WSJF", "Round Robin"]

    for algo in algorithms:
        if algo == "Round Robin":
            throughput, turnaround_time, waiting_time = calculate_metrics(processes, algo, quantum)
        else:
            throughput, turnaround_time, waiting_time = calculate_metrics(processes, algo)

        score = 0
        if user_preference == "efficiency":
            if algo == "Round Robin":
                score += 4
            elif throughput > 0.2:
                score += 2
        if user_preference == "short_jobs" and algo == "SJF":
            score += 4
        if user_preference == "deadlines" and algo == "EDF":
            score += 4

        scores[algo] = {
            "score": score,
            "throughput": throughput,
            "turnaround_time": turnaround_time,
            "waiting_time": waiting_time
        }

    recommended_algorithm = max(scores, key=lambda k: scores[k]["score"])
    return recommended_algorithm, scores


def main():
    quantum = int(input("Enter the time quantum for Round Robin (ms): "))
    user_preference = input("\nDo you prefer any specific scheduling characteristic?\n1. 'efficiency': Fast processing for most jobs.\n2. 'short_jobs': Prioritizes shorter jobs.\n3. 'deadlines': Favors jobs with specific deadlines.\nEnter your choice or press Enter for default: ")
    
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    
    for i in range(num_processes):
        burst_time = int(input(f"Enter burst time for Process {i+1}: "))
        priority = input(f"Enter priority for Process {i+1} (or leave blank): ")
        deadline = input(f"Enter deadline for Process {i+1} (or leave blank): ")
        weight = input(f"Enter weight for Process {i+1} (or leave blank): ")
        process_type = input(f"Enter type for Process {i+1} ('interactive' or 'batch'): ").strip().lower()
        
        while process_type not in ['interactive', 'batch']:
            print("Invalid input. Please enter 'interactive' or 'batch' only.")
            process_type = input(f"Enter type for Process {i+1} ('interactive' or 'batch'): ").strip().lower()
        
        process = {
            'burst_time': burst_time,
            'priority': int(priority) if priority else None,
            'deadline': int(deadline) if deadline else None,
            'weight': int(weight) if weight else None,
            'type': process_type
        }
        processes.append(process)

    recommended_algorithm, scores = recommend_algorithm(processes, user_preference, quantum)
    
    print("\n### Scheduling Recommendation System ###\n")
    print(f"**Recommended Algorithm**: {recommended_algorithm}")
    print(f"**Score**: {scores[recommended_algorithm]['score']}/10")
    print("**Metrics for Recommended Algorithm**:")
    print(f"  - Throughput: {scores[recommended_algorithm]['throughput']}")
    print(f"  - Turnaround Time: {scores[recommended_algorithm]['turnaround_time']}")
    print(f"  - Waiting Time: {scores[recommended_algorithm]['waiting_time']}\n")
    
    print("**Alternative Algorithms to Consider**:")
    for algo, metrics in scores.items():
        if algo != recommended_algorithm:
            print(f"- **{algo}** (Score: {metrics['score']}/10)")
            print(f"  **Metrics**:")
            print(f"    - Throughput: {metrics['throughput']}")
            print(f"    - Turnaround Time: {metrics['turnaround_time']}")
            print(f"    - Waiting Time: {metrics['waiting_time']}\n")


if __name__ == "__main__":
    main()
