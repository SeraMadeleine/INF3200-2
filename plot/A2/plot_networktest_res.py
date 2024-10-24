import matplotlib.pyplot as plt
import numpy as np

def save_plot(plt, filename):
    plt.savefig(f'plot/{filename}', dpi=300, bbox_inches='tight', format='pdf')

# Data for nodes without finger table
no_finger_results = [
    {'nodes': 2, 'join_avg': 0.00014313062032063803, 'join_std': 0.00019112391661976153, 'leave_avg': 2.384185791015625e-07, 'leave_std': 0.0}, 
    {'nodes': 4, 'join_avg': 2.4954477945963543e-05, 'join_std': 1.8441471175282772e-05, 'leave_avg': 0.00010752677917480469, 'leave_std': 3.3897387345522265e-05}, 
    {'nodes': 8, 'join_avg': 3.719329833984375e-05, 'join_std': 2.2086878925358704e-05, 'leave_avg': 5.18957773844401e-05, 'leave_std': 1.590609133049435e-05}, 
    {'nodes': 16, 'join_avg': 5.841255187988281e-05, 'join_std': 2.3433849914343552e-05, 'leave_avg': 2.566973368326823e-05, 'leave_std': 7.308046933856105e-06}, 
    {'nodes': 32, 'join_avg': 0.00010895729064941406, 'join_std': 3.184710622532463e-05, 'leave_avg': 1.3033548990885416e-05, 'leave_std': 3.311263188679959e-06}
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

# # Data for 16 nodes with different finger table sizes
# finger_results = [
#     {'finger': 0, 'join_avg': 9.727128823598227, 'join_std': 0.24937378864760984, 'leave_avg': 8.968641916910807, 'leave_std': 0.038643329111794224},
#     {'finger': 2, 'join_avg': 6.36955205599467, 'join_std': 0.06951057331176141, 'leave_avg': 5.978910128275554, 'leave_std': 0.10088526026373933},
#     {'finger': 4, 'join_avg': 4.421700795491536, 'join_std': 0.047840331763432345, 'leave_avg': 4.0844349066416425, 'leave_std': 0.025710102112591657},
#     {'finger': 6, 'join_avg': 4.369396527608235, 'join_std': 0.03211150621159705, 'leave_avg': 4.111806710561116, 'leave_std': 0.03154388183680087},
#     {'finger': 8, 'join_avg': 4.009881019592285, 'join_std': 0.0331916351896988, 'leave_avg': 3.7238598664601645, 'leave_std': 0.04343130067673035}
# ]

# # Extract data for plotting for 16 nodes
# finger_sizes = [entry['finger'] for entry in finger_results]
# join_times_16 = [entry['join_avg'] for entry in finger_results]
# join_stds_16 = [entry['join_std'] for entry in finger_results]
# leave_times_16 = [entry['leave_avg'] for entry in finger_results]
# leave_stds_16 = [entry['leave_std'] for entry in finger_results]

# # Plot PUT and GET times for 16 nodes with different finger table sizes
# plt.figure(figsize=(10, 6))
# plt.errorbar(finger_sizes, join_times_16, yerr=join_stds_16, marker='o', color='orange', label='PUT', capsize=5)
# plt.errorbar(finger_sizes, leave_times_16, yerr=leave_stds_16, marker='o', color='blue', label='GET', capsize=5)
# plt.title('PUT and GET Operation Times for 16 Nodes with Different Finger-table Sizes')
# plt.xlabel('Finger table size')
# plt.ylabel('Time (seconds)')
# plt.xticks(finger_sizes)
# plt.grid(True)
# plt.legend()

# save_plot(plt, 'put_leave_times_vs_finger_table_size_16_nodes.pdf')