import os
import sys
import json
import time
import re
import urllib.request
import numpy as np

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

        # Start nodes again for each repeat to ensure availability
        print(f"Starting nodes for repeat {repeat + 1}...")
        run_script_output = os.popen(f"sh ../src/run-unjoined.sh {len(nodes)}").read()
        print("Deployment Output:\n", run_script_output)  # Log the output for debugging

        # Extract node addresses from the output
        node_list_match = re.search(r'\[".*"\]', run_script_output)
        if not node_list_match:
            print(f"Failed to extract node list for repeat {repeat + 1} from run-unjoined.sh output.")
            continue

        node_list_json = node_list_match.group()
        nodes = json.loads(node_list_json)

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
            except urllib.error.URLError as e:
                print(f"Error: Node {node} failed to join. Error: {e}")
            except Exception as e:
                print(f"Unexpected error when node {node} tried to join: {e}")

        if join_times:
            all_join_times.append(join_times)
        else:
            print(f"Skipping repeat {repeat + 1} due to errors.")

    # If no successful joins occurred, return None
    if not all_join_times:
        return None

    # Ensure all join times are of equal length for creating a consistent numpy array
    min_length = min(len(join_times) for join_times in all_join_times)
    all_join_times = [join_times[:min_length] for join_times in all_join_times]

    # Convert to NumPy array for easier calculations
    all_join_times = np.array(all_join_times)

    # Calculate mean and standard deviation across repeats for each node join time
    join_avg = np.mean(all_join_times, axis=0)
    join_std = np.std(all_join_times, axis=0)

    return {
        "join_avg": join_avg.tolist(),  # Convert to list for JSON serialization
        "join_std": join_std.tolist(),  # Convert to list for JSON serialization
        "total_time": float(np.sum(join_avg)),  # Convert to float for JSON serialization
        "joins_count": int(len(join_avg))
    }

def shutdown_nodes(nodes):
    for node in nodes:
        print(f"Shutting down node: {node}")
        try:
            response = urllib.request.urlopen(f"http://{node}/shutdown", timeout=5)
            response.read()
        except urllib.error.URLError as e:
            print(f"Error shutting down node {node}: {e}")
        except Exception as e:
            print(f"Unexpected error when shutting down node {node}: {e}")

if __name__ == "__main__":
    node_counts = [2, 4, 8]
    results = []

    for node_count in node_counts:
        print(f"\nStarting test with {node_count} nodes...")
        run_script_output = os.popen(f"sh ../src/run-unjoined.sh {node_count}").read()
        print("Deployment Output:\n", run_script_output)  # Log the output for debugging

        # Extract node addresses from the output
        node_list_match = re.search(r'\[".*"\]', run_script_output)
        if not node_list_match:
            print(f"Failed to extract node list from run-unjoined.sh output for {node_count} nodes.")
            continue

        node_list_json = node_list_match.group()
        nodes = json.loads(node_list_json)

        # Check if the number of nodes matches the expected count
        if len(nodes) < node_count:
            print(f"Warning: Requested {node_count} nodes, but only {len(nodes)} were deployed.")
            continue

        print("Running dynamic joining test...")
        test_result = dynamic_joining_test(nodes)

        if not test_result:
            print("Dynamic joining test encountered an issue for {node_count} nodes.")
        else:
            print("Dynamic joining test completed successfully for {node_count} nodes.")

            # Calculate mean and standard deviation
            join_avg = np.mean(test_result["join_avg"])
            join_std = np.std(test_result["join_std"])

            result_entry = {
                "nodes": node_count,
                "join_avg": join_avg,
                "join_std": join_std,
                "total_time": test_result["total_time"],
                "joins_count": test_result["joins_count"]
            }
            results.append(result_entry)

        shutdown_nodes(nodes)

    # Write results to res.txt file
    with open("res.txt", "w") as f:
        f.write("no_finger_results = ")
        json.dump(results, f, indent=2)

    print("All tests completed! Results saved to res.txt")
