import requests
import time
import statistics

num_tests = 3  # Number of times to run each experiment

def join_node(node, nprime):
    """API call to join a node to the network."""
    url = f"http://{node}/join?nprime={nprime}"
    response = requests.post(url)
    return response.status_code

def leave_node(node):
    """API call for a node to leave the network."""
    url = f"http://{node}/leave"
    response = requests.post(url)
    return response.status_code

def check_stability(nodes):
    """Check if all nodes in the network are stable."""
    stable = True

    # Check if each node is reachable and stable 
    for node in nodes:
        try:
            response = requests.get(f"http://{node}/node-info")
            if response.status_code != 200:
                stable = False
                break
        except requests.ConnectionError:
            stable = False
            break
    return stable

# Experiment 1: Grow network to 32 nodes, and record time for each join
def experiment_growth(initial_nodes, total_nodes):
    """Measure the time taken to add each node to the network."""
    all_join_times = []
    for _ in range(num_tests):  
        current_nodes = initial_nodes.copy()
        join_times = []

        # Add nodes until we reach the target number
        for i in range(len(current_nodes), total_nodes):
            node = f"node-{i}:8080"
            start_time = time.time()
            join_node(node, current_nodes[0])  
            current_nodes.append(node)

            # Wait until network is stable before adding the next node
            while not check_stability(current_nodes): 
                time.sleep(1)
            end_time = time.time()

            # Record time for this join
            join_times.append(end_time - start_time)  
        all_join_times.append(join_times)
    
    return all_join_times

# Experiment 2: Shrink network back to 1 node, and record time for each leave
def experiment_shrink(initial_nodes, target_nodes):
    """Measure the time taken to remove each node from the network."""
    all_leave_times = []
    for _ in range(num_tests):  # Run the experiment multiple times
        current_nodes = initial_nodes.copy()
        leave_times = []

        # Remove nodes until we reach the target number 
        while len(current_nodes) > target_nodes:
            start_time = time.time()
            leave_node(current_nodes.pop()) 
            
            # Wait until network is stable before removing the next node
            while not check_stability(current_nodes): 
                time.sleep(1)
            end_time = time.time()
            leave_times.append(end_time - start_time)  
        all_leave_times.append(leave_times)
    
    return all_leave_times

# Running experiments
initial_nodes = [f"node-{i}:8080" for i in range(32)]  # Initial 32 nodes in the network

# Experiment 1: Grow to 32 nodes, and capture individual join times
growth_times = experiment_growth(initial_nodes[:1], 32)
print(f"Growth times for each node: {growth_times}")

# Experiment 2: Shrink from 32 to 1 node, and capture individual leave times
shrink_times = experiment_shrink(initial_nodes, 1)
print(f"Shrink times for each node: {shrink_times}")


