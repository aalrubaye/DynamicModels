__author__ = 'Abdul Rubaye'
from igraph import *
import numpy as np

graph = Graph()
nodes = []
nodes_count = 0
ii = 0
pq = [0.5, 0.5]
steps_t = 0
limit = 10000

# The implementation of birth process
def birth_process():

    global steps_t,nodes_count

    # creating a list of nodes probability for process_type = 1 (birth)
    add_prob_list = nodes_probs(1)

    # creating a new node
    new_node_index = nodes_count
    nodes_count += 1
    add_node(new_node_index)

    steps_t += 1

    # finding the preferential node that will be connected to the new node
    preferential_node = weighted_random_node(add_prob_list)

    # add the new edge
    graph.add_edge(str(new_node_index), str(nodes[preferential_node]))

    # print preferential_node
    # print graph.vs['name']
    # print nodes
    # print graph.get_edgelist()
    # print ('*'*20)

    # print steps_t
    print (str(steps_t),'->',str(graph.vcount()))


# The implementation of death process
def death_process():
    global steps_t
    if graph.vcount() > 0:
        # creating a list of nodes probability for process_type = 2 (death)
        deletion_prob_list = nodes_probs(2)

        # finding the preferential node that will be removed from the graph
        preferential_node = weighted_random_node(deletion_prob_list)
        remove_node(preferential_node)
        #
        # print preferential_node
        # print graph.vs['name']
        # print nodes
        # print graph.get_edgelist()
        # print ('*'*20)

        steps_t += 1

        print (str(steps_t),'->',str(graph.vcount()))

    else:
        print ('the network is vanished')


# procedure to add a node to the graph and to the index array
def add_node(index):
    graph.add_vertex(name=str(index))
    # self.graph.add_node(index)
    nodes.append(index)


# procedure to remove a node from the graph and from the index array
def remove_node(index):
    # self.graph.delete_vertices(self.nodes[index])
    graph.delete_vertices(index)
    nodes.remove(nodes[index])


# Figuring out the next process to take
def next_process():
    if weighted_random_node(pq) == 0:
        # print ('next process => birth')
        birth_process()
    else:
        # print ('next process => death')
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
    # started with creating two nodes to prevent a self edge
    add_node(0)
    add_node(1)

    graph.add_edge(str(0), str(1))
    nodes_count = graph.vcount()
    #
    # print graph.vs['name']
    # print nodes
    # print graph.get_edgelist()
    # print ('*'*20)

    steps_t += 1
    print steps_t

    for i in range (0, limit):
        next_process()

