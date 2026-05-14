import time
import random
import threading
import pandas as pd
import matplotlib.pyplot as plt
import psutil

from codecarbon import EmissionsTracker

# ======================================================
# SIMPLE TASK
# ======================================================

def simple_task(task_id):

    start = time.time()

    total = 0

    for i in range(1000000):
        total += i

    execution_time = time.time() - start

    return {
        "task_id": task_id,
        "difficulty": "Low",
        "time": execution_time
    }

# ======================================================
# MEDIUM TASK
# ======================================================

def medium_task(task_id):

    start = time.time()

    data = []

    for i in range(500000):
        data.append(i * random.random())

    processed = sum(data)

    execution_time = time.time() - start

    return {
        "task_id": task_id,
        "difficulty": "Medium",
        "result": processed,
        "time": execution_time
    }

# ======================================================
# COMPLEX TASK
# ======================================================

def complex_task(task_id):

    start = time.time()

    matrix = [[random.random() for _ in range(300)] for _ in range(300)]

    result = 0

    for row in matrix:
        for value in row:
            result += value * random.random()

    execution_time = time.time() - start

    return {
        "task_id": task_id,
        "difficulty": "High",
        "result": result,
        "time": execution_time
    }

# ======================================================
# MONOLITHIC AI
# ======================================================

class MonolithicAI:

    def process_task(self, task_type, task_id):

        if task_type == "low":
            return simple_task(task_id)

        elif task_type == "medium":
            return medium_task(task_id)

        elif task_type == "high":
            return complex_task(task_id)

# ======================================================
# AGENT
# ======================================================

class Agent:

    def __init__(self, name):
        self.name = name

    def execute(self, task_type, task_id):

        time.sleep(0.2)

        if task_type == "low":
            return simple_task(task_id)

        elif task_type == "medium":
            return medium_task(task_id)

        elif task_type == "high":
            return complex_task(task_id)

# ======================================================
# MULTI AGENT SYSTEM
# ======================================================

class MultiAgentSystem:

    def __init__(self):

        self.agents = [
            Agent("Reasoning Agent"),
            Agent("Validation Agent"),
            Agent("Refinement Agent")
        ]

    def process_task(self, task_type, task_id):

        results = []

        for agent in self.agents:
            result = agent.execute(task_type, task_id)
            results.append(result)

        return results

# ======================================================
# SEQUENTIAL EXECUTION
# ======================================================

def sequential_execution(system, task_type, num_tasks):

    print("\nSequential Execution Started")

    tracker = EmissionsTracker()
    tracker.start()

    start_time = time.time()

    results = []

    for i in range(num_tasks):
        results.append(system.process_task(task_type, i))

    total_time = time.time() - start_time

    emissions = tracker.stop()

    print("Sequential Execution Completed")

    return {
        "type": "Sequential",
        "time": total_time,
        "emissions": emissions,
        "results": results
    }

# ======================================================
# THREAD WORKER
# ======================================================

def worker(system, task_type, task_id, output):

    result = system.process_task(task_type, task_id)

    output.append(result)

# ======================================================
# PARALLEL EXECUTION
# ======================================================

def parallel_execution(system, task_type, num_tasks):

    print("\nParallel Execution Started")

    tracker = EmissionsTracker()

    tracker.start()

    start_time = time.time()

    threads = []

    results = []

    for i in range(num_tasks):

        thread = threading.Thread(
            target=worker,
            args=(system, task_type, i, results)
        )

        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()

    total_time = time.time() - start_time

    emissions = tracker.stop()

    print("Parallel Execution Completed")

    return {
        "type": "Parallel",
        "time": total_time,
        "emissions": emissions,
        "results": results
    }

# ======================================================
# SYSTEM MONITORING
# ======================================================

def system_usage():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory().percent

    return {
        "CPU Usage": cpu,
        "Memory Usage": memory
    }

# ======================================================
# ANALYSIS
# ======================================================

def analyze_results(data):

    df = pd.DataFrame(data)

    print("\nPerformance Summary")
    print(df)

    # Execution Time Graph

    plt.figure(figsize=(10, 5))

    plt.bar(df['Architecture'], df['Execution Time'])

    plt.xlabel("Architecture")
    plt.ylabel("Execution Time")
    plt.title("Execution Time Comparison")

    plt.savefig("graphs/execution_time.png")

    plt.show()

    # Emissions Graph

    plt.figure(figsize=(10, 5))

    plt.bar(df['Architecture'], df['Emissions'])

    plt.xlabel("Architecture")
    plt.ylabel("Carbon Emissions")

    plt.title("Energy Consumption Comparison")

    plt.savefig("graphs/emissions.png")

    plt.show()

# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    NUM_TASKS = 5

    results = []

    # ==========================================
    # MONOLITHIC SYSTEM
    # ==========================================

    monolithic = MonolithicAI()

    print("\n==========================")
    print("MONOLITHIC AI SYSTEM")
    print("==========================")

    seq_result = sequential_execution(
        monolithic,
        "medium",
        NUM_TASKS
    )

    results.append({
        "Architecture": "Monolithic Sequential",
        "Execution Time": seq_result["time"],
        "Emissions": seq_result["emissions"]
    })

    par_result = parallel_execution(
        monolithic,
        "medium",
        NUM_TASKS
    )

    results.append({
        "Architecture": "Monolithic Parallel",
        "Execution Time": par_result["time"],
        "Emissions": par_result["emissions"]
    })

    # ==========================================
    # MULTI AGENT SYSTEM
    # ==========================================

    multi_agent = MultiAgentSystem()

    print("\n==========================")
    print("MULTI AGENT AI SYSTEM")
    print("==========================")

    seq_result = sequential_execution(
        multi_agent,
        "medium",
        NUM_TASKS
    )

    results.append({
        "Architecture": "Multi-Agent Sequential",
        "Execution Time": seq_result["time"],
        "Emissions": seq_result["emissions"]
    })

    par_result = parallel_execution(
        multi_agent,
        "medium",
        NUM_TASKS
    )

    results.append({
        "Architecture": "Multi-Agent Parallel",
        "Execution Time": par_result["time"],
        "Emissions": par_result["emissions"]
    })

    # ==========================================
    # SYSTEM USAGE
    # ==========================================

    usage = system_usage()

    print("\nSystem Usage")
    print(usage)

    # ==========================================
    # ANALYSIS
    # ==========================================

    analyze_results(results)