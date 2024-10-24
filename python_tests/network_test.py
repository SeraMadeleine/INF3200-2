import os
import sys
import json
import time
import re
import urllib.request
import numpy as np

def dynamic_joining_test(nodes, timeout=5):
    """Joins each node in the nodes list dynamically."""
    join_times = []

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

    # Calculate mean and standard deviation
    join_avg = np.mean(join_times)
    join_std = np.std(join_times)

    return {
        "join_avg": join_avg,
        "join_std": join_std,
        "total_time": sum(join_times),
        "joins_count": len(join_times)
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

    shutdown_nodes(nodes)

    print("Test done!")
    print(json.dumps(test_result, indent=2))
