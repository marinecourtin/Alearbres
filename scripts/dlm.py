""" script for producing optimal linearisations in terms of dependency length minimisation"""

import conll3
import randomtrees

def get_weight_kids(tree, node, weights):
	"""
	called inside optimal_linearization(), recursive

	@args:
	- Tree()
	- node (root node for the first call)
	- dict() (empty for initialization)

	recursive function, returns a dictionary with the weights (number of descendants, direct and indirect) of each node
	"""
	kids = node.get("kids").keys()
	if kids:
		weights[node["id"]] = 0
		for k in kids:
			weights[node["id"]] +=1
			weights = get_weight_kids(tree, tree[k], weights)
			# print(node["id"], "current child", k, "weight of child", weights[k], "new node weight", weights[node["id"]]+weights[k])
			weights[node["id"]] += weights[k]
	else:
		weights[node["id"]] = 0
		return weights
	return weights


def optimal_linearization(tree):
	"""
	@args:
	- Tree()

	Returns one of the optimal linearization in terms of dependency length minimization (DLM)
	"""
	tree.addkids(tree)
	root = tree.get_root()

	# creates a dictionary that indicates how many descendents every node has
	weights = get_weight_kids(tree, tree[root], dict())

	# start linearization
	linearization = list()
	kids = tree[root].get("kids")
	linearization.append(root)

	# do it as long as some nodes are not part of the linearization
	while len(linearization) < len(tree):

		kids = [(k, weights[k]) for k in kids]

		# sort kids by order of dicreasing weight
		kids = sorted([(x,y) for (x,y) in kids], key=lambda x:x[1])

		# nodes that will be linearized in the next iteration
		new_kids = list()

		for i, (k, _) in enumerate(kids):
			# print("looking at kid ", k)
			new_kids.extend([x for x in tree[k].get("kids")])
			# print("future kids :", new_kids)

			# find governor of the current node k
			idgov, rel = tree.idgovRel(k)

			# find where this govenor is in the linearization
			idgov_index = linearization.index(idgov)
			# print("gov is ", idgov, " with index in linearization ", idgov_index, "linearisation is ", linearization)

			# we place kids alternately on the left or right of their govenor


			# TODO : add parameter to select the first direction (left or right)
			# i is pair : place it on the right
			if i % 2 == 0:
				kid_index = idgov_index+1

			# i is not pair : place it on the left
			else:
				kid_index = idgov_index-1

				# exception : if governor index is 0, kid_index will be at index 0
				if kid_index < 0:
					kid_index = 0

			# print("kid will go at index ", kid_index, " in linearization")
			linearization.insert(kid_index, k)
			# print("new linearisation ", linearization)
		
		# kids have been linearized, we move on to the kids of the kids
		kids = new_kids

	return linearization




if __name__ == "__main__":
	conll = """1	le	le	_	_	_	3	det	_	_
2	petit	petit	_	_	_	3	amod	_	_
3	chat	chat	_	_	_	4	subj	_	_
4	dort	dort	_	_	_	0	root	_	_
5	très	très	_	_	_	6	advmod	_	_
6	bien	bien	_	_	_	4	advmod	_	_
"""
	tree = conll3.conll2tree(conll)
	linearization = optimal_linearization(tree)
	new_tree = randomtrees.rewrite_tree(tree, linearization)
	print(new_tree)