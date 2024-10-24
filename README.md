Here is the revised README in English, with the requested adjustments:

---

# INF-3200: Assignment 2 - Dynamic Membership

## Table of Contents

- [Overview](#overview)
- [Implementation Details](#implementation-details)
- [Deployment and Setup](#deployment-and-setup)
- [Testing](#testing)
- [Cleanup](#cleanup)

## Overview

This project extends the Assignment 1 by adding **dynamic membership**. Nodes should be able to **join** and **leave** the network dynamically. The system includes an expanded **HTTP API** to manage dynamic node operations and simulate node failures.

## Implementation Details

- The project is developed in **Rust**, building upon the foundation laid in Assignment 1.
- Nodes are organized using a hash function that determines their position in the Chord ring.
- Core server logic is implemented in `main.rs`, while key-value storage operations are handled by the `Storage` struct in `storage.rs`.
- The `run-node.sh` script starts individual nodes, while `run.sh` coordinates the deployment of multiple nodes and sets up the Chord-like network with dynamic membership features.

## Deployment and Setup

### Prerequisites

1. **Log in to the compute cluster** where the system will be deployed.
2. **Download the deployment script** using the following commands:

   ```bash
   wget https://raw.githubusercontent.com/SeraMadeleine/INF3200-2/master/src/run.sh
   chmod 552 run.sh
   ```
**NB**: if you have an old version of the repo, you have to delete the following folder from the cluster ``` inf2300-a1-bin-x86_64-unknown-linux-gnu```

### Deployment Options

- The system can be deployed as a containerized service (e.g., using Docker) or as a binary for Linux (x86_64) and macOS (aarch64).
- Ensure that all dependencies are installed and network configurations are set according to the assignment requirements before running.

## Testing

### Api check  
The system can be tested using the `api_check.py` script to verify that all API endpoints comply with the specifications. 

> **Note:** For compatibility with Rust, a `Content-Type` header has been added to the tests. This modification is included in the version of the test script located at `python_tests/api_check.py`.

#### Running the API Check

1. **Start the system:**  
   Run the following command to start the system:
   ```sh
   ../src/run-unjoined.sh 4 8001
   ```
   Copy the output after running this command.

2. **Run the API check:**  
   Execute the `api_check.py` script using the command below, replacing `[nodes]` with the list of nodes output from the previous step:
   ```sh
   python3 api_check.py '[nodes]'
   ```
   For example:
   ```sh
   python3 api_check.py '["c11-3:52769","c6-2:49970","c3-29:52453","c3-13:64421"]'
   ```


### Dynamic join and leav 
- Performance testing can be conducted to validate that the network maintains its functionality and stability as nodes dynamically join or leave.
- Additionally, the `join_and_leave.sh` script, found in `python_tests/join_and_leave_test.py`, can be used to measure the times and results. This script generates the metrics and output that are used in the report.

### 


## Cleanup

After completing the testing and tasks, it's recommended to **clean up** the cluster to release resources. This can be done by running the following command:

   ```bash
   /share/ifi/cleanup.sh
   ```
