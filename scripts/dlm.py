"""This script is used to generate dependency trees which are optimal in terms of Dependency Length Minimization"""

import random

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
	kids = tree[root].get("kids")
	linearization.append(root)

	# do it as long as some nodes are missing from the linearization
	while len(linearization) < len(tree):

		kids = [(k, weights[k]) for k in kids]

		# sort kids by order of decreasing weight
		kids = sorted([(x,y) for (x,y) in kids], key=lambda x:x[1])

		# nodes that will be linearized in the next iteration
		new_kids = list()

		# we don't want the first kid to always be on the same side
		first_direction = random.choice(["Left", "Right"])

		for i, (k, _) in enumerate(kids):
			new_kids.extend([x for x in tree[k].get("kids")])

			# find governor of the current node k
			idgov, rel = tree.idgovRel(k)

			# find where this govenor is in the linearization
			idgov_index = linearization.index(idgov)
			# print("gov is ", idgov, " with index in linearization ", idgov_index, "linearisation is ", linearization, " first direct is ", first_direction)


			if first_direction == "Right":
				
				if i % 2 == 0:
					kid_index = idgov_index+1 # i is pair : place it on the right
				else:
					kid_index = idgov_index-1 # i is not pair : place it on the left
					if kid_index < 0: # exception : if governor index is 0, kid_index will be at index 0, never -1
						kid_index = 0
			else:
				if i % 2 == 0:
					kid_index = idgov_index-1 # i is pair : place it on the left
					if kid_index < 0:
						kid_index = 0 # exception : if governor index is 0, kid_index will be at index 0, never -1
				else:
					kid_index = idgov_index+1 # i is not pair : place it on the right

			linearization.insert(kid_index, k)
		
		kids = new_kids # kids have been linearized, we move on to the grandkids

	return linearization




if __name__ == "__main__":
	conll = """1	le	le	_	_	_	3	det	_	_
2	petit	petit	_	_	_	3	amod	_	_
3	chat	chat	_	_	_	4	subj	_	_
4	dort	dort	_	_	_	0	root	_	_
5	très	très	_	_	_	6	advmod	_	_
6	bien	bien	_	_	_	4	advmod	_	_
"""
	# store the dependency tree in a dict
	tree = conll3.conll2tree(conll)

	# find the optimal sequence of nodes
	linearization = optimal_linearization(tree)
	print(linearization)

	# rewrite the conll according to the new linearisation
	new_tree = random_linearisation.rewrite_tree(tree, linearization)
	print(new_tree.conllu())
	# write the tree(s) to a file
	conll3.trees2conllFile([new_tree], "sample-dlmtree.conllu")