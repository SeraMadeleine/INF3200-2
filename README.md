# INF-3200, Assignment 2 

## Overview 

## Implementation Details

- The project is written in **Rust**.
- Core server logic is implemented in `main.rs`.
- Key-value storage operations are handled by the `Storage` struct located in `storage.rs`.
- `run-node.sh` script is used to deploy individual nodes.
- `run.sh` orchestrates the deployment of multiple nodes and configures the Chord-like network.

## Deployment

The server can be deployed in a **containerized environment** or distributed as a **binary** for Linux (x86_64) and macOS (aarch64) platforms.

## Setup and Downloading

1. **Log in to the cluster** where you intend to deploy the system.
2. **Download the script** by running the following commands:

   ```bash
   wget https://raw.githubusercontent.com/SeraMadeleine/INF3200-1B/master/src/run.sh
   chmod 552 run.sh
   ```

## Running the System

1. **Run the deployment script**:

   ```bash
   ./run.sh <number_of_nodes> [size_of_finger_table]
   ```

   - `<number_of_nodes>`: The number of distributed nodes to deploy.
   - `[size_of_finger_table]` (optional): The size of the finger table used in the Chord DHT. If not provided, it defaults to 0.

2. After the script runs, it will output a **JSON array** containing the deployed services (node:port pairs).

## Testing 
### Running Basic Tests
To test the distributed key-value store, use the provided Python test script located in the `src` directory:

1. Navigate to the `src` directory.
2. Run the test script:

   ```bash
   python3 testscript.py '<output_from_run.sh>'
   ```

   - The script will validate the functionality of the deployed nodes.

### Testing with Specific Node Configurations
You can also test the system with a specific node configuration, including varying node sizes and finger table sizes. For example:

   ```bash
   python3 throughput-tester.py '[[8,0], [8,2], [8,4]]'
   ```

   - This command tests the system with 8 nodes and finger table sizes of 0, 2, and 4.

### Clean-up

After completing the tasks, **clean up** the cluster by running the following command:
Note, you do not need to fo this if you only used the throughput-tester since it does it for you. 

   ```bash
   /share/ifi/cleanup.sh
   ```

