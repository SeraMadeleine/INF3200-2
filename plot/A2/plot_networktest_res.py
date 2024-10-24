import matplotlib.pyplot as plt
import json
import numpy as np
import os

def save_plot(plt, filename):
    # Ensure the plot directory exists
    os.makedirs('plot', exist_ok=True)
    plt.savefig(f'{filename}', dpi=300, bbox_inches='tight', format='pdf')

def plot_results():
    # Load results from res.txt
    try:
        with open("../../python_tests/res.txt", "r") as f:
            data = f.read()
        no_finger_results = json.loads(data.split('= ')[1])
    except FileNotFoundError:
        print("Error: res.txt file not found. Please ensure the file exists in the current directory.")
        return

    # Extract data for plotting
    nodes = [entry['nodes'] for entry in no_finger_results]
    join_avg_values = [entry['join_avg'][0] for entry in no_finger_results]
    join_std_values = [entry['join_std'][0] for entry in no_finger_results]
    # Assuming 'put_avg' and 'put_std' keys exist for PUT operation data
    put_avg_values = [entry.get('put_avg', 0) for entry in no_finger_results]
    put_std_values = [entry.get('put_std', 0) for entry in no_finger_results]

    # Plotting GET and PUT times for different node counts (only 2, 4, 8 nodes)
    plt.figure(figsize=(10, 6))
    plt.errorbar(nodes, join_avg_values, yerr=join_std_values, marker='o', color='blue', label='GET', capsize=5)
    plt.errorbar(nodes, put_avg_values, yerr=put_std_values, marker='o', color='orange', label='PUT', capsize=5)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Time (s)')
    plt.title('PUT and GET Operation Times for Different Node Counts (Finger-table size 0)')
    plt.xscale('log', base=2)
    plt.xticks(nodes, labels=nodes)
    plt.grid(True)
    plt.legend()

    save_plot(plt, 'put_get_times_vs_nodes_without_finger_table.pdf')
    print("Plot saved as put_get_times_vs_nodes_without_finger_table.pdf")

if __name__ == "__main__":
    plot_results()
