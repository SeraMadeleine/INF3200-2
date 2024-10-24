import matplotlib.pyplot as plt
import numpy as np

def save_plot(plt, filename):
    plt.savefig(f'plot/{filename}', dpi=300, bbox_inches='tight', format='pdf')

# Data for nodes without finger table
no_finger_results = [
    {'nodes': 2, 'join_avg': 6.905078887939453e-06, 'join_std': 1.5757200154368955e-05, 'leave_avg': 1.0633468627929688e-07, 'leave_std': 1.4640609194193026e-07}, 
    {'nodes': 4, 'join_avg': 1.1176586151123047e-05, 'join_std': 2.009362533765602e-06, 'leave_avg': 8.448219299316406e-05, 'leave_std': 4.351499385807828e-06}, 
    {'nodes': 8, 'join_avg': 2.135610580444336e-05, 'join_std': 2.256257743576741e-06, 'leave_avg': 4.135346412658692e-05, 'leave_std': 2.5764147410684835e-06}, 
    {'nodes': 16, 'join_avg': 4.192113876342774e-05, 'join_std': 2.981253448997794e-06, 'leave_avg': 2.0782947540283204e-05, 'leave_std': 1.7767399783808714e-06}, 
    {'nodes': 32, 'join_avg': 8.383727073669434e-05, 'join_std': 3.822948643801801e-06, 'leave_avg': 1.0535478591918945e-05, 'leave_std': 1.1618418683286766e-06}
]

# Extract data for plotting
nodes = [entry['nodes'] for entry in no_finger_results]
join_times = [entry['join_avg'] for entry in no_finger_results]
join_stds = [entry['join_std'] for entry in no_finger_results]
leave_times = [entry['leave_avg'] for entry in no_finger_results]
leave_stds = [entry['leave_std'] for entry in no_finger_results]

# Plot PUT and GET times for different node counts
plt.figure(figsize=(10, 6))
plt.errorbar(nodes, join_times, yerr=join_stds, marker='o', color='orange', label='Join', capsize=5)
plt.errorbar(nodes, leave_times, yerr=leave_stds, marker='o', color='blue', label='Leave', capsize=5)
plt.title('Join and Leave Times for Different Node Counts (Finger-table size 0)')
plt.xlabel('Number of nodes in network')
plt.ylabel('Time (seconds)')
plt.xscale('log', base=2)
plt.xticks(nodes, labels=nodes)
plt.grid(True)
plt.legend()

save_plot(plt, 'leave_and_join_without_fingertable.pdf')
