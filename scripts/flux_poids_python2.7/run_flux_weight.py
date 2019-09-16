#! usr/bin/python
# coding:utf-8

import os
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import conll, bdd_for_trees
import dir_functions as df
import json
from config import FUNC_RELATIONS


# date: 28/05/2019
# 28/05/2019

# TODO:


def project_by_dir(dir_path):
    # 创建项目的output文件夹
    list_corpus = os.listdir(dir_path)
    print "corpus list :  ", list_corpus

    output_corpus_path = dir_path + "output"
    df.mkdir(output_corpus_path)
    for corpus_dir in list_corpus:
        corpus_dir_path = dir_path + "/" + corpus_dir
        # 创建子文件夹
        corpus_files = os.listdir(corpus_dir_path)
        for f in corpus_files:
            print("corpus %s" %f)
            if f.endswith(".conllu"):
                # 处理文件路径
                file_path = corpus_dir_path + "/" + f
                output_file_path = output_corpus_path + "/" + f+".json"
                # print output_file_path
                trees_generator = conll.conllFile2trees(file_path)
                trees, mat_flux, id_dep = bdd_for_trees.all_bdd_for_flux(trees_generator)
                file_mat = open(output_file_path, "w")
                json.dump(unicode(mat_flux), file_mat, ensure_ascii=False, encoding='utf-8')
                weight = corpus_weight(mat_flux, conll.conllFile2trees(file_path))
                print weight

                # save conllu
    #             output = open(output_file_path, "w")
    #             output.write(output_text)
    #             # 存数据结果
    #             data_ratio_avr[corpus_dir] = r_avr_corpus
    #
    # # """输出csv"""
    # # data_ratio_dist = DataFrame(data_ratio_dist)
    # # data_ratio_dist.to_csv("ratio_dist.csv", encoding="utf-8", header=True, index=False, line_terminator="\n")
    #
    # data_ratio_avr = DataFrame(data_ratio_avr)
    # data_ratio_avr.to_csv("ratio_avr.csv", encoding="utf-8", header=True, index=False, line_terminator="\n")



def corpus_weight(mat_flux, trees_generator, func=True):
    """
    :param mat_flux: matrice du flux
    :param trees_generator: trees generator object
    :param func: si on veut functional relations
    :return: weight_liste
    """

    """init"""
    weight_list = []
    func_relations = []

    """ config """
    if not func:
        func_relations = FUNC_RELATIONS

    """traitement principal"""
    for tree in trees_generator:
        # print tree.text
        arbre = tree.id
        liste_W = []
        """ 处理 tree的 punct_list属性的值, 记录根的位置 root"""
        """ traiter punct_list et root de l'arbre"""
        for i in tree:
            head = tree[i].get("gov", "").values()[0]
            if head == "root":
                tree.root = i
            if head == "punct":
                tree.punct_list.append(i)

        """ flux 的处理和计算 """
        """ traitement flux """
        for flux in mat_flux[arbre]:
            flux_item = flux
            weight = 0
            matrice = []

            if len(mat_flux[arbre][flux]) >= 1:
                # print flux, mat_flux[arbre][flux]
                if flux_item in tree.punct_list:
                    """ 如果在punct list 里面, 就先不要考虑 继续往下循环"""
                    # print flux_item, "in punctlist! "
                    continue
                # print flux_item, "ok not in punct list"
                traitementFlux = mat_flux[arbre][flux]
                if not func:
                    traitementFlux = supprFunc(traitementFlux, func_relations)

                if traitementFlux is None:
                    """ 这里要注意, 当这个flux 被删的完全什么都没有了, 就直接输出0值 为了保持 relation的个数和flux的个数的一致性"""
                    # print "maybe problem"
                    # print tree.text
                    liste_W = liste_W + [0]
                    continue
                for ligne,colonne in traitementFlux.iteritems():
                    """
                    mat_flux[arbre][flux]: {1: [[9, 7, u'nmod', 2, u'PROPN', u'NOUN', u'Hughes', u'vie', 1, 1]]}
                    ligne: 1
                    colonne: [[9, 7, u'nmod', 2, u'PROPN', u'NOUN', u'Hughes', u'vie', 1, 1]]     
                    """
                    for element in colonne:
                        if element != '':
                            matrice = matrice+ [(element[8], element[9])]

                weight = calcul_dans_matrice(matrice, weight)
                liste_W = liste_W + [weight]
        weight_list = weight_list + liste_W
    return weight_list


def sup(ch,mt):
    liste = []
    if ch:
        for element in mt:
            if element[0] == ch[0] or element[1] == ch[1]:
                liste = liste + [element]
        for rmv in liste:
            # print "rmv", rmv
            mt.remove(rmv)
        return mt


def calcul_dans_matrice(m,e):
    # ex. m == [(1,1),(1,2),(1,3),(2,2)]
    if m or m!=[]:
        l=[]
        c=[]
        for x in m:
            l=l+[x[0]]
            c=c+[x[1]]
        # print l,c
        choix=''
        # on regarde chaque ligne
        for element in m:
            if c.count(element[1])==1:
                # si seul dans sa colone
                # print element
                e=e+1
                choix=element
                break
        # si on n'a pas trouver le choix. donc il est toujours ''
        if choix=='':
            #on regarde les colonnes
            for element in m:
                if l.count(element[0])==1:
                    # si seul dans sa ligne
                    # print element
                    e=e+1
                    choix=element
                    break
        m = sup(choix, m)
        # on supprime la ligne et la colonne du Choix
        # print e
        # print "m",m
        # Si dans m, il y a encore des choses, il faut continuer, si il est deja vide, retourner la valeur e.
        return calcul_dans_matrice(m,e)
    else:
        return e


def supprFunc(flux, func_relations):
    """pas necessaire pour l instant, pas très important et c'est moche """
    # func_relations = [u"conj", u"aux", u"fixed", u"flat", u"det", u"case", u"cop", u"mark", u"flat:name"]
    func=[]
    # trouver ou sont les func
    for ligne, colonne in flux.iteritems():
        for element in colonne:
            if element!='' and element[2] in func_relations:
                # dans chaque ligne , pour chaque element , si cet relation est functionnelle
                    func.append((ligne,colonne.index(element)))
                    # print func
                    # os.system("pause")
    # supprimer les funcs et exporter une nouvelle flux_mat
    if func==[]:return flux  # si func est vide, c-a-dire pas de func, donc on garde le flux
    else:  # sinon il faut supprimer les relations func dans le flux et regenerer la dictionnaire matrice
        # print "supression des relations func"
        # print flux
        ligne_supprimer = []
        for (l, c) in func:
            flux[l][c] = ""
        for (l,c) in func:
            if l in flux.keys():  # si l existe
                if flux[l].count('') == len(flux[l]):
                # si une ligne est vide
                    del flux[l]
                    ligne_supprimer.append(l)
                # memoriser les lignes supprimees
            if flux == {}: return None
            for col_vide in range(0,len(flux[flux.keys()[0]])-1):
                # pour un rang de 1 jusqu au longueur de la ligne l +1
                # print "debug ",flux,col_vide
                dele=1
                if [flux[ligne][col_vide] for ligne in flux].count("") == len(flux):
                    # si une colonne est vide apres la supression d une ligne
                    # print [flux[row][col_vide] for row in flux]
                    for ligne in flux:
                        del flux[ligne][col_vide]
                        dele=0
                if dele==0:
                    break  # chaque fois supprimer une colonne
        # print "ligne supprimer: ", ligne_supprimer
        if ligne_supprimer != []:
            newflux = {}
            # print range(1, len(flux)+1)
            for key in range(1, len(flux) + 1):
                newflux[key] = flux[flux.keys()[key - 1]]
            # print "newflux ", newflux
            flux = newflux
        for key in flux.keys():
            # reorganiser les numeros dans le dicitonnaire de matrice
            ctr = 0
            for relation in flux[key]:
                ctr = ctr + 1
                if relation != "":
                    relation[8] = key
                    relation[9] = ctr
        # print "flux final : ", flux
        # os.system("pause")
    if 1 not in flux.keys():
        print flux
    for col_vide in range(0, len(flux[flux.keys()[0]]) - 1):
        if [flux[ligne][col_vide] for ligne in flux].count("") == len(flux):
            print "!!!!", flux
            os.system("pause")
    return flux


def main():
    # project_by_dir("corpus/sud-treebanks-v2.2_concate")
    # project_by_dir("corpus/ud-treebanks-v2.2_concate")
    project_by_dir(u"corpus/test")


if __name__ == '__main__':
    main()