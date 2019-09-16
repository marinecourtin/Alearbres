# Summary
The Universal Dependency version of the French Treebank (Abeillé et al., 2003), hereafter UD_French-FTB, is a treebank of sentences from the newspaper Le Monde, initially manually annotated with morphological information and phrase-structure and then converted to the Universal Dependencies annotation scheme.

# Introduction
UD_French-FTB 2.3 is an automatic conversion of the [French Treebank](http://ftb.linguist.univ-paris-diderot.fr/index.php?langue=en).
The French Treebank constituency trees were first converted to dependency trees following (Candito et al., 2010), then the dependency trees were converted to UD scheme using B. Guillaume's [Sequoia treebank UD conversion rules](https://gitlab.inria.fr/grew/SSQ_UD). Finally a data-driven cross-treebank annotation transfer process (Seddah et al, 2017, forthcoming) was applied.

<!-- This release of the French Treebank (Abeille et al, 2003) UD 2.3 version is based on the FTB SPMRL release (Seddah et al, 2013)
whose tokenization has been changed to match the [UD 2.0 specifications](http://universaldependencies.org/u/overview/tokenization.html) . Its native depedency scheme was converted via the use of the [Sequoia treebank UD conversion rules](https://gitlab.inria.fr/grew/SSQ_UD) and a data-driven cross-treebank annotation transfer process (Seddah et al, 2017, forthcoming).
-->

An evaluation on a gold standard leads to 94.75% of LAS, 99.40% UAS on the test set, on par with other high quality UD treebanks such as UD_English.


# Origin
The French Treebank annotation project began in 1997 and has a long history of intermediate releases, culminating with [the official 1.0 version](http://ftb.linguist.univ-paris-diderot.fr/index.php?langue=en), available since January 2017.
The official reference is (Abeillé et al. 2003).

Some notable versions have been used for research in  statistical parsing:
* 2004: whole set of sentences used by Arun et al. 2005 , without any functional annotations ;
* 2007: version with 12.531 sentences with functional annotations, used e.g. in Candito et al. 2010 ;
* 2010: version with 15.922 sentences with functional annotations, used e.g. in Green et al., 2011 ;
* 2013: version with 18.535 sentences with functional annotations, used for the [SPMRL 2013, 2014 shared tasks](http://dokufarm.phil.hhu.de/spmrl2014/doku.php).

To ease comparison with published parsing results, we derived the UD_French-FTB from the version released for the SPMRL Shared Tasks (2013, 2014).

# Splitting
The whole corpus contains 18,535 sentences and 456,576 tokens.

In **UD_French-FTB**, the split follows the FTB SPMRL instance.
 * `fr_ftb-ud-test.conllu`: 61,287 tokens for 2541 sentences
 * `fr_ftb-ud-dev.conllu`: 318,818 tokens for 1235 sentences
 * `fr_ftb-ud-train.conllu`: 363,471 tokens for 14,759 sentences

Note that, the first 9981 sentences correspond to the canonical 2007 training set,  the last 1235 sentences of the test set to its 2007 counterpart and the dev set is the same.


# Genres
The original sentences of the corpus originate from the Le Monde newspaper (1990-1993), and cover various kind of newswire articles (sports, cinema, interviews, current affairs and financial news).


# Building the Treebank
The construction of the **UD_French-FTB** is described in this paper (Seddah et al, 2017, to appear).

# License

The original French treebank is distributed freely for research purposes. An ID licence number
can be obtained by filling the form at:
http://ftb.linguist.univ-paris-diderot.fr/telecharger.php?&langue=en

<!-- provided you fill and return the licence
that can be found here : http://www.llf.cnrs.fr/Gens/Abeille/French-Treebank-fr.php.
-->

<!--Alternatively, the original FTB can be downloaded and an ID license number will be provided.-->

Please note that the UD annotation layers are released under the LGPL-LR license.

# How to get the full data
Due to the FTB licensing restrictions (original data are under an LDC's license), the UD_French-FTB is released without the lexical data. To merge the annotation with the corresponding FTB data, please follow the following steps:

- Obtain a copy of the original FTB (either via the [application form](http://ftb.linguist.univ-paris-diderot.fr/telecharger.php?&langue=en) cited above or via the SPMRL Shared Task data set license http://dokufarm.phil.hhu.de/spmrl2014/lib/exe/fetch.php?media=french.pdf)
- Send the ID license number or the signed license to djame.seddah@gmail.com
- a diff file will be then made available for download
- uncompress and apply that patch inside the current UD_French-FTB directory (eg. patch -p1 < [patch file])


# Acknowledgments

contributors:
Marie Candito, Bruno Guillaume, Teresa Lynn, Hector Martinez-Alonso, Benoit Sagot, Djamé Seddah, Eric Villemonte de la Clergerie

contact:
Djamé Seddah: djame.seddah@paris-sorbonne.fr
Marie Candito: marie.candito@linguist.univ-paris-diderot.fr

# References
**(Abeillé et al., 2003)**  Anne Abeillé, Lionel Clément, and Françàçs Toussenel. 2003. "Building a treebank for French", in A. Abeillé (ed) Treebanks, Kluwer, Dordrecht.

**(Arun et Keller. 2005)** Abhishek Arun and Frank Keller. 2005. Lexicalization in crosslinguistic probabilistic parsing: The case of French. In Proceedings of ACL, pages 306–313, Ann Arbor, MI, USA.

**(Candito et al, 2010)** Marie Candito, Benoît Crabbé and Pascal Denis. 2010. Statistical French dependency parsing: treebank conversion and first results. In Proceedings of LREC'2010, La Valletta, Malta.

**(Green et al, 2011)** Spence Green, Marie-Catherine de Marneffe, John Bauer J. and Christopher D. Manning. "2011. Multiword Expression Identification with Tree Substitution Grammars: A Parsing tour de force with French." In EMNLP 2011.

**(Seddah et al, 2013)** Djamé Seddah, Reut Tsarfaty, Sandra Kübler, Marie Candito, Jinho D. Choi, Richárd Farkas, Jennifer Foster, Iakes Goenaga, Koldo Gojenola Galletebeitia, Yoav Goldberg, Spence Green, Nizar Habash, Marco Kuhlmann, Wolfgang Maier, Yuval Marton, Joakim Nivre, Adam Przepiórkowski, Ryan Roth, Wolfgang Seeker, Yannick Versley, Veronika Vincze, Marcin Woliski,Alina Wróblewska,Eric Villemonte de la Clergerie. 2013. "Overview of the SPMRL 2013 Shared Task: A Cross-Framework Evaluation of Parsing Morphologically Rich Languages" Proceedings of the Fourth SPMRL Workshop, Seattle, USA

**(Seddah et al, 2018) Djamé Seddah, Éric de La Clergerie, Benoît Sagot, Hector Martinez-Alonso, Marie Candito, "Cheating a Parser to Death: Data-driven Cross-Treebank Annotation Transfer" , Eleventh International Conference on Language Resources and Evaluation (LREC 2018), Miasaki, Japan

# Changelog

* October 31, 2018: The files were hand-corrected in order to pass the UD 2.2 validation script.
Errors were mostly due to conjuncts or fixed tokens wrongly attached to their right-hand side.

* November 21, 2017: change of licence to enable compatibility with the FTB original license in term of potential commercial usage. Correction in list of references.

* 2017-11-15 v2.1
  <!--* Automatic application of new decisions taken for harmonisation of several French Treebanks (causative, copules, auxiliaries)-->
  - A few modifications were applied to augment consistency with some of the other UD_French treebanks (main UD_French and UD_French-Sequoia):
    - The possessive determiners attach now with a "det" dependency instead of "nmod:poss"
    - Causative constructions now represent "faire" as an auxiliary.
    - The causer argument bears a nsubj:caus label
    - The only valid auxiliaries are "être", "avoir" and "faire" (a dozen unfixed cases remain though)
    - The only valid copula is "être"
    - Moreover, when the copula introduces an infinitival clause or a full clause, then "être" is not treated as a cop, but is taken to be the root.

  	Examples:
	- L'objectif est de calmer les esprits ==>  "est" is root, and "calmer" is its xcomp.
        - Le plus étonnant est que la baisse accélère ==> "est" is root, and "accélère" is its ccomp

* 2017-03-08 v2.0
  * First release for inclusion as supplementary data for the ConLL 2017 Universal Dependency parsing shared task.


=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.0
License: LGPL-LR
Includes text: no
Genre: news
Lemmas: converted from manual
UPOS: converted from manual
XPOS: not available
Features: converted from manual
Relations: converted from manual
Contributors: Candito, Marie; Guillaume, Bruno; Lynn, Teresa; Martínez Alonso, Héctor; Sagot, Benoît; Seddah, Djamé; Villemonte de la Clergerie, Eric
Contributing: elsewhere
Contact: djame.seddah@paris-sorbonne.fr, marie.candito@linguist.univ-paris-diderot.fr
===============================================================================
