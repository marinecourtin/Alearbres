"""This script is used to generate dependency trees which are optimal in terms of Dependency Length Minimization"""

import random
import copy

# local scripts
import conll3
import random_linearisation

def get_weight_kids(tree, node, weights):
	"""
	Computes the weight (i.e the number of direct and indirect dependents) for each node.
	
	Recursive function called inside optimal_linearization.

	Parameters
	----------
	tree : Tree
		a dependency Tree in dict format
	node : dict
		the dict corresponding to the current root node
	weights : dict
		the dict updated with each node's weight

	Returns
	-------
	weights : dict
		the dict updated with each node's weight
	"""
	kids = node.get("kids").keys()
	weights[node["id"]] = 0
	if not kids:
		return weights
	for k in kids:
		weights[node["id"]] +=1
		weights = get_weight_kids(tree, tree[k], weights)
		weights[node["id"]] += weights[k]
	return weights
	

def optimal_linearization(tree):
	"""
	Reorders the nodes to minimize Dependency Length.

	The resulting relinearized tree will be one of the possible trees
	that minimize dependency length without altering the structure.
	
	Parameters
	----------
	tree : Tree
		the original dependency Tree in dict format

	Returns
	-------
	linearization : list
		the new sequence of nodes that minimizes Dependency Length
	"""
	tree.addkids()
	root = tree.get_root()

	# creates a dictionary that indicates how many descendents every node has
	weights = get_weight_kids(tree, tree[root], dict())

	# start the linearization
	linearization = list()
	kidz = [[root,sorted([x for x in tree[root].get("kids")], key=lambda x:weights[x], reverse=True)]]
	print(kidz)
	linearization.append(root)
	first_direction = 0
	count = 0
	new_kids = []

	# # do it as long as some nodes are missing from the linearization
	while len(linearization) < len(tree):
		for idgov, kids in kidz:
			nb_kids = len(kids)

			if count > 0:
				# finding head_direction
				grand_idgov, _ = tree.idgovRel(idgov)
				grand_idgov_index = linearization.index(grand_idgov)
				idgov_index = linearization.index(idgov)

				if idgov_index - grand_idgov_index > 0:
					head_direction = 1
				else:
					head_direction = 0
			else:
				head_direction = first_direction

			for i, k in enumerate(kids):
				idgov_index = linearization.index(idgov)
				if tree[k].get("kids"):

					new_kids += [[k, sorted([x for x in tree[k].get("kids")], key=lambda x:weights[x], reverse=True)]]
				
				# pair kid will always go in the direction of its governor
				if i % 2 == 0:
					first_direction = head_direction
					linearization.insert(idgov_index+first_direction, k)

				# odd kid, inverse direction compare to head direction
				else:
					if head_direction == 1:
						linearization.insert(idgov_index, k)

					else:
						linearization.insert(idgov_index+1, k)

		kidz = new_kids
		count += 1

	return linearization



if __name__ == "__main__":
# 	conll = """1	le	le	_	_	_	3	det	_	_
# 2	petit	petit	_	_	_	3	amod	_	_
# 3	chat	chat	_	_	_	4	subj	_	_
# 4	dort	dort	_	_	_	0	root	_	_
# 5	très	très	_	_	_	6	advmod	_	_
# 6	bien	bien	_	_	_	4	advmod	_	_
# 7	bien	bien	_	_	_	4	advmod	_	_
# 8	bien	bien	_	_	_	3	advmod	_	_
# """

	conll = """1	le	le	_	_	_	0	root	_	_
2	petit	petit	_	_	_	1	amod	_	_
3	chat	chat	_	_	_	4	subj	_	_
4	dort	dort	_	_	_	2	root	_	_
5	très	très	_	_	_	4	advmod	_	_
6	bien	bien	_	_	_	4	advmod	_	_
7	bien	bien	_	_	_	5	advmod	_	_
"""
	# store the dependency tree in a dict
	# tree = conll3.conll2tree(conll)

	# # # find the optimal sequence of nodes
	# linearization = optimal_linearization(tree)
	# # print(linearization)

	# # rewrite the conll according to the new linearisation
	# new_tree = random_linearisation.rewrite_tree(tree, linearization)
	# # print(new_tree.conllu())
	# # write the tree(s) to a file
	# conll3.trees2conllFile([new_tree], "sample-dlmtree.conllu")

	new_trees = list()
	trees = conll3.conllFile2trees("sample_random-forest.conllu")
	for t in trees:
		l = optimal_linearization(t)
		n_t = random_linearisation.rewrite_tree(t, l)
		new_trees += [n_t]
	conll3.trees2conllFile(new_trees, "../sample_optimal-forest.conllu")