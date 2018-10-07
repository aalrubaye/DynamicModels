import sys

__author__ = 'Abdul Rubaye'
import networkx as nx
import numpy as np


class RunModel:

    # create a network instance
    graph = nx.Graph()
    nodes = []
    nodes_count = 0
    ii = 0
    pq = [0.8, 0.2]

    steps_t = 0
    limit = 1000

    # initializer
    def __init__(self):
        # started with creating two nodes to prevent a self edge
        self.add_node(0)
        self.add_node(1)
        self.graph.add_edge(0, 1)

        self.nodes_count = self.graph.number_of_nodes()
        # print ('node count = '+ str(self.nodes_count))

        # let's assume starting with a birth process if there is only one node in the graph
        # self.birth_process()

        self.steps_t += 1

        # self.next_process()
        self.birth_process()

    # The implementation of birth process
    def birth_process(self):
        # creating a list of nodes probability for process_type = 1 (birth)
        add_prob_list = self.nodes_probs(1)

        # creating a new node
        new_node_index = self.nodes_count
        self.nodes_count += 1
        self.add_node(new_node_index)

        self.steps_t += 1

        # finding the preferential node that will be connected to the new node
        preferential_node = self.weighted_random_node(add_prob_list)

        # add the new edge
        self.graph.add_edge(new_node_index, self.nodes[preferential_node])

        # print preferential_node
        # print self.graph.nodes
        # print self.nodes
        # print self.graph.edges
        # print ('*'*20)

        if self.steps_t < self.limit:
            print self.steps_t
            # self.next_process()
            self.birth_process()

    # The implementation of death process
    def death_process(self):

        if self.graph.number_of_nodes() > 0:
            # creating a list of nodes probability for process_type = 2 (death)
            deletion_prob_list = self.nodes_probs(2)
            # print ('node count = '+ str(self.nodes_count))
            # finding the preferential node that will be removed from the graph
            preferential_node = self.weighted_random_node(deletion_prob_list)
            self.remove_node(preferential_node)
            # self.nodes_count -= 1
            # print ('node count = '+ str(self.nodes_count))
            #
            # print preferential_node
            # print self.graph.nodes
            # print self.graph.edges
            # print ('*'*20)

            if self.steps_t < self.limit:
                print self.steps_t
                self.next_process()

        else:
            print ('the network is vanished')

    # procedure to add a node to the graph and to the index array
    def add_node(self,index):
        self.graph.add_node(index)
        self.nodes.append(index)

    # procedure to remove a node from the graph and from the index array
    def remove_node(self,index):
        self.graph.remove_node(self.nodes[index])
        self.nodes.remove(self.nodes[index])

    # Figuring out the next process to take
    def next_process(self):
        if self.weighted_random_node(self.pq) == 0:
            # print ('next process => birth')
            self.birth_process()
        else:
            # print ('next process => death')
            self.death_process()

    # calculating the probability of all nodes (process_type = 1 is birth process & process_type = 2 death process)
    def equations(self, node_degree, process_type):
        if process_type == 1:
            return float(node_degree) / float((self.graph.number_of_edges()*2))
        else:
            numerator = self.graph.number_of_nodes() - node_degree
            if numerator < 1:
                numerator = 1
            return float(numerator) / float(self.graph.number_of_nodes()**2 - self.graph.number_of_edges()*2)

    # creating a list of nodes' probabilities
    def nodes_probs(self, process_type):
        prob_list = []

        for i in range(0, self.graph.number_of_nodes()):
            node_degree = self.graph.degree[self.nodes[i]]
            if (node_degree == 0) and (process_type == 1):
                prob = 0
            else:
                prob = self.equations(node_degree, process_type)
            prob_list.append(prob)

        return prob_list

    # This function picks a random index from the list of the nodes based on their preferential probability
    def weighted_random_node(self, add_prob_list):
        if self.graph.number_of_edges() == 0:
            rand = 0
        else:
            rand = np.random.choice(len(add_prob_list), 1, p=add_prob_list)[0]
        return rand


# The main function
if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    RunModel()
