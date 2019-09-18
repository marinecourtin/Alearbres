"""This script is used to create random projective linearisations for dependency trees"""


import random
import numpy as np
import copy

# local imports

import conll3
from conll3 import  Tree






def get_kids(tree, num):
	"""
	Gives the list of dependent nodes of a governor.

	Parameters
	----------
	tree : Tree
		a dependency Tree in dict format
	num : int
		the id of the governor nodes

	Returns
	-------
	kids : list
		a list of ids of the dependent nodes
	"""
	kids = list(tree[num]["kids"])
	return kids

def randomly_select_dependents(deps):
	"""
	Gives the order in which dependents will be processed

	Parameters
	----------
	deps: list
		a list of dependent nodes

	Updates
	----------
	deps : list
		a randomly ordered list of dependent nodes
	"""
	random.shuffle(deps)

def randomly_select_direction(tree, linearisation, node, gov_initial):
	"""
	Gives the directions in which dependent nodes will be linearised.

	True: left
	False: right

	Parameters
	----------
	tree: Tree
		a dependency Tree in dict format
	linearisation: list
		a list of nodes in the order of the current linearisation
	node: int
		the id of the node to linearize
	gov_initial: float
		the desired probability for governor-initial dependency links

	Returns
	-------
	linearisation: list
		a list of nodes in the order of the current linearisation, where
		the current node has been placed.

	Example
	----------
	deps = [2,0,1]
	node = 3 (kid of 2)
	the random components returns False
	linearisation = [2,3,0,1] -> 3 is placed on the right of its governor
	"""
	left = np.random.rand() > gov_initial # True:left / False:right

	gov = list(tree[node]["gov"])[0] # grab the governor of the current node
	gov_rank = linearisation.index(gov) # get its index in the linearisation

	# insert node in list next to its governor
	if left:
		linearisation.insert(gov_rank, node) # insert the node just before its governor
	else:
		linearisation.insert(gov_rank+1, node) # insert the node just after its governor

	return linearisation



def create_random_pj_linearisation(tree, gov_initial=0.5):
	""" 
	Creates a random projective linearisation (main function).

	Parameters
	----------
	tree: Tree
		a dependency Tree in dict format
	gov_initial : float
		the desired probability for governor-initial dependency links

	Returns
	-------
	randomly_linearised_tree : Tree
		a dependency Tree in dict format where the order of nodes
		has been randomized.
	"""
	tree_for_rewrite = copy.deepcopy(tree)
	tree.addkids(tree)
	num_root = tree.get_root() # grab the root
	linearisation = [num_root] # initialize the linearisation

	# produce a random projective linearisation
	reorder_kids(tree, num_root, linearisation, gov_initial)

	# reorder the nodes according to the linearisation
	randomly_linearised_tree = rewrite_tree(tree_for_rewrite, linearisation)
	return randomly_linearised_tree


def reorder_kids(tree,node, linearisation, gov_initial):
	"""
	Updates the linearisation of the tree by recursively placing children nodes
	around their governor node.

	The reordering is constrained to produce projective trees.

	Parameters
	----------
	tree: Tree
		a dependency Tree in dict format
	gov_initial : float
		the desired probability for governor-initial dependency links
	"""
	all_kids = get_kids(tree, node)
	if not all_kids: # node is a leaf
		pass
	else:
		# randomize the order of kids in all_kids
		randomly_select_dependents(all_kids)

		# apply the same procedure to all the subkids
		for kid in all_kids:
			randomly_select_direction(tree, linearisation, kid, gov_initial)
			reorder_kids(tree,kid, linearisation, gov_initial) # recursive call

def create_random_nonpj_linearisation(tree):
	"""
	Creates a random linearisation with no projectivity constraints.

	Parameters
	----------
	tree: Tree
		a dependency Tree in dict format

	Returns
	-------
	randomly_linearised_tree : Tree
		a dependency Tree in dict format where the order of nodes
		has been randomized.
	"""
	tree_for_rewrite = copy.deepcopy(tree)
	nodes = list(tree.keys())
	random.shuffle(nodes)
	random_tree = rewrite_tree(tree, nodes)
	return random_tree



def rewrite_tree(tree, li):
	"""
	Rewrites a Tree according to a new linearisation

	Parameters
	----------
	tree: Tree
		a dependency Tree in dict format
	li : list
		linearisation to reproduce

	Returns
	-------
	tree: Tree
		a dependency Tree in dict format, where nodes have been reordered
	"""
	new_tree = Tree()

	for i, node in tree.items():
		new_node = tree[li[i-1]] # grab the node from the original tree
		new_node["id"] = i # replace its old id by its position in the linearisation
		gi = list(new_node["gov"].keys())[0]

		if gi != 0: # this node is not the root
			new_gi = li.index(gi)+1 # update the governor id
			new_node["gov"] = {new_gi: new_node["gov"][gi]}
		new_tree[i] = new_node # add this node in the new tree

	return new_tree



if __name__ == "__main__":

	conll = """1	le	le	_	_	_	3	det	_	_
2	petit	petit	_	_	_	3	amod	_	_
3	chat	chat	_	_	_	4	subj	_	_
4	dort	dort	_	_	_	0	root	_	_
5	très	très	_	_	_	6	advmod	_	_
6	bien	bien	_	_	_	4	advmod	_	_
"""


	conll2 ="""# sent_id = annodis.er_00022
# text = Ouverture tous les jours sauf le lundi de 14h30 à 18h.
1	Ouverture	ouverture	NOUN	_	Gender=Fem|Number=Sing	0	root	_	_
2	tous	tout	ADJ	_	Gender=Masc|Number=Plur	4	amod	_	_
3	les	le	DET	_	Definite=Def|Number=Plur|PronType=Art	4	det	_	_
4	jours	jour	NOUN	_	Gender=Masc|Number=Plur	1	nmod	_	_
5	sauf	sauf	ADP	_	_	7	case	_	_
6	le	le	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	7	det	_	_
7	lundi	lundi	NOUN	_	Gender=Masc|Number=Sing	4	nmod	_	_
8	de	de	ADP	_	_	10	case	_	_
9	14	14	NUM	_	NumType=Card	10	nummod	_	SpaceAfter=No
10	h	h	NOUN	_	_	1	nmod	_	SpaceAfter=No
11	30	30	NUM	_	NumType=Card	10	nummod	_	_
12	à	à	ADP	_	_	14	case	_	_
13	18	18	NUM	_	NumType=Card	14	nummod	_	SpaceAfter=No
14	h	h	NOUN	_	_	10	nmod:range	_	SpaceAfter=No
15	.	.	PUNCT	_	_	1	punct	_	_
"""

	## small example
	tree = conll3.conll2tree(conll) # str -> Tree
	gov_initial=0.5
	random_tree = create_random_pj_linearisation(tree, gov_initial=gov_initial) # random linearisation + projective
	r_nonproj = create_random_nonpj_linearisation(tree) # random linearisation

	trees = [random_tree, r_nonproj]
	conll3.trees2conllFile(trees, "sample_randomly-linearised-trees.conllu") # writes the conll to a file