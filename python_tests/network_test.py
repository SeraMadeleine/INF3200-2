import os
import re
import json
import subprocess
import time
import statistics
import urllib.request
import numpy as np

RESULTS_FILE = "res.txt"
ITERATIONS = 3
NODE_COUNTS = [2, 4, 8, 16, 32]
MAX_NODES = max(NODE_COUNTS)

# Get the absolute path of the current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def remove_previous_results():
    # Remove previous results file if exists
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

def start_nodes():
    print("Starting 32 nodes...")
    try:
        nodesstr = os.popen(f" sh {os.path.join(SCRIPT_DIR, '../src/run-unjoined.sh')} {MAX_NODES}").read()
    except PermissionError as e:
        print(f'error {e}')
    # print("nodes started")

    nodesmatch = re.findall("\\[.*\\]", nodesstr)
    nodes = json.loads(nodesmatch[0])

    return nodes

def join_nodes(nodes):
    n_prime = nodes[0]
    node_count = 1 
    join_times = [] 

    for target_node_count in NODE_COUNTS:
        # print(f"Target node count: {target_node_count}")
        join_start_time = time.time()
        while node_count < target_node_count:
            # print(f"Joining {nodes[node_count-1]} to {n_prime}") 
            join_url = f"http://{nodes[node_count-1]}/join?nprime={n_prime}"
            req = urllib.request.Request(url=join_url, method="POST")

            node_count += 1

        join_end_time = time.time()
        join_times.append(join_end_time - join_start_time)
    print(f' join times {join_times}')

    return join_times
    
def leave_nodes(nodes):
    leave_times = [] 
    node_count = NODE_COUNTS[-1]

    for target_node_count in reversed(NODE_COUNTS):
        # print(f"Target node count: {target_node_count}")

        leave_start_time = time.time()
        while node_count > target_node_count: 
            leave_url = f'https://{nodes[node_count-1]}/leave'
            req = urllib.request.Request(url=leave_url, method="POST")

            node_count -= 1
        leave_end_time = time.time()
        leave_times.append(leave_end_time - leave_start_time)
    print(f' leave times {leave_times}')

    return leave_times

def shutdown_nodes(nodes):
    for node in nodes:
        # print(f"Shutting down node: {node}")
        response = urllib.request.urlopen(f"http://{node}/shutdown").read()

def calculate_stats(times):
    avg = sum(times) / len(times) if times else 0
    std = statistics.stdev(times) if len(times) > 1 else 0
    return avg, std

if __name__ == "__main__":
    nodes = start_nodes()
    # print(f'nodes: {nodes}')
    all_join_times = {node_count: [] for node_count in NODE_COUNTS}
    all_leave_times = {node_count: [] for node_count in NODE_COUNTS}
    
    for i in range(ITERATIONS): 
        join_times = join_nodes(nodes)
        leave_times = leave_nodes(nodes)
        
        for idx, node_count in enumerate(NODE_COUNTS):
            all_join_times[node_count].append(join_times[idx])
            all_leave_times[node_count].append(leave_times[idx])

    for node_count in NODE_COUNTS:
        join_avg = np.mean(all_join_times[node_count])
        join_std = np.std(all_join_times[node_count])
        leave_avg = np.mean(all_leave_times[node_count])
        leave_std = np.std(all_leave_times[node_count])

        result = {
                'nodes': node_count,
                'join_avg': join_avg,
                'join_std': join_std,
                'leave_avg': leave_avg,
                'leave_std': leave_std
            }
        print(f'{result}, ')
        
        # print(f'Node count: {node_count}')
        # print(f'  Join - Avg: {join_avg:.6f}, Std: {join_std:.6f}')
        # print(f'  Leave - Avg: {leave_avg:.6f}, Std: {leave_std:.6f}')

    shutdown_nodes(nodes)
    remove_previous_results()

