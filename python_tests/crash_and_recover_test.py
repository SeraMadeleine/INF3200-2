import os
import re
import json
import time
import urllib.error
import uuid
import statistics
import urllib.request
import random
import numpy as np

RESULTS_FILE = "res.txt"
ITERATIONS = 1000
MAX_NODES = 32 
MAX_CRASHED_NODES = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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

def initilize_network(nodes):
    print("Initializing the network...")
    n_prime = nodes[0]
    for i in range(1, MAX_NODES):
        try: 
            # Join each node to nprime (the first node in the list) to build a network 
            join_url = f"http://{nodes[i]}/join?nprime={n_prime}"
            urllib.request.Request(url=join_url, method="POST")
        except Exception as e: 
            print(f"Error initializing node {nodes[i]}: {e}")
    print("Network Initilized") 

def crash_node(node):
    print(f'Chrashing node: {node}')
    try: 
        join_url = f"http://{node}/sim-crash"
        urllib.request.Request(url=join_url, method="POST")
        print(f"Node {node} crashed.")
    except Exception as e:
        print(f"Error crashing node {node}: {e}")


def recover_node(node):
    print(f'Recovering node: {node}')
    try: 
        join_url = f"http://{node}/sim-recover"
        urllib.request.Request(url=join_url, method="POST")
        print(f"Node {node} recovering.")
    except Exception as e:
        print(f"Error recovering node {node}: {e}")



def put_get_test(nodes):
    # send put req til noder med en alue, også prøv å gette de og sjekk at de er det samme 
    key_value_to_test = [(uuid.uuid4(), uuid.uuid4()) for _ in range(1000)]

    for key, value in key_value_to_test:
            # print(f"PUT http://{random.choice(nodes)}/storage/{key}")
            req = urllib.request.Request(
                url=f"http://{random.choice(nodes)}/storage/{key}", 
                data=bytes(str(value).encode("utf-8")), 
                method="PUT"
            )
            req.add_header("Content-type", "text/plain")
            urllib.request.urlopen(req)

            success_counter = 0
            failure_counter = 0
            
    for key, value in key_value_to_test:
        # print(f"GET http://{random.choice(nodes)}/storage/{key}")
        try: 
            response = urllib.request.urlopen(f"http://{random.choice(nodes)}/storage/{key}").read()

            if response.decode("utf-8") == str(value):
                success_counter += 1
            else:
                failure_counter += 1 
        
        except urllib.error.HTTPError as e:
            failure_counter += 1
        

    print(f"Tested PUT-GET, {success_counter} successes, {failure_counter} failures")

def shutdown_nodes(nodes):
    for node in nodes:
        # print(f"Shutting down node: {node}")
        response = urllib.request.urlopen(f"http://{node}/shutdown").read()


def test_burst_crashes(nodes, max_crashes):
    for burst_size in range(1, max_crashes+1):
        print(f"Testing burst of {burst_size} node(s) crash...")
        crashed_nodes = random.sample(nodes, burst_size)

        # simulate burst of chrashes 
        for node in crashed_nodes:
            crash_node(node)
        
         # Allow time for the network to stabilize after crashes
        time.sleep(10)

        # test if the network still is consistent 
        put_get_test(nodes)     # ?? vil nettverket stablisere seg på egenhånd så jeg kan gjøre det slik, eller må jeg tweeke noe

        # recover the crashed nodes 
        for node in crashed_nodes: 
            recover_node(node)

        # Allow time for the network to stabilize after recovery
        time.sleep(5) 

        # test if the network still is consistent 
        put_get_test(nodes)
        
    pass 

if __name__ == "__main__":
    nodes = start_nodes()
    
    if nodes: 
        initilize_network(nodes)
        test_burst_crashes(nodes, MAX_CRASHED_NODES)
        shutdown_nodes(nodes)
    else: 
        print(f'No nodes')


