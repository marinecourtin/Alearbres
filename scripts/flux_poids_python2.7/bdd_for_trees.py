#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Entrée : trees_generator = conll.conllFile2trees("SUD_French-Spoken.conllu")

Sortie :
- trees
    → dictionnaire indiquant, pour chaque arbre, la liste des dépendances
    → --- trees = {n° arbre : [tok, gov, fct], [tok, gov, fct], ...]}
- liste_arbres
    → liste des id des arbres
- cats
    → cats = {n° arbre: [cat mot1, cat mot2, ...]}
- mots
    → mots = {n° arbre : [mot1, mot2, mot3, ...]}
- dep_ord
    → dep_ord = {n° arbre: [[tok_g, tok_d], ...]}
- id_dep
    → id_dep = {n° arbre: [[tok, tok_gov, fct, sens+empan, cat, cat_gov, mot, mot_gov],...]}
- id_flux
- mat_flux
script adapter à partir de la version de Marie-Amélie Botalla
"""

import conll,time

#TODO: 把tree的部分 搬家到treefuncitons里面 ，然后这里只进行调用！！！！！！
#TODO: 写的太麻烦！！ 不停地重复遍历不好，要看看flux的时候具体用到哪个function，直接一次遍历生成自己想要的内容 ，最多允许遍历两次，多了太慢！！


def liste_arbres(trees):
    id = 0
    for tree in trees:
        id +=1
        yield id


def all_bdd_for_flux(trees_generator):
    trees = {}
    # --- trees = {n° arbre : [[tok, gov, fct], [tok, gov, fct], ...]}
    tree_id = 0
    # print "bdd cats"
    cats = {}
    # dictionnaire contenant les cats des mots de chaque phrase
    # --- cats = {n° arbre: [cat mot1, cat mot2, ...]}
    mots = {}
    # dictionnaire contenant les mots de chaque phrase
    # --- mots = {n° arbre : [mot1, mot2, mot3, ...]}
    for tree in trees_generator:
        tree_id += 1
        trees[tree_id] = []
        cats[tree_id] = []
        mots[tree_id] = []
        for id_node, node in tree.iteritems():
            cats[tree_id].append(node["tag"])
            mots[tree_id].append(node["t"])
            for gi, gnode in node["gov"].iteritems():
                trees[tree_id].append([id_node, gi, gnode])

    # si la relation est punct ou attention, on le valeur 0  pour ne pas comptabiliser
    dep_ord = {}
    id_dep = {}
    # --- id_dep = {n° arbre: [[tok, tok_gov, fct, sens+empan, cat, cat_gov, mot, mot_gov],...]}
    # liste des dépendances pour chaque arbre
    # --- dep_ord = {n° arbre: [[tok_g, tok_d], ...]}
    for t in trees.keys():
        # pour chaque arbre
        dep_ord[t] = []
        id_dep[t] = trees[t]
        # liste des liens
        for link in trees[t]:

            # if "punct" in link[2] or "attention" in link[2]:
            #     link[1] = 0

            # pour chaque lien, on range les tokens dans l'ordre de lecture
            elt = [link[0], link[1]]
            elt.sort()
            dep_ord[t].append(elt)

            if link[1] != 0:
                link.append(link[0] - link[1])
            else:
                link.append(0)
                # catégories
            link.append(cats[t][link[0] - 1])
            if link[1] != 0:
                link.append(cats[t][link[1] - 1])
            else:
                link.append("root")
            # mots
            link.append(mots[t][link[0] - 1])
            if link[1] != 0:
                link.append(mots[t][link[1] - 1])
            else:
                link.append("root")
    id_flux_dict = id_flux(id_dep, dep_ord)
    mat_flux = toutesmatrice(id_flux_dict)

    return trees, mat_flux, id_flux_dict


def bdd_trees(trees_generator):
    print "bdd trees"
    trees = {}
    # --- trees = {n° arbre : [[tok, gov, fct], [tok, gov, fct], ...]}
    tree_id = 0
    for tree in trees_generator:
        tree_id += 1
        trees[tree_id] = []
        for id_node, node in tree.iteritems():
            for gi, gnode in node["gov"].iteritems():
                trees[tree_id].append([id_node,gi, gnode])

    # si la relation est punct ou attention, on le valeur 0  pour ne pas comptabiliser
    for t in trees.keys():
        for l in trees[t]:
            if "punct" in l[2]:
                l[1] = 0
    return trees


def bdd_cats(trees_generator):
    print "bdd cats"
    cats = {}
    # dictionnaire contenant les cats des mots de chaque phrase
    # --- cats = {n° arbre: [cat mot1, cat mot2, ...]}
    tree_id = 0
    for tree in trees_generator:
        # print tree
        tree_id += 1
        cats[tree_id] = []
        for id_node, node in tree.iteritems():
            cats[tree_id].append(node["tag"])

    return cats


def bdd_mots(trees_generator):
    print "Liste des mots"
    mots = {}
    # dictionnaire contenant les mots de chaque phrase
    # --- mots = {n° arbre : [mot1, mot2, mot3, ...]}
    tree_id = 0
    for tree in trees_generator:
        # print tree
        tree_id += 1
        mots[tree_id] = []
        for id_node, node in tree.iteritems():
            # print node
            # for gi, gnode in node["gov"].iteritems():
            mots[tree_id].append(node["t"])
    return mots
    # pickle.dump(mots, open("mots.p","wb"))


def dep_ord(trees):
    print "dep_ord"
    dep_ord = {}
    # liste des dépendances pour chaque arbre
    # --- dep_ord = {n° arbre: [[tok_g, tok_d], ...]}

    for t in trees.keys():
        # pour chaque arbre
        dep_ord[t] = []
        # liste des liens
        for link in trees[t]:
            # pour chaque lien, on range les tokens dans l'ordre de lecture
                elt = [link[0], link[1]]
                elt.sort()
                dep_ord[t].append(elt)

    return dep_ord

    # pickle.dump(dep_ord,open("dep_ord.p","wb"))


def id_dep(trees, cats, mots):
    print "id_dep"
    id_dep = {}
    # --- id_dep = {n° arbre: [[tok, tok_gov, fct, sens+empan, cat, cat_gov, mot, mot_gov],...]}
    for t in trees.keys():
        id_dep[t] = trees[t]
        for link in id_dep[t]:
            # print t
            # sens et empan
            # print "link",link,trees[t]
            # print t
            if link[1] != 0:
                link.append(link[0]-link[1])
            else:
                link.append(0)
            # catégories
            link.append(cats[t][link[0]-1])
            if link[1] != 0:
                link.append(cats[t][link[1]-1])
            else:
                link.append("root")
            # mots
            link.append(mots[t][link[0]-1])
            if link[1] != 0:
                link.append(mots[t][link[1]-1])
            else:
                link.append("root")
    return id_dep

    # pickle.dump(id_dep,open("id_dep.p","wb"))


def id_flux(id_dep, dep_ord):
    # print "id_flux"
    # TODO: change this function!!!!!!! too slow！！！！！ too much “for”！！！！
    # id_dep = pickle.load(open("id_dep.p","rb"))
    # dep_ord = pickle.load(open("dep_ord.p","rb"))
    id_flux_temp = {}

    for t in dep_ord.keys():
        id_flux_temp[t] = {}
        l = []
        l_fin = []
        posmax = 0
        for dep in dep_ord[t]:
            if dep[1] > posmax:
                posmax = dep[1]
        pos = 1
        while pos < posmax:
            l.append([])
            if len(l) != 1:
                l[-1].extend(l[-2])
            for dep in dep_ord[t]:
                if dep[0] == pos:
                    l_fin.append(dep[1])
                    l[-1].append(dep)
            f = 0
            while f < len(l_fin):
                if l_fin[f] == pos:
                    l_fin.pop(f)
                    l[-1].pop(f)
                    f -= 1
                f += 1
            id_flux_temp[t][pos] = l[-1]
            pos += 1

    id_flux = {}

    for t in id_flux_temp.keys():
        id_flux[t] = {}
        for p in id_flux_temp[t].keys():
            id_flux[t][p] = []
            for dep in id_flux_temp[t][p]:
                for elt in id_dep[t]:
                    a = [elt[0],elt[1]]
                    a.sort()
                    if dep[0] == a[0] and dep[1] == a[1]:
                        id_flux[t][p].append(list(elt))

    for t in id_flux.keys():
        for p in id_flux[t].keys():
            entree = []
            sortie = []
            for dep in id_flux[t][p]:
                if min(dep[0],dep[1]) not in entree:
                    entree.append(min(dep[0],dep[1]))
                if max(dep[0],dep[1]) not in sortie:
                    sortie.append(max(dep[0],dep[1]))
            entree.sort()
            sortie.sort()
            sortie.reverse()
            for d in range(len(id_flux[t][p])):
                dep = id_flux[t][p][d]
                ajout = []
                pl_in = 1
                for i in range(len(entree)):
                    if entree[i]==min(dep[0],dep[1]):
                        ajout.append(pl_in)
                    pl_in += 1
                pl_out = 1
                for i in range(len(sortie)):
                    if sortie[i]==max(dep[0],dep[1]):
                        ajout.append(pl_out)
                    pl_out += 1
                id_flux[t][p][d] = id_flux[t][p][d]+ajout

    # print id_flux[15376]
    # pickle.dump(id_flux,open("id_flux.p","wb"))
    return id_flux


def toutesmatrice(id_flux):
    # id_flux = pickle.load(open("id_flux.p","rb"))
    # for t in id_flux.keys():
        # print t
        # raw_input(id_flux[t])
    mat_flux = {}
    for t in id_flux.keys():
        mat_flux[t] = {}
        for p in id_flux[t].keys():
            mat_flux[t][p] = {}
            lin = 0
            col = 0
            for dep in id_flux[t][p]:
                if dep[-2] > lin:
                    lin = dep[-2]
                if dep[-1] > col:
                    col = dep[-1]
            for i in range(lin):
                mat_flux[t][p][i+1] = []
                for j in range(col):
                    mat_flux[t][p][i+1].append("")
            for dep in id_flux[t][p]:
                pl_in = dep[-2]
                pl_out = dep[-1]-1
                mat_flux[t][p][pl_in][pl_out] = dep

    # pickle.dump(mat_flux,open("mat_flux.p","wb"))
    return mat_flux


if __name__ == '__main__':
    start = time.time()
    """
    cats = bdd_cats(conll.conllFile2trees("SUD_Czech-PDT.conllu"))
    mots = bdd_mots(conll.conllFile2trees("SUD_Czech-PDT.conllu"))
    trees = bdd_trees(conll.conllFile2trees("SUD_Czech-PDT.conllu"))
    dep_ord = dep_ord(trees)
    id_dep = id_dep(trees, cats, mots)
    id_flux = id_flux(id_dep, dep_ord)
    mat_flux = toutesmatrice(id_flux)
    print mat_flux
    """
    print all_bdd_for_flux(conll.conllFile2trees("corpus/sud-treebanks-v2.2_concate/SUD_French-Spoken/SUD_French-Spoken.conllu"))
    end = time.time()
    print "time,", start, end
