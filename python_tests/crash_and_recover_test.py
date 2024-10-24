import os
import re
import json
import time
import urllib.error
import urllib.request
import random
import uuid

RESULTS_FILE = "res.txt"
MAX_NODES = 2
MAX_CRASHED_NODES = 1

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
            # Join each node to n_prime (the first node in the list) to build the network 
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

def check_node_status(node):
    try:
        node_info_url = f"http://{node}/node-info"
        response = urllib.request.urlopen(node_info_url)
        if response.status == 200:
            print(f"Node {node} is operational.")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 503:
            print(f"Node {node} is currently crashed.")
            return False
        else:
            print(f"Error checking status of node {node}: {e}")
    except Exception as e:
        print(f"General error checking status of node {node}: {e}")
    return False

def test_burst_crashes(nodes, max_crashes):
    for burst_size in range(1, max_crashes + 1):
        print(f"Testing burst of {burst_size} node(s) crash...")
        crashed_nodes = random.sample(nodes, burst_size)

        # Simulate burst of crashes 
        for node in crashed_nodes:
            crash_node(node)

            time.sleep(1)

            if not check_node_status(node):
                print(f"Node {node} has been confirmed as crashed.")
            else:
                print(f"Node {node} is still operational after crash attempt. Check again.")
        
        # Allow time for the network to stabilize after crashes
        time.sleep(5)

        # Recover the crashed nodes 
        for node in crashed_nodes: 
            recover_node(node)

            time.sleep(1)
            # Check if the node has recovered
            if check_node_status(node):
                print(f"Node {node} has been confirmed as recovered.")
            else:
                print(f"Node {node} did not recover correctly. Check again.")

        # Allow time for the network to stabilize after recovery
        time.sleep(5)

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
        print("No nodes")
