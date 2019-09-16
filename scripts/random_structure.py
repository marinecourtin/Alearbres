""" This script is used to create random dependency structures"""

import random

# visualisation
import matplotlib.pyplot as plt
import networkx as nx

# local
import conll3


class DependencyTree(object):
	"""
	A class used to build dependency trees

	Attributes
	----------
	size : int
		number of nodes in the tree
	nodes : list
		a list of the tree's nodes
	edges : list
		a list of the tree's edges
	root : int
		the root of the dependency tree
	floating_nodes : list
		a list of all the nodes that have no edges linking them to other nodes
	potential_governors : list
		a list of nodes that are part of the tree and can act as governors for floating_nodes
	
	Methods
	----------
	add_edge()
		randomly add an edge to the dependency tree
	parse()
		creates a complete random parse for the dependency tree
	view()
		visualize the tree using networkx
	toTree()
		produces a dict version of the Dependency Tree that can be used by the conll3 library
	"""

	def __init__(self, size, root=0):
		"""
		Parameters
		----------
		size : int
			number of nodes in the tree
		root : int
			the root of the dependency tree (default is 0)
		"""
		self.size = size
		self.nodes = [x for x in range(size)]
		self.edges = []
		self.root = root
		self.floating_nodes = [n for n in self.nodes if n!=self.root]
		self.potential_governors = [self.root]
		self.parse()

	def add_edge(self):
		"""
		Randomly add an edge to the dependency tree

		Updates the edges attribute by linking one of the floating nodes
		to one of the potential governors.

		Parameters
		----------
		self: DependencyTree
			the current dependency tree with its nodes, edges...

		Updates
		----------
		edges : list
			adds a new edge
		floating_nodes : list
			removes the last attached node
		potential_governors : list
			adds the last attached node to the list
		"""
		dep= self.floating_nodes[0]
		gov = random.choice(self.potential_governors)
		edge = (dep, gov)
		self.edges.append(edge)
		self.potential_governors.append(dep)
		self.floating_nodes = self.floating_nodes[1:]

	def parse(self):
		"""
		Creates a complete random parse for the dependency tree

		Parameters
		----------
		self: DependencyTree
			the current dependency tree with its nodes, edges...

		Updates
		----------
		edges : list
			adds a new edge
		floating_nodes : list
			removes the last attached node
		potential_governors : list
			adds the last attached node to the list
		"""
		self.tree = dict()
		while self.floating_nodes:
			self.add_edge()
		for (node, gov) in self.edges:
			if gov in self.tree:
				self.tree[gov] += [node]
			else:
				self.tree[gov] = [node]
			if node not in self.tree:
				self.tree[node] = []
			else:
				continue

	def view(self):
		"""
		Visualize the Dependency Tree with networkx

		Parameters
		----------
		self: DependencyTree
			the current dependency tree with its nodes, edges...

		"""
		G = nx.Graph()
		G.add_nodes_from(self.nodes)
		G.add_edges_from(self.edges)
		nx.draw(G, font_weight="bold", with_labels=True)
		plt.show()

	def toTree(self):
		"""
		Produces a dict version of the Dependency Tree that can be used by the conll3 library

		Parameters
		----------
		self: DependencyTree
			the current dependency tree with its nodes, edges...

		Returns
		----------
		c_tree : Tree
			dictionary version of the Dependency Tree, can be used by conll3.
			This tree only contains information about the dependency relations between the nodes.
			- each token is named __n__ where n is the integer symbolizing the node
			- the tree by default has no UPOS or XPOS
			- the relations are either root or unk (for unknown)
		"""
		tree = dict()
		tree[self.root+1] = {"id":self.root+1,"gov":{0:"root"}, "t":"__"+str(self.root+1)+"__"}
		for (dep, gov) in self.edges:
			tree[dep+1] = {"id":dep+1,"gov":{gov+1:"unk"}, "t":"__"+str(dep+1)+"__"}
		c_tree = conll3.Tree(tree)
		return c_tree



if __name__ == "__main__":

	## small example
	# create a random tree with 5 nodes
	t = DependencyTree(5, root=1)
	# visualize it
	t.view()
	# transform it to conll3 format
	tree = t.toTree()
	# write it to a file
	conll3.trees2conllFile([tree], "sample_random-trees.conllu")