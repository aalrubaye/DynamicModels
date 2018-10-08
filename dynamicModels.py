__author__ = 'Abdul Rubaye'
from igraph import *
import numpy as np
import matplotlib.pyplot as plt
import powerlaw as pl

# Notes:
# graph: the instance of the generated graph
# nodes: a list of all the existing nodes in graph
# nodes_index: pointing to the index of next node to be injected
# steps_counter: a counter for the taken steps (Birth & Death processes)
# limit: the total number of steps will be taken place
# pq: a list that will be used to define the P and Q probabilities. used in equations 1 and 2
# p: a list of all p used
# t_steps: a list of the steps we take. Used in plotting the final figures
# n_counts: a list of the node counts. Used in plotting the final figures

graph = Graph()
nodes = []
nodes_index = 0
steps_counter = 0
limit = 5000
pq = []
p = [0.6, 0.75, 0.9]
t_steps = []
n_counts = []
m_counts = []
fig_m = []
degrees_p9 = []


# initializes a graph with a given probability p
def initialize_graph(prob):
    global pq, fig_m, degrees_p9

    pq = [prob, 1-prob]

    # started with creating two nodes to prevent a self edge
    add_node(0)
    add_node(1)

    graph.add_edge(str(0), str(1))

    for i in range(0, limit):
        next_process()

    fig_t = t_steps
    fig_n = n_counts
    fig_m = m_counts

    if prob == 0.9:
        degrees_p9 = graph.degree()

    reset_graph()
    return fig_t, fig_n, fig_m


# reset the graph and other related parameters
def reset_graph():
    global nodes_index, steps_counter, nodes, n_counts, t_steps, m_counts
    graph.delete_vertices(graph.vs)
    nodes_index = 0
    steps_counter = 0
    nodes = []
    n_counts = []
    m_counts = []
    t_steps = []


# The implementation of birth process
def birth_process():
    # creating a list of nodes probability for process_type = 1 (birth)
    add_prob_list = nodes_probs(1)

    # creating a new node
    new_node_index = nodes_index
    add_node(new_node_index)

    # finding the preferential node that will be connected to the new node
    preferential_node = weighted_random_node(add_prob_list)

    # add the new edge
    graph.add_edge(str(new_node_index), str(nodes[preferential_node]))


# The implementation of death process
def death_process():
    if graph.vcount() > 0:
        # creating a list of nodes probability for process_type = 2 (death)
        deletion_prob_list = nodes_probs(2)

        # finding the preferential node that will be removed from the graph
        preferential_node = weighted_random_node(deletion_prob_list)
        remove_node(preferential_node)

    else:
        print ('the network is vanished')


# procedure to add a node to the graph and to the index array
def add_node(index):
    global steps_counter, nodes_index

    graph.add_vertex(name=str(index))
    nodes.append(index)
    steps_counter += 1
    nodes_index += 1
    t_steps.append(steps_counter)
    n_counts.append(graph.vcount())
    m_counts.append(graph.ecount())

    print 'step =', steps_counter,' --> Birth '


# procedure to remove a node from the graph and from the index array
def remove_node(index):
    global steps_counter, nodes_index

    graph.delete_vertices(index)
    nodes.remove(nodes[index])
    steps_counter += 1
    t_steps.append(steps_counter)
    n_counts.append(graph.vcount())
    m_counts.append(graph.ecount())

    print 'step =', steps_counter,' --> Death '


# Figuring out the next process to take
def next_process():
    if weighted_random_node(pq) == 0:
        birth_process()
    else:
        death_process()


# calculating the probability of all nodes (process_type = 1 is birth process & process_type = 2 death process)
def equations(node_degree, process_type):
    if process_type == 1:
        return float(node_degree) / float((graph.ecount()*2))
    else:
        numerator = graph.vcount() - node_degree
        if numerator < 1:
            numerator = 1
        return float(numerator) / float(graph.vcount()**2 - graph.ecount()*2)


# creating a list of nodes' probabilities
def nodes_probs(process_type):
    prob_list = []

    for i in range(0, graph.vcount()):
        node_degree = graph.degree(i)
        if (node_degree == 0) and (process_type == 1):
            prob = 0
        else:
            prob = equations(node_degree, process_type)
        prob_list.append(prob)

    return prob_list


# This function picks a random index from the list of the nodes based on their preferential probability
def weighted_random_node(add_prob_list):
    if graph.ecount() == 0:
        rand = 0
    else:
        rand = np.random.choice(len(add_prob_list), 1, p=add_prob_list)[0]
    return rand


# calculated the expected nodes count
def expected_nodes(prob, steps):
    en = []
    for i in range(0, steps):
        en.append(((prob-(1-prob))*i)+(2*(1-prob)))
    return en


# calculated the expected edges count
def expected_edges(prob, steps):
    em = []
    for i in range(0, steps):
        em.append((prob*(prob-(1-prob)))*i)
    return em


# Prepares the data to be plotted as scatter
def create_scatter(list, rng):
    s = 0
    k = 0
    ind = rng/2
    new = []
    step_line = []
    for i in range (0, len(list)):
        s += list[i]
        k += 1
        if k == rng:
            step_line.append(ind)
            new.append(float(s/rng))
            k = 0
            s = 0
            ind += rng

    return step_line, new


# calls all other functions to calculate and prepare data for plotting
def create_fig_n_count(prob):
    steps, number_of_nods, number_of_edges = initialize_graph(prob)
    en = expected_nodes(prob, len(steps))
    em = expected_edges(prob, len(steps))
    scatter_steps, scatter_number_of_nodes = create_scatter(number_of_nods, space_between_ticks)
    scatter_steps, scatter_number_of_edges = create_scatter(number_of_edges, space_between_ticks)
    if prob == p[0]:
        mrkr = 'D'
        lbl = 'P='+str(prob)
    if prob == p[1]:
        mrkr = 's'
        lbl = 'P='+str(prob)
    if prob == p[2]:
        mrkr = '^'
        lbl = 'P='+str(prob)

    plt.plot(scatter_steps, scatter_number_of_nodes, mrkr, markersize=10, mfc='none', label=lbl)
    plt.plot(steps, en, '-')

    return [scatter_steps, scatter_number_of_edges, steps, em]


def create_fig_m_count(prob, params):
    if prob == p[0]:
        mrkr = 'D'
        lbl = 'P='+str(prob)
    if prob == p[1]:
        mrkr = 's'
        lbl = 'P='+str(prob)
    if prob == p[2]:
        mrkr = '^'
        lbl = 'P='+str(prob)

    plt.plot(params[0], params[1], mrkr, markersize=10, mfc='none', label=lbl)
    plt.plot(params[2], params[3], '-')


# The main function
if __name__ == "__main__":
    space_between_ticks = limit/10
    plt.figure(figsize=(16,10))

    plt.xticks(np.arange(0, limit, step=space_between_ticks))
    plt.subplots_adjust(wspace=0.4, hspace=0.3)

    # plotting Figure 2 in the paper
    plt.subplot(2, 2, 1)
    plt.xlabel('t', fontsize=18)
    plt.ylabel('E[n_t]', fontsize=16, rotation=0, labelpad=30)
    plt.title('Growth in # of nodes')

    fig_m_params_1 = create_fig_n_count(p[0])
    fig_m_params_2 = create_fig_n_count(p[1])
    fig_m_params_3 = create_fig_n_count(p[2])

    # gets the degrees of the graph and returns the cumulative DD
    srtd = np.sort(degrees_p9)[::-1]
    srtd_u = np.unique(srtd)
    s_srted_u = np.sort(srtd_u)[::-1]
    index_array = []
    count_array = []
    index_array.append(s_srted_u[0])
    for i in range (s_srted_u[0]-1,-1,-1):
        index_array.append(i)
    for i in range(0, len(index_array)):
        cn = np.count_nonzero(srtd == index_array[i])
        count_array.append(cn)
    counts = 0
    final_data_to_plot = []
    for i in range (0, len(index_array)):
        counts += count_array[i]
        for k in range(0, counts):
            final_data_to_plot.append(index_array[i])

    plt.legend(loc='upper left', numpoints=1)
    # plotting figure 3 in the paper
    plt.subplot(2, 2, 2)
    plt.xlabel('t', fontsize=18)
    plt.ylabel('E[m_t]', fontsize=16, rotation=0, labelpad=30)
    plt.title('Growth in # of edges')

    create_fig_m_count(p[0], fig_m_params_1)
    create_fig_m_count(p[1], fig_m_params_2)
    create_fig_m_count(p[2], fig_m_params_3)

    plt.legend(loc='upper left', numpoints=1)

    fit = pl.Fit(degrees_p9)
    label = r'$\alpha = %.2f\pm%.3f$'%(fit.power_law.alpha,2*fit.power_law.sigma)
    plt.subplot(2, 2, 3)
    plt.xlabel('k', fontsize=18)
    plt.ylabel('P[k]', fontsize=16, rotation=0, labelpad=30)
    plt.title('Cumulative Degree distribution (P = 0.9)')
    fit = pl.Fit(final_data_to_plot)
    fit.plot_pdf(marker='s',linestyle='none', color='black', mfc='none', markersize=12)
    fit.power_law.plot_pdf(label=label,lw=1.4, color='black')
    plt.legend(loc='upper right', fontsize= 16)
    plt.tick_params(axis='both', which='minor', labelsize=16)

    plt.show()
