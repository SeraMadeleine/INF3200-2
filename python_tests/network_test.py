import os
import sys
import json
import time
import re
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

def dynamic_joining_test(nodes, timeout=5, repeats=3):
    """
    Joins each node in the nodes list dynamically for a given number of repeats.
    Returns the mean and standard deviation of the measured join times.
    """
    all_join_times = []

    # Repeat the experiment for the specified number of times
    for repeat in range(repeats):
        join_times = []
        print(f"\nStarting repeat {repeat + 1}...")

        # The first node is the initial node that others will join through
        single_node = nodes[0]
        other_nodes = nodes[1:]

        # Measure the time to join each node dynamically
        for node in other_nodes:
            join_start_time = time.time()
            join_url = f"http://{node}/join?nprime={single_node}"
            req = urllib.request.Request(url=join_url, method="POST")
            try:
                print(f"Attempting to join node {node} with nprime={single_node}")
                response = urllib.request.urlopen(req, timeout=timeout)
                if response.status == 200:
                    join_time = time.time() - join_start_time
                    join_times.append(join_time)
                    print(f"Node {node} joined in {join_time:.2f} seconds")
                else:
                    print(f"Error: Node {node} failed to join. Status code: {response.status}")
                    return False
            except urllib.error.URLError as e:
                print(f"Error: Node {node} failed to join. Error: {e}")
                return False
            except Exception as e:
                print(f"Unexpected error when node {node} tried to join: {e}")
                return False

        all_join_times.append(join_times)

    # Convert to NumPy array for easier calculations
    all_join_times = np.array(all_join_times)

    # Calculate mean and standard deviation across repeats for each node join time
    join_avg = np.mean(all_join_times, axis=0)
    join_std = np.std(all_join_times, axis=0)

    return {
        "join_avg": join_avg,
        "join_std": join_std,
        "total_time": np.sum(join_avg),
        "joins_count": len(join_avg)
    }

def shutdown_nodes(nodes):
    for node in nodes:
        print(f"Shutting down node: {node}")
        try:
            response = urllib.request.urlopen(f"http://{node}/shutdown", timeout=5)
            response.read()
        except urllib.error.URLError as e:
            print(f"Error shutting down node {node}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <node count>")
        print(f"Example: python3 {sys.argv[0]} 32")
        sys.exit(1)

    try:
        node_count = int(sys.argv[1])
    except ValueError:
        print("Invalid node count provided.")
        sys.exit(1)

    # Start nodes using run-unjoined.sh and capture the output
    print(f"Starting {node_count} nodes...")
    run_script_output = os.popen(f"sh ../src/run-unjoined.sh {node_count}").read()
    print("Deployment Output:\n", run_script_output)  # Log the output for debugging

    # Extract node addresses from the output
    node_list_match = re.search(r'\[".*"\]', run_script_output)
    if not node_list_match:
        print("Failed to extract node list from run-unjoined.sh output.")
        sys.exit(1)

    node_list_json = node_list_match.group()
    nodes = json.loads(node_list_json)

    # Check if the number of nodes matches the expected count
    if len(nodes) < node_count:
        print(f"Warning: Requested {node_count} nodes, but only {len(nodes)} were deployed.")
        sys.exit(1)

    print("Running dynamic joining test...")
    test_result = dynamic_joining_test(nodes)

    if not test_result:
        print("Dynamic joining test encountered an issue.")
    else:
        print("Dynamic joining test completed successfully.")
        print(json.dumps(test_result, indent=2))

        # Plotting the results
        mean_values = test_result['join_avg']
        std_values = test_result['join_std']
        node_indices = np.arange(1, len(mean_values) + 1)

        plt.errorbar(node_indices, mean_values, yerr=std_values, fmt='o-', ecolor='r', capsize=5, label='Join Times')
        plt.xlabel('Node Index')
        plt.ylabel('Join Time (s)')
        plt.title('Mean Join Times with Standard Deviation')
        plt.legend()
        plt.grid(True)
        plt.show()

    shutdown_nodes(nodes)
    print("Test done!")
