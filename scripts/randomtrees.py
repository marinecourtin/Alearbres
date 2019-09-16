import random
import numpy as np
import conll3
from conll3 import  Tree
import copy


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

def is_root(node):
    if 0 in node["gov"]:
        return True
    else:
        return False

def get_root(tree):
    """
    
    """
    for num in tree:
        node = tree[num]
        if is_root(node):
            return num
            # return list(node["kids"].keys())

def get_kids(tree, num):
    """
    @args:
        - Tree()
        - Int : id of the parent node
    @out:
        - List() : list of ids of kid nodes
    """
    kids = list(tree[num]["kids"])
    return kids

def randomly_select_dep(deps):
	"""
	@args :
		- List() : list of dep ; [1,2]
	@out :
		- List() : list of dep in the order that they will be processed; [2,1]
    
	Note:
	il faut garder l'ordre en memoire pour le reutiliser quand on traite les dependants
	"""
	random.shuffle(deps)

def randomly_select_order(tree, linearisation, node, gov_initial):
    """
    @args:
        - Tree()
        - List() : list of dep ; [2,0,1]
        - Int : node ; 3

    @out :
        - List() ; [2,3,0,1] 3 (kid of 2) was placed on the right of its gov
    """
    # True:left ; False:right
    left = np.random.rand() > gov_initial

    # get gov of node
    gov = list(tree[node]["gov"])[0]
    gov_rank = linearisation.index(gov)

    # insert node in list next to its gov
    if left:
        # print("left")
        linearisation.insert(gov_rank, node)
    else:
        # print("right")
        linearisation.insert(gov_rank+1, node)
    
    # print("linearisation ", linearisation)
    return linearisation

def random_tree():
    """traitement principal
    :return:
    """
    pass


def random_tree1(tree, gov_initial=0.5):
    """ traitement principal
    tree: Tree(), float (% of gov_initial dependency links)
    :return: 
    """
    # TODO: 1. c'est pas exhaustif  2. (pas tres sure)
    # print("main function")
    tree_for_rewrite = copy.deepcopy(tree)
    tree.addkids(tree)
    num_root = get_root(tree)
    # print("root ", num_root)
    linearisation = [num_root]
    recursif_kids(tree, num_root, linearisation, gov_initial)
    # print(rewrite_tree(tree_for_rewrite, linearisation))
    return rewrite_tree(tree_for_rewrite, linearisation)


def recursif_kids(tree,node, linearisation, gov_initial):
    all_kids = get_kids(tree, node)
    # print("all_kids", all_kids)
    randomly_select_dep(all_kids)
    # print("all kids randomized order ", all_kids)
    if all_kids:
        for kid in all_kids:
            randomly_select_order(tree, linearisation, kid, gov_initial)
            recursif_kids(tree,kid, linearisation, gov_initial)

def rewrite_tree(tree, li):
    """
    takes a Tree() and a list() which represent the new linearisation
    output : new Tree(), a conllu string
    """
    # print(tree)
    new_tree = Tree()
    for i, node in tree.items():
        """ take tree node and change id and gov"""
        new_node = tree[li[i-1]]
        # print(new_node)
        """ change id """
        new_node["id"] = i
        gi = list(new_node["gov"].keys())[0]
        if gi != 0:
            """change governor info"""
            new_gi = li.index(gi)+1
            # print(new_gi)
            new_node["gov"] = {new_gi: new_node["gov"][gi]}
        new_tree[i] = new_node
    # print("updated tree %s" % new_tree)
    # text = new_tree.conllu()
    # del(tree)
    # del(new_tree)
    # return text
    return new_tree



if __name__ == "__main__":
    tree = conll3.conll2tree(conll2)
    # tree = conll3.conll2tree(conll)
    random_trees = list()
    gov_initial=0.8
    for x in range(100):

        # chunxiao
        # tree_for_random = copy.deepcopy(tree)
        # random_tree1(tree_for_random)
        # del(tree_for_random)

        # marine
        random_tree = random_tree1(tree, gov_initial=gov_initial)
        random_trees.append(random_tree)
    conll3.trees2conllFile(random_trees, "random-projective-trees_"+str(gov_initial)+"_gov-initial.conllu")


    # making a random sequoia
    
    # on recupere les arbres
    # on linearise