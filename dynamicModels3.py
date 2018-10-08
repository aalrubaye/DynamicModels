__author__ = 'Abdul Rubaye'
from igraph import *
import numpy as np
import matplotlib.pyplot as plt

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
limit = 10
pq = []
p = [0.6, 0.75, 0.9]
t_steps = []
n_counts = []


# initializes a graph with a given probability p
def initialize_graph(p):
    global pq

    pq = [p, 1-p]

    # started with creating two nodes to prevent a self edge
    add_node(0)
    add_node(1)

    graph.add_edge(str(0), str(1))

    for i in range(0, limit):
        next_process()

    reset_graph()


# reset the graph and other related parameters
def reset_graph():
    global nodes_index, steps_counter, nodes, n_counts
    graph.delete_vertices(graph.vs)
    nodes_index = 0
    steps_counter = 0
    nodes = []
    n_counts = []


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

    # # print steps_t
    # print steps_counter


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

    print ('step = ', steps_counter,'-> # nodes ', graph.vcount())


# procedure to remove a node from the graph and from the index array
def remove_node(index):
    global steps_counter, nodes_index

    graph.delete_vertices(index)
    nodes.remove(nodes[index])
    steps_counter += 1
    t_steps.append(steps_counter)
    n_counts.append(graph.vcount())

    print ('step = ', steps_counter,'-> # nodes ', graph.vcount())


# Figuring out the next process to take
def next_process():
    # pq = [p[2], 1-p[2]]
    if weighted_random_node(pq) == 0:
        print ('next process => birth')
        birth_process()
    else:
        print ('next process => death')
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


# The main function
if __name__ == "__main__":

    initialize_graph(p[0])
    print ('*'*40)
    initialize_graph(p[1])
    print ('*'*40)
    initialize_graph(p[2])
    # plt.plot([1,2,3,4], [1,4,9,16], 'ro')
    # plt.axis([0, 6, 0, 20])
    # plt.show()


