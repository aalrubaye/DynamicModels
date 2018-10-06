__author__ = 'Abdul Rubaye'
import networkx as nx
import numpy as np


class RunModel:

    # create a network instance
    graph = nx.Graph()
    nodes_count = 0
    ii = 0
    pq = [0.8, 0.2]

    # initializing the graph with a node that has an edge to itself
    def __init__(self):
        self.graph.add_node(0)
        self.graph.add_edge(0, 0)

        self.nodes_count = self.graph.number_of_nodes()

        # let's assume starting with a birth process if there is only one node in the graph
        self.birth_process()

    # The implementation of birth process
    def birth_process(self):
        # creating a list of nodes probability for process_type = 1 (birth)
        add_prob_list = self.nodes_probs(1)

        # creating a new node
        new_node_index = self.nodes_count
        self.nodes_count += 1
        self.graph.add_node(new_node_index)

        # finding the preferential node that will be connected to the new node
        preferential_node = self.weighted_random_node(add_prob_list)
        # add the new edge
        self.graph.add_edge(new_node_index, preferential_node)

        print self.graph.nodes
        print self.graph.edges

        self.ii += 1

        # rr = self.weighted_random_node(self.pq)

        if self.ii < 10:
            self.birth_process()

    # The implementation of death process
    def death_process(self):
        # creating a list of nodes probability for process_type = 2 (death)
        deletion_prob_list = self.nodes_probs(2)
        print deletion_prob_list

        # finding the preferential node that will be removed from the graph
        preferential_node = self.weighted_random_node(deletion_prob_list)

        print preferential_node
        self.graph.remove_node(preferential_node)
        self.nodes_count -= 1
        print self.graph.nodes
        print self.graph.edges

    # calculating the probability of all nodes (process_type = 1 is birth process & process_type = 2 death process)
    def equations(self, node_degree, process_type):
        if process_type == 1:
            return float(node_degree) / float((self.graph.number_of_edges()*2))
        else:
            return float(self.graph.number_of_nodes() - node_degree) / float(self.graph.number_of_nodes()**2 - self.graph.number_of_edges()*2)

    # creating a list of nodes' probabilities
    def nodes_probs(self, process_type):
        prob_list = []

        for i in range(0, self.graph.number_of_nodes()):
            node_degree = self.graph.degree[i]
            prob = self.equations(node_degree, process_type)
            prob_list.append(prob)

        return prob_list

    # This function picks a random index from the list of the nodes based on their preferential probability
    def weighted_random_node(self, add_prob_list):
        rand = np.random.choice(len(add_prob_list), 1, p=add_prob_list)[0]
        return rand


# The main function
if __name__ == "__main__":
    RunModel()
