__author__ = 'Abdul Rubaye'
import networkx as nx
import numpy as np


class RunModel:

    # create a network instance
    graph = nx.Graph()
    nodes_count = 0

    ii = 0

    # initializing the graph with a node that has an edge to itself
    def __init__(self):
        self.graph.add_node(0)
        self.graph.add_edge(0, 0)
        self.nodes_count = self.graph.number_of_nodes()
        self.birth_process()

    # The implementation of birth process
    def birth_process(self):
        add_prob_list = []

        # calculating the probability of all nodes
        for i in range(0, self.graph.number_of_nodes()):
            node_degree = self.graph.degree[i]
            node = self.graph.nodes[i]

            # the implementation of equation 1
            prob = float(node_degree) / float((self.graph.number_of_edges()*2))
            # creating a list of all nodes' addition probabilities
            add_prob_list.append(prob)

            print node_degree
            print add_prob_list[i]

        print ('*'*10)

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

        self.ii +=1

        if self.ii < 10 :
            self.birth_process()

    # This function picks a random index from the list of the nodes based on their preferential probability
    def weighted_random_node(self, add_prob_list):
        rand = np.random.choice(len(add_prob_list), 1, p=add_prob_list)[0]
        return rand

    # The implementation of death process
    def death_process(self):
        death = True


# The main function
if __name__ == "__main__":
    RunModel()
