import os
import re
import json
import time
import urllib.error
import urllib.request
import random

MAX_NODES = 4
MAX_CRASHED_NODES = 4

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def start_nodes():
    print(f'Starting {MAX_NODES} nodes...')
    try:
        nodesstr = os.popen(f"sh {os.path.join(SCRIPT_DIR, '../src/run-unjoined.sh')} {MAX_NODES}").read()
    except PermissionError as e:
        print(f'Error: {e}')
        return []

    nodesmatch = re.findall(r"\[.*\]", nodesstr)
    nodes = json.loads(nodesmatch[0])
    return nodes

def initialize_network(nodes):
    print("Initializing the network...")
    n_prime = nodes[0]
    for i in range(1, len(nodes)):
        try: 
            join_url = f"http://{nodes[i]}/join?nprime={n_prime}"
            req = urllib.request.Request(url=join_url, method="POST")
            urllib.request.urlopen(req)
            print(f"Node {nodes[i]} joined network.")
        except Exception as e: 
            print(f"Error initializing node {nodes[i]}: {e}")
    print("Network Initialized") 

def crash_node(node):
    print(f'Crashing node: {node}')
    try: 
        crash_url = f"http://{node}/sim-crash"
        req = urllib.request.Request(url=crash_url, method="POST")
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error crashing node {node}: {e}")

def recover_node(node):
    print(f'Recovering node: {node}')
    try: 
        recover_url = f"http://{node}/sim-recover"
        req = urllib.request.Request(url=recover_url, method="POST")
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error recovering node {node}: {e}")

def get_node_info(node):
    """Get node information such as node_hash, successor, and others."""
    try:
        node_info_url = f"http://{node}/node-info"
        response = urllib.request.urlopen(node_info_url)
        data = json.loads(response.read().decode())
        return data
    except urllib.error.HTTPError as e:
        if e.code == 503:
            print(f"Node {node} is currently crashed.")
            return None
        else:
            print(f"Error getting node info for {node}: {e}")
    except Exception as e:
        print(f"General error getting node info for {node}: {e}")
    return None

def validate_network(nodes):
    """Validate that the network is stable by checking successor/predecessor relationships."""
    all_ok = True
    for node in nodes:
        info = get_node_info(node)
        if not info:
            continue
        successor = info['successor']
        others = info['others']
        if not (successor and others):
            print(f"Node {node} has inconsistent state: Successor: {successor}, Others: {others}")
            all_ok = False
    return all_ok

def test_burst_crashes(nodes, max_crashes):
    results = []
    for burst_size in range(1, max_crashes + 1):
        print(f"Testing burst of {burst_size} node(s) crash...")
        crashed_nodes = random.sample(nodes, burst_size)

        # Simulate burst of crashes 
        for node in crashed_nodes:
            crash_node(node)
            time.sleep(1)
            if get_node_info(node) is not None:
                print(f"Node {node} is still operational after crash attempt.")
                results.append("no")
                break
        else:
            # Allow time for the network to stabilize after crashes
            time.sleep(5)

            # Validate the network state after the crashes
            if validate_network([node for node in nodes if node not in crashed_nodes]):
                # Attempt to recover nodes
                for node in crashed_nodes:
                    recover_node(node)
                    time.sleep(1)
                    if get_node_info(node) is None:
                        print(f"Node {node} did not recover correctly.")
                        results.append("no")
                        break
                else:
                    # Allow time for the network to stabilize after recovery
                    time.sleep(5)

                    # Validate the network state after recovery
                    if validate_network(nodes):
                        results.append("ok")
                    else:
                        results.append("no")
            else:
                results.append("no")

        # If the last test resulted in "no", stop further testing
        if results[-1] == "no":
            break

    # Print all results at the end
    for i, result in enumerate(results, 1):
        print(f"burst of node(s) {i}: {result}")

def shutdown_nodes(nodes):
    for node in nodes:
        try:
            shutdown_url = f"http://{node}/shutdown"
            req = urllib.request.Request(url=shutdown_url)
            urllib.request.urlopen(req)
            print(f"Node {node} shut down.")
        except Exception as e:
            print(f"Error shutting down node {node}: {e}")

if __name__ == "__main__":
    nodes = start_nodes()
    
    if nodes: 
        initialize_network(nodes)
        test_burst_crashes(nodes, MAX_CRASHED_NODES)
        shutdown_nodes(nodes)
    else: 
        print(f'No nodes')
