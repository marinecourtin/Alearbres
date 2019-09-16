import random

# visualisation
import matplotlib.pyplot as plt
import networkx as nx

# local
import conll3

class DependencyTree(object):
	"""
	A dependency tree is made of:
	- list of nodes
	- list of edges
	"""

	def __init__(self, size, root=0):
		self.size = size
		self.nodes = [x for x in range(size)]
		self.edges = []
		self.root = root
		self.floating_nodes = [n for n in self.nodes if n!=self.root]
		self.potential_governors = [self.root]
		self.parse()

	def add_edge(self):
		"""
		Adds one edge to a tree's list of edges.

		@out:
		- self.edges

		@mod:
		- self.edges
		- self.floating_nodes
		- self.potential_governors
		"""
		dep= self.floating_nodes[0]
		gov = random.choice(self.potential_governors)
		edge = (dep, gov)
		self.edges.append(edge)
		self.potential_governors.append(dep)
		self.floating_nodes = self.floating_nodes[1:]

	def parse(self):
		"""
		Randomly creates a parse for the dependency tree

		@out:
		- self.tree
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
		Visualisation of the dependency graph.

		"""
		G = nx.Graph()
		G.add_nodes_from(self.nodes)
		G.add_edges_from(self.edges)
		nx.draw(G, font_weight="bold", with_labels=True)
		plt.show()

	def toTree(self):
		tree = dict()
		tree[self.root+1] = {"id":self.root+1,"gov":{0:"root"}, "t":"__"+str(self.root+1)+"__"}
		for (dep, gov) in self.edges:
			tree[dep+1] = {"id":dep+1,"gov":{gov+1:"unk"}, "t":"__"+str(dep+1)+"__"}
		return conll3.Tree(tree)



if __name__ == "__main__":
	trees = list()
	for i in range(6,13):
		t = DependencyTree(i)

		# si on veut visualiser
		# t.view()
		print("yay")

	# 	# au format de conll
	# 	tree = t.toTree()
	# 	trees.append(tree)
	# conll3.trees2conllFile(trees, "random-structured-trees.conllu")