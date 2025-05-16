# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:59:10 2024

@author: mjoigneau
"""


#%% ====================== PACKAGES ===========================================


import PyPDF2
from PyPDF2 import PdfReader
import pandas as pd
import camelot
import numpy as np
from os import listdir
from os.path import isfile, join
import re
import itertools


#%% ====================== FONCTIONS ==========================================
#%%% ====== I/ MOTS CLES POUR SEPARER TEXTE ===================================


# On créé toutes les combinaisons de mots clés séparés
def sep_keywords(key,sep):
    
    combi = pd.DataFrame(list(itertools.product(sep, repeat=len(key)-1)))
    #print(combi)
    
    result = []
    for i in range(len(combi)):
        print("\ni is ", str(i))
        result_j = ""
        for j in range(len(key)-1):
            result_j = result_j + key[j] + combi.loc[i,j]
            #print(result_j)
        result_j = result_j + key[len(key)-1]
        result = result + [result_j]

    return(result)

# sep1 = ["p","q"]
# key1 = ["1","2","4"]
# sep_keywords(key1,sep1)



#%%% ====== II/ EXTRAIRE LE TEXTE =============================================


# Extraire la données textuelle (hors tableaux)
def extract_data_from_text(keywords):
    
    choix_keyword = []
    for i in range(len(keywords)) :
        #print("\ni is " + str(i) + " ====")
        choix_keyword_j = []
        for j in range(len(keywords[i])) :
            #print("\nj is " + str(j) + "----")
            #print(keywords[i][j])
            if (keywords[i][j] in text) == True :
                #print("True !")
                choix_keyword_j = choix_keyword_j + [j]
        # On prend la 1ère occurence au cas où il y ait des doublons
        if len(choix_keyword_j)>0:
            choix_keyword = choix_keyword + [choix_keyword_j[0]]
        else:
            choix_keyword = choix_keyword + [0]
        print(choix_keyword)
    print(choix_keyword)

    info = []
    for i in range(len(keywords)-1) :
        print("\ni is " + str(i) + " ====")
        # Index du début (on y ajoute la longueur du mot de l'index)
        index_debut = text.index(keywords[i][choix_keyword[i]]) + len(keywords[i][choix_keyword[i]])
        print("index début")
        print(index_debut)
        # Index de fin
        index_fin = text.index(keywords[i+1][choix_keyword[i+1]])
        print("index fin")
        print(index_fin)
        # Information entre les 2 index
        info_here = text[index_debut:index_fin]
        print("information")
        print(info_here)
        info = info + [[info_here]]
        print("toutes les informations")
        print(info)
        
    return info    



#%%% ====== III/ FEUILLETS EXCEL ==============================================


# On y ajoute les 3 colonnes nécessaires à tous les feuillets
def annee_PEPR_projet_NaN(df, annee_df, PEPR_df, projet_df):
    
    # On y rajoute les colonnes
    df.insert(0,"Année",annee_df)
    df.insert(1,"AcronymePEPR",PEPR_df)
    df.insert(2,"AcronymeProjet",projet_df)
    
    # On convertie la colonne du PEPR sinon elle n'apparaît pas sur l'Excel
    df['AcronymePEPR'] = df['AcronymePEPR'].astype(str)  # Si tu veux forcer le type chaîne
    
    # Et on y remplace les VIDE par des NaN
    df.replace(to_replace = "VIDE",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "\nVIDE\n",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = " \nVIDE\n",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "  \nVIDE\n",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "   \nVIDE\n",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = " \nVIDE",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = " \nVIDE",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "   \nVIDE",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "   \nVIDE ",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = " VIDE\n",
               value = np.nan,
               inplace = True)
    df.replace(to_replace = "VIDE\n",
               value = np.nan,
               inplace = True)
    
    # Et on y remplace les NA par des NaN
    df.replace(to_replace = "NA",
               value = np.nan,
               inplace = True)
    # Et on y remplace les RAS par des NaN
    df.replace(to_replace = "RAS",
               value = np.nan,
               inplace = True)
    
    return df




#%%% ====== IV/ INDICATEURS ===================================================
#%%%% ----- 1) Année ----------------------------------------------------------

## Année
def indic_annee(data_infoprojet) :

    # On prend la partie du PDF
    annee = data_infoprojet[1]
    print(annee)
    # On extrait uniquement l'année
    annee = int(annee[0][7:11])
    
    return(annee)



#%%%% ----- 2) Projet ---------------------------------------------------------


## Projet
def indic_projet(data_infoprojet) :

    projet = data_infoprojet[0]
    projet = projet[0].strip()
    print(projet)
    
    return(projet)


## Simplifié ou non
def simplifie(dir_PEPR_projets, projet):
    
    # On lit l'Excel PEPR projet
    PEPR_projets = pd.read_excel(dir_PEPR_projets, sheet_name = "Feuil1")
    print(PEPR_projets)
    # On trouve le PEPR qui correspond au projet
    simplifie_pas = PEPR_projets[PEPR_projets["Projet"] == projet]['Reporting_simplifié'].values[0]
    print(simplifie_pas)
    
    return(simplifie_pas)


## SNA ou non
def SNA(dir_PEPR_projets, projet):
    
    # On lit l'Excel PEPR projet
    PEPR_projets = pd.read_excel(dir_PEPR_projets, sheet_name = "Feuil1")
    print(PEPR_projets)
    # On trouve le PEPR qui correspond au projet
    SNA_PEPR = PEPR_projets[PEPR_projets["Projet"] == projet]['SNA'].values[0]
    print(SNA_PEPR)
    
    return(SNA_PEPR)


#%%%% ----- 3) PEPR -----------------------------------------------------------

## PEPR
def indic_PEPR(dir_PEPR_projets, projet) :

    # On lit l'Excel PEPR projet
    PEPR_projets = pd.read_excel(dir_PEPR_projets, sheet_name = "Feuil1")
    print(PEPR_projets)
    # On trouve le PEPR qui correspond au projet
    PEPR = PEPR_projets[PEPR_projets["Projet"] == projet]['PEPR'].values[0]
    print(PEPR)
    
    return(PEPR)



#%%%% ----- 4) Infos du projet ------------------------------------------------

# data_infoprojet = extract_data_from_text(keywords_info)

# for i in range(len(data_infoprojet)):
#     print("===================================================")
#     print(i)
#     print("===================================================")
#     print(data_infoprojet[i])

## Infos du projets
def indic_infoprojet(data_infoprojet, reporting_simplifie, SNA_PEPR) :

    # On supprime la partie du PDF qui ne nous intéresse pas
    if reporting_simplifie == "Oui" :
        print("reporting simplifie")
        print(data_infoprojet[16])
        del data_infoprojet[16]
    else :
        print("reporting non simplifié")
        print(data_infoprojet[29])
        del data_infoprojet[29]
    
    # On rajoute une case vide si le PEPR ne suit pas une SNA
    if (SNA_PEPR == "Non") or ((SNA_PEPR == "Oui") and (reporting_simplifie == "Oui")):
        data_infoprojet.insert(25,['VIDE'])
    
    # S'il n'y a pas assez de cases remplies, on en rajoute
    if len(data_infoprojet) < 31 :
        print("len < 30")
        add = 31 - len(data_infoprojet)
        data_infoprojet = data_infoprojet + add*[["VIDE"]]
        
        # Les commentaires libres vont dans la dernière case
        if reporting_simplifie == "Oui" :
            data_infoprojet = data_infoprojet + [data_infoprojet[16]]
            del data_infoprojet[16]
        else:
            data_infoprojet = data_infoprojet + [data_infoprojet[28]] + [data_infoprojet[29]]
            del data_infoprojet[28]
            del data_infoprojet[28]
    print(data_infoprojet)
    
    # On nettoie les données
    data_infoprojet = [[s[0].strip()] for s in data_infoprojet]
    # On enlève les \n au milieu du texte
    data_infoprojet = [x[0].replace("\n"," ") for x in data_infoprojet]
    # Puis on convertie en dataframe
    data_infoprojet = pd.DataFrame(data_infoprojet)
    print(data_infoprojet)
    
    # On supprime la ligne du projet qui va être en doublon
    data_infoprojet = data_infoprojet.drop(labels = 0)
    
    # On inverse ligne et colonne
    data_infoprojet = data_infoprojet.T
    print(data_infoprojet)
    
    return(data_infoprojet)



#%%%% ----- 5) Brevet ---------------------------------------------------------


def indic_brevet(info_indic) : 

    ## Brevet
    data_brevet = info_indic[0]
    # On nettoie les données
    data_brevet = [s.strip() for s in data_brevet]
    # On divise par \n
    data_brevet = data_brevet[0].split("\n")
    print(data_brevet)
    # On convertie en dataframe
    data_brevet = pd.DataFrame(data_brevet)
    # On précise la catégorie
    data_brevet.insert(0,"Type_ReportRST_ResultatsImpacts","Brevet")
    data_brevet.insert(1,"Identification_ReportRST_ResultatsImpacts","Numéro de demande")
    
    return(data_brevet)




#%%%% ----- 5) Données de la recherche ----------------------------------------

## Données de la recherche
def indic_donneesrecherche(info_indic) :

    data_dataset = info_indic[1]
    # On nettoie les données
    data_dataset = [s.strip() for s in data_dataset]
    # On divise par \n
    data_dataset = data_dataset[0].split("\n")
    print(data_dataset)
    # On convertie en dataframe
    data_dataset = pd.DataFrame(data_dataset)
    # On précise la catégorie
    data_dataset.insert(0,"Type_ReportRST_ResultatsImpacts","Données de la recherche")
    data_dataset.insert(1,"Identification_ReportRST_ResultatsImpacts","DOI")
    
    return(data_dataset)



#%%%% ----- 6) Code source logiciel -------------------------------------------

## Codes sources logiciel
def indic_logiciel(info_indic) :

    data_logiciel = info_indic[2]
    # On nettoie les données
    data_logiciel = [s.strip() for s in data_logiciel]
    # On divise par \n
    if "\n" in data_logiciel[0] :
        data_logiciel = data_logiciel[0].split("\n")
    elif " " in data_logiciel[0] :
        data_logiciel = data_logiciel[0].split(" ")
    print(data_logiciel)
    # On convertie en dataframe
    data_logiciel = pd.DataFrame(data_logiciel)
    # On précise la catégorie
    data_logiciel.insert(0,"Type_ReportRST_ResultatsImpacts","Code source et logiciel")
    data_logiciel.insert(1,"Identification_ReportRST_ResultatsImpacts","URL, SWHID ou DOI")

    return(data_logiciel)




#%%%% ----- 7) Technologies ---------------------------------------------------

## Technologie
def indic_techno(info_indic) :
    
    data_techno_all = info_indic[3]
    print(data_techno_all)
    
    # S'il n'y a pas assez de cases remplies, on en rajoute
    if "VIDE" in data_techno_all[0] :
        data_techno = data_techno_all + 5*["VIDE"]
        # On enlève les espaces au début et à la fin
        data_techno = [x.strip() for x in data_techno]
        # On convertie en dataframe
        data_techno = pd.DataFrame(data_techno)
        # On inverse
        data_techno = data_techno.T
        print(data_techno)
        
    else :
        # Liste de toutes les technologies clés possibles
        technologie_clef_xlsx = pd.read_excel(dir_techno, sheet_name = "Feuil1")
        technologie_clef = list(technologie_clef_xlsx["Technologie"])
        print(technologie_clef)
        
        # Technologies clés mal écrites
        if "Intelligence artiﬁcielle" in data_techno_all[0] :
            data_techno_all[0] = data_techno_all[0].replace("Intelligence artiﬁcielle","Intelligence artificielle")
            print(data_techno_all)
        
        # On souhaite y trouver les positions des débuts et fins des technologies clés dans le référentiel sans \n
        idx_techno = []
        espace_ou_non = []
        for i in range(len(technologie_clef)):
            print("i is ", str(i), " ====")
            print(technologie_clef[i])
            # Si le type de financeur est dans le texte
            if technologie_clef[i] in data_techno_all[0].replace("\n",""):
                print("True !")
                print(technologie_clef[i])
                # On cherche tous les positions où on trouve technologie_clef[i] dans data_techno_all[0]
                idx_techno_début = [match.start() for match in re.finditer(technologie_clef[i], data_techno_all[0].replace("\n",""))]
                # On y note l'espace correspondant
                espace_ou_non = espace_ou_non + [""]*len(idx_techno_début)
                # On y rajoute la position de la fin du mot
                idx_techno_i = []
                for elem in idx_techno_début :
                    idx_techno_i.append(elem)
                    idx_techno_i.append(elem + len(technologie_clef[i]))
                idx_techno = idx_techno + idx_techno_i
                print(idx_techno)
            elif technologie_clef[i] in data_techno_all[0].replace("\n"," "):
                print("True !")
                print(technologie_clef[i])
                # On cherche tous les positions où on trouve technologie_clef[i] dans data_techno_all[0]
                idx_techno_début = [match.start() for match in re.finditer(technologie_clef[i], data_techno_all[0].replace("\n"," "))]
                # On y note l'espace correspondant
                espace_ou_non = espace_ou_non + [" "]*len(idx_techno_début)
                # On y rajoute la position de la fin du mot
                idx_techno_i = []
                for elem in idx_techno_début :
                    idx_techno_i.append(elem)
                    idx_techno_i.append(elem + len(technologie_clef[i]))
                idx_techno = idx_techno + idx_techno_i
                print(idx_techno)
        # On ordonne ensuite les indices
        idx_techno = list(np.sort(idx_techno))
        print(idx_techno) 
        print(espace_ou_non)
        
        # On souhaite y trouver les positions des débuts et fins des TRL
        idx_TRL = []
        # On cherche tous les positions où on trouve technologie_clef[i] dans data_financ_all[0]
        idx_TRL_début = [match.start() for match in re.finditer("TRL", data_techno_all[0])]
        # On y rajoute la position de la fin du mot
        idx_TRL_i = []
        for elem in idx_TRL_début :
            idx_TRL_i.append(elem)
            idx_TRL_i.append(elem + 7)
        idx_TRL = idx_TRL + idx_TRL_i
        print(idx_TRL)
        # On ordonne ensuite les indices
        idx_TRL = list(np.sort(idx_TRL))
        # S'il y a moins d'indices que de TRL, on rajoute un vide
        if len(idx_TRL) % 6 != 0 : 
            idx_TRL.append(idx_TRL[len(idx_TRL)-1])
            idx_TRL.append(idx_TRL[len(idx_TRL)-1])
        print(idx_TRL) 
        
        # On souhaite y trouver les positions des débuts des technologies clés dans le vrai référentiel
        idx_techno_réel = []
        for i in range(len(technologie_clef)):
            print("i is ", str(i), " ====")
            # Si le type de financeur est dans le texte
            if technologie_clef[i][0:11] in data_techno_all[0]:
                print("True !")
                print(technologie_clef[i])
                # On cherche tous les positions où on trouve technologie_clef[i] dans data_techno_all[0]
                idx_techno_réel = idx_techno_réel + [match.start() for match in re.finditer(technologie_clef[i][0:9], data_techno_all[0])]
                print(idx_techno_réel)
        # On ordonne ensuite les indices
        idx_techno_réel = list(np.sort(idx_techno_réel))
        print(idx_techno_réel) 
        
        ## On y trouve les données
        # Indice fin
        idx_fin = len(data_techno_all[0])
        # Nombre ligne
        nb_ligne = int(np.round(len(idx_TRL)/6))
        print(nb_ligne)
        # 1ère donnée
        data_techno = []
        if nb_ligne != 1:
            # Premières lignes
            for i in range(nb_ligne-1) : 
                print("i is ", str(i))
                data_techno = data_techno + [data_techno_all[0][idx_TRL[0+i*6]:
                                                  idx_TRL[1+i*6]], # TRL départ
                               data_techno_all[0][idx_TRL[2+i*6]:
                                                  idx_TRL[3+i*6]], # TRL atteint cette année
                               data_techno_all[0][idx_TRL[4+i*6]:
                                                  idx_TRL[5+i*6]], # TRL d'arrivée visé
                               data_techno_all[0][idx_TRL[5+i*6]:
                                                  idx_techno_réel[1+i]], # Définition + technologie 
                               data_techno_all[0].replace("\n",espace_ou_non[i])[idx_techno[0+i*2]:
                                                                   idx_techno[1+i*2]], # techno clef
                                             ] 
                print(data_techno)
        # Dernière ligne
        print("i is ", str(nb_ligne))
        data_techno = data_techno + [data_techno_all[0][idx_TRL[0+(nb_ligne-1)*6]:
                                                        idx_TRL[1+(nb_ligne-1)*6]], # TRL départ
                                     data_techno_all[0][idx_TRL[2+(nb_ligne-1)*6]:
                                                        idx_TRL[3+(nb_ligne-1)*6]], # TRL atteint cette année
                                     data_techno_all[0][idx_TRL[4+(nb_ligne-1)*6]:
                                                        idx_TRL[5+(nb_ligne-1)*6]], # TRL d'arrivée visé
                                     data_techno_all[0][idx_TRL[5+(nb_ligne-1)*6]:
                                                        idx_fin], # Définition + technologie
                                     data_techno_all[0].replace("\n",espace_ou_non[nb_ligne-1])[idx_techno[0+(nb_ligne-1)*2]:
                                                                         idx_techno[1+(nb_ligne-1)*2]] # techno clef
                                      ] 
        print(data_techno) 
        
        # On nettoie le jeu de données
        # - on enlève les \n
        data_techno = [x.replace("\n"," ") for x in data_techno]
        # - on enlève les espaces au début et à la fin
        data_techno = [x.strip() for x in data_techno]
        print(data_techno) 
        
        # On divise par ligne
        data_techno = [data_techno[0+i*5:5+i*5] for i in range(nb_ligne)]
        
        # On trouve le numéro qui correspond à la technologie
        for i in range(nb_ligne) :
            print("i is " + str(i) + " ====")
            num_techno = int(technologie_clef_xlsx[technologie_clef_xlsx["Technologie"] == data_techno[i][4]]['Numéro'].values[0])
            data_techno[i].insert(4,num_techno)
        print(data_techno)
    
        # On convertie en dataframe
        data_techno = pd.DataFrame(data_techno)
        print(data_techno)
        #data_techno.to_excel(dir_Excel_output + "techno.xlsx", index=False)
    
    return(data_techno)


#%%%% ----- 8) Start-ups ------------------------------------------------------


## Start-up
def indic_startup(info_indic) :
    
    data_startup = info_indic[4]
    # On nettoie les données
    data_startup = [s.strip() for s in data_startup]
    print(data_startup)
    # On convertie en dataframe
    data_startup = pd.DataFrame(data_startup)
    # On précise que ce sont des startups
    #data_startup.insert(0,"categ","startup")
    print(data_startup)
    # On précise la catégorie
    data_startup.insert(0,"Type_ReportRST_ResultatsImpacts","Start-up")
    data_startup.insert(1,"Identification_ReportRST_ResultatsImpacts","SIRET")
    
    return(data_startup)



#%%%% ----- 9) Financements externes ------------------------------------------


## Financement externe
def indic_financ(info_indic) :

    data_financ_all = info_indic[5]
    print(data_financ_all)
    
    # Si rien n'est rempli :
    if "VIDE" in data_financ_all[0] and "Monétaire" not in data_financ_all[0] and "En nature" not in data_financ_all[0] :
        data_financ = data_financ_all[0].split()
        print(data_financ)
        # S'il n'y a pas assez de cases remplies, on en rajoute
        if len(data_financ) < 5 :
            add = 5 - len(data_financ)
            data_financ = data_financ + add*["VIDE"]
        # On convertie en dataframe
        data_financ = pd.DataFrame(data_financ)
        # On inverse les lignes et les colonnes
        data_financ = data_financ.T
        print(data_financ)
    
    else :
        type_financeur = ["PUBLIC-ANR",
                          "PUBLIC-COLLECTIVITES",
                          "PUBLIC-ADMINISTRATION",
                          "PUBLIC-AUTRES-ORGANISME",
                          "INTERNATIONAL-COMMISSION-EUROP",
                          "INTERNATIONAL-AUTRES",
                          "PRIVE-AUTRE"]
        type_financement = ["Monétaire",
                            "En nature : valorisation temps\npassé",
                            "En nature : autres"]
        
        # On souhaite y trouver les positions des débuts et fins des types de financeurs
        idx_financeur = []
        for i in range(len(type_financeur)):
            print("i is ", str(i))
            # Si le type de financeur est dans le texte
            if type_financeur[i] in data_financ_all[0]:
                print("True")
                # On cherche tous les positions où on trouve type_financeur[i] dans data_financ_all[0]
                idx_financeur_début = [match.start() for match in re.finditer(type_financeur[i], data_financ_all[0])]
                # On y rajoute la position de la fin du mot
                idx_financeur_i = []
                for elem in idx_financeur_début :
                    idx_financeur_i.append(elem)
                    idx_financeur_i.append(elem + len(type_financeur[i]))
                idx_financeur = idx_financeur + idx_financeur_i
                print(idx_financeur)
        # On ordonne ensuite les indices
        idx_financeur = list(np.sort(idx_financeur))
        print(idx_financeur) 
        
        # On souhaite y trouver les positions des débuts et fins des types de financements
        idx_financement = []
        for i in range(len(type_financement)):
            print("i is ", str(i))
            # Si le type de financement est dans le texte
            if type_financement[i] in data_financ_all[0]:
                print("True")
                # On cherche tous les positions où on trouve type_financement[i] dans data_financ_all[0]
                idx_financement_début = [match.start() for match in re.finditer(type_financement[i], data_financ_all[0])]
                # On y rajoute la position de la fin du mot
                idx_financement_i = []
                for elem in idx_financement_début :
                    idx_financement_i.append(elem)
                    idx_financement_i.append(elem + len(type_financement[i]))
                idx_financement = idx_financement + idx_financement_i
                print(idx_financement)
        # On ordonne ensuite les indices
        idx_financement = list(np.sort(idx_financement))
        print(idx_financement)
        
        # Position de fin
        if "Totaux" in data_financ_all[0] :
            idx_fin = data_financ_all[0].index("Totaux")
        else :
            idx_fin = len(data_financ_all[0])
        
        ## On y trouve les données
        # Nombre ligne
        nb_ligne = int(np.round(len(idx_financement)/2))
        # 1ère donnée
        data_financ = [data_financ_all[0][0:idx_financeur[0]]]
        # Premières lignes
        for i in range(nb_ligne-1) : 
            print("i is ", str(i)) 
            data_financ = data_financ + [data_financ_all[0][idx_financeur[0+i*2]:
                                                            idx_financeur[1+i*2]], #type financeur
                                         data_financ_all[0][idx_financeur[1+i*2]:
                                                            idx_financement[0+i*2]], # nom financeur
                                         data_financ_all[0][idx_financement[0+i*2]:
                                                            idx_financement[1+i*2]], # type financement
                                         data_financ_all[0][idx_financement[1+i*2]:
                                                              idx_financeur[2+i*2]].split("\n")[0], # montant     
                                         data_financ_all[0][idx_financement[1+i*2]:
                                                              idx_financeur[2+i*2]][len(data_financ_all[0][idx_financement[1+i*2]:
                                                                                   idx_financeur[2+i*2]].split("\n")[0]):len(data_financ_all[0][idx_financement[1+i*2]:
                                                                                                        idx_financeur[2+i*2]])], # etablissement coordinateur 
                                         ] 
            print(data_financ)
        # Dernière ligne
        print("i is ", str(nb_ligne-1))
        data_financ = data_financ + [data_financ_all[0][idx_financeur[0+(nb_ligne-1)*2]:
                                                        idx_financeur[1+(nb_ligne-1)*2]], #type financeur
                                     data_financ_all[0][idx_financeur[1+(nb_ligne-1)*2]:
                                                        idx_financement[0+(nb_ligne-1)*2]], # nom financeur
                                     data_financ_all[0][idx_financement[0+(nb_ligne-1)*2]:
                                                        idx_financement[1+(nb_ligne-1)*2]], # type financement
                                     data_financ_all[0][idx_financement[1+(nb_ligne-1)*2]:
                                                        idx_fin] # montant
                                     ] 
                      
        print(data_financ) 
        
        # On nettoie les données
        data_financ = [s.strip() for s in data_financ]
        # On enlève les \n au milieu du texte
        data_financ = [x.replace("\n"," ") for x in data_financ]
        # On divise les données 5 par 5
        data_financ = [data_financ[i*5:5+i*5] for i in range(nb_ligne)]
        print(data_financ)
        # On transforme en dataframe
        data_financ = pd.DataFrame(data_financ)
        print(data_financ)

    return(data_financ)



#%%%% ----- 10) Projets ERC ---------------------------------------------------


## Projets ERC
def indic_ERC(info_indic) :
    
    data_ERC = info_indic[6]
    data_ERC = data_ERC[0].split()
    
    # S'il n'y a pas assez de cases remplies car VIDE, on en rajoute
    if len(data_ERC) < 6 :
        
        add = 6 - len(data_ERC)
        data_ERC = data_ERC + add*["VIDE"]
        
    # Sinon on extrait la donnée
    else :
        
        # On remet la donnée à l'état initial
        data_ERC = info_indic[6]
        
        # On trouve l'emplacement de la case Retenu
        type_retenu = ["En cours\nd’évaluation",
                       "Oui",
                       "Non"]
        idx_retenu = []
        for i in range(len(type_retenu)):
            print("i is ", str(i))
            if type_retenu[i] in data_ERC[0]:
                j = i
                print(type_retenu[i])
                idx_retenu = idx_retenu + [re.search(type_retenu[i],data_ERC[0]).start()] + [re.search(type_retenu[i],data_ERC[0]).start() + len(type_retenu[i])]
        print(idx_retenu)
        
        # On trouve les nom prénom du chercheur
        data_ERC_split_début = data_ERC[0][0:idx_retenu[0]].split()
        prenom_ERC = data_ERC_split_début[-1]
        nom_ERC = data_ERC_split_début[-2]
        
        # On trouve l'emplacement du montant du financement obtenu
        if "VIDE" in data_ERC[0]:
            montant_ERC = "VIDE"
        else:
            montant_ERC = next(re.finditer(r'\d+', data_ERC[0]), None).group()
        
        
        # Et l'emplacement du lien du projet avec France 2030
        if "VIDE" in data_ERC[0]:
            lien_ERC = data_ERC[0][next(re.finditer('VIDE', data_ERC[0]), None).end():len(data_ERC[0])]
        else:
            lien_ERC = data_ERC[0][next(re.finditer(r'\d+', data_ERC[0]), None).end():len(data_ERC[0])]
        
        # Ainsi que le projet
        idx_nom = re.search(nom_ERC,data_ERC[0]).start()
        projet_ERC = data_ERC[0][0:idx_nom]
        
        data_ERC = [projet_ERC, 
                    nom_ERC, 
                    prenom_ERC, 
                    type_retenu[j], 
                    montant_ERC, 
                    lien_ERC]
        print(data_ERC)

    # On nettoie les données
    data_ERC = [x.strip() for x in data_ERC]
    # On enlève les \n au milieu du texte
    data_ERC = [x.replace("\n"," ") for x in data_ERC]
    print(data_ERC)
    
    # On convertie en dataframe
    data_ERC = pd.DataFrame(data_ERC)
    # On inverse les lignes et les colonnes
    data_ERC = data_ERC.T
    print(data_ERC)
    
    return(data_ERC)



#%%%% ----- 11) Ressources humaines et formation ------------------------------


## Ressource humaine et formation
def indic_RH(info_indic) :
    
    data_RH1 = info_indic[7]
    data_RH2 = info_indic[8]
    print(data_RH1)
    print(data_RH2)
    # On sépare par les espaces
    data_RH1 = data_RH1[0].split()
    data_RH2 = data_RH2[0].split()
    # On fusionne
    data_RH = data_RH1 + data_RH2
    # On transforme en nombre
    if "VIDE" not in data_RH :
        data_RH = [float(x) for x in data_RH]
    # On convertie en dataframe
    data_RH = pd.DataFrame(data_RH)
    # On inverse les lignes et les colonnes
    data_RH = data_RH.T
    print(data_RH)
    
    return(data_RH)



#%%%% ----- 12) Formations ----------------------------------------------------

def indic_formation(info_indic) :

    ## Formation
    data_formation1 = info_indic[9]
    data_formation2 = info_indic[10]
    data_formation3 = info_indic[11]
    data_formation4 = info_indic[12]
    data_formation5 = info_indic[13]
    data_formation6 = info_indic[14]
    data_formation7 = info_indic[15]
    data_formation8 = info_indic[16]
    data_formation9 = info_indic[17]
    data_formation10 = info_indic[18]
    data_formation11 = info_indic[19]
    # On sépare par les espaces
    data_formation1 = data_formation1[0].split()
    data_formation2 = data_formation2[0].split()
    data_formation3 = data_formation3[0].split()
    data_formation4 = data_formation4[0].split()
    data_formation5 = data_formation5[0].split()
    data_formation6 = data_formation6[0].split()
    data_formation7 = data_formation7[0].split()
    data_formation8 = data_formation8[0].split()
    data_formation9 = data_formation9[0].split()
    data_formation10 = data_formation10[0].split()
    data_formation11 = data_formation11[0].split()
    # On les fusionne
    data_formation = [data_formation1] + [data_formation2] + [data_formation3] + [data_formation4] + [data_formation5] + [data_formation6] + [data_formation7] + [data_formation8] + [data_formation9] + [data_formation10] + [data_formation11]
    # # On transforme en nombre
    # [[int(x[0]),int(x[1])] for x in data_formation]
    # On convertie en dataframe
    data_formation = pd.DataFrame(data_formation)
    # On y rajoute la colonne sur le détail de la formation
    data_formation.insert(0,
                     "Année_ReportRST_Formations",
                     ["1ère année Bac+2",
                      "2ème année Bac+2",
                      "1ère année Licence Bac+3",
                      "2ème année Licence Bac+3",
                      "3ème année Licence Bac+3",
                      "1ère année Master",
                      "2ème année Master",
                      "Université 1 an",
                      "1ère année université plus d'1 an",
                      "2ème année université plus d'1 an",
                      "3ème année université plus d'1 an"]
                     )
    # Les VIDES sont des 0
    data_formation.replace(to_replace = "VIDE",
                           value = 0,
                           inplace = True)
    print(data_formation)
    
    return(data_formation)



#%%%% ----- 13) Doctorats -----------------------------------------------------

## Doctorat
def indic_doct(info_indic) :
    
    data_doct = info_indic[20]
    data_doct = data_doct[0].split()
    print(data_doct)
    # S'il n'y a pas assez de cases remplies, on en rajoute
    if len(data_doct) < 6 :
        add = 6 - len(data_doct)
        data_doct = data_doct + add*["VIDE"]
    # On détermine le nombre de doctorant
    nb_doct = int(len(data_doct)/6)
    # On divise par doctorant
    data_doct = [data_doct[i*6:6+i*6] for i in range(nb_doct)]
    print(data_doct)
    # On convertie en dataframe
    data_doct = pd.DataFrame(data_doct)
    # On précise que ce sont des post-doctorants
    data_doct.insert(0,"DoctoratPostdoctorat_ReportRST_DocPostdoc","Doctorat")
    print(data_doct)
    
    return(data_doct)




#%%%% ----- 14) Post-doctorats ------------------------------------------------


## Post-doctorat
def indic_postdoc(info_indic) :
    
    # On extrait la table
    data_postdoc = info_indic[21]
    # On split avec l'espace entre
    data_postdoc = data_postdoc[0].split()
    print(data_postdoc)
    # On détermine le nombre de doctorant
    nb_postdoc = int(len(data_postdoc)/3)
    # On divise par doctorant
    data_postdoc = [data_postdoc[i*3:3+i*3] for i in range(nb_postdoc)]
    print(data_postdoc)
    # On convertie en dataframe
    data_postdoc = pd.DataFrame(data_postdoc)
    # On précise que ce sont des post-doctorants
    data_postdoc.insert(0,"DoctoratPostdoctorat_ReportRST_DocPostdoc","Post-doctorat")
    print(data_postdoc)
    
    return(data_postdoc)



#%%%% ----- 15) Projets de maturation / prématuration -------------------------


## Projets transférés vers des programmes de maturation / prématuration
def indic_matpremat(info_indic) :
    
    data_matpremat = info_indic[22]
    print(data_matpremat)
    # Nettoyage de la donnée
    data_matpremat[0] = data_matpremat[0].strip()
    # Transformation en dataframe
    data_matpremat = pd.DataFrame(data_matpremat)
    # On précise la catégorie
    data_matpremat.insert(0,"Type_ReportRST_ResultatsImpacts","Projets transférés programmes (Pré)maturation")
    data_matpremat.insert(1,"Identification_ReportRST_ResultatsImpacts","Nombre")
    
    return(data_matpremat)



#%%% ====== V/ FEUILLETS EXCEL ================================================
#%%%% ----- 1) Infos du projet ------------------------------------------------

## Feuillet ReportRST_InfosProjets
def xlsx_infoprojet(data_infoprojet) :
    
    data_infoprojet = data_infoprojet_indic
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_infoprojet = annee_PEPR_projet_NaN(data_infoprojet, annee, PEPR, projet)
    print(data_infoprojet)
    # On y renomme les colonnes
    data_infoprojet.rename(columns={data_infoprojet.columns[3]: 'DébutPériodeRapport_ReportRST_InfosProjets',
                                    data_infoprojet.columns[4]: 'FinPériodeRapport_ReportRST_InfosProjets',
                                    data_infoprojet.columns[5]: 'DateCAA_ReportRST_InfosProjets',
                                    data_infoprojet.columns[6]: 'Titre_ReportRST_InfosProjets',
                                    data_infoprojet.columns[7]: 'Mots-clés_ReportRST_InfosProjets',
                                    data_infoprojet.columns[8]: 'EtablissementCoordinateur_ReportRST_InfosProjets',
                                    data_infoprojet.columns[9]: 'DateDébutProjet_ReportRST_InfosProjets',
                                    data_infoprojet.columns[10]: 'DateFinProjet_ReportRST_InfosProjets',
                                    data_infoprojet.columns[11]: 'SiteWeb_ReportRST_InfosProjets',
                                    data_infoprojet.columns[12]: 'NomPrénomRST_ReportRST_InfosProjets',
                                    data_infoprojet.columns[13]: 'Tel_ReportRST_InfosProjets',
                                    data_infoprojet.columns[14]: 'Mail_ReportRST_InfosProjets',
                                    data_infoprojet.columns[15]: 'DateRédaction_ReportRST_InfosProjets',
                                    data_infoprojet.columns[16]: 'Résumé_ReportRST_InfosProjets',
                                    data_infoprojet.columns[17]: 'Activités_ReportRST_InfosProjets',
                                    data_infoprojet.columns[18]: 'MiseEnPlacePilotageSuivi_ReportRST_InfosProjets',
                                    data_infoprojet.columns[19]: 'RésultatsObtenus_ReportRST_InfosProjets',
                                    data_infoprojet.columns[20]: 'PersonnesMobilisées_ReportRST_InfosProjets',
                                    data_infoprojet.columns[21]: 'DiﬀusionRésultats_ReportRST_InfosProjets',
                                    data_infoprojet.columns[22]: 'ValorisationRésultatsStratPart_ReportRST_InfosProjets',
                                    data_infoprojet.columns[23]: 'ValorisationRésultatsTransfertTechnologie_ReportRST_InfosProjets',
                                    data_infoprojet.columns[24]: 'RayonnementEuropeInternational_ReportRST_InfosProjets',
                                    data_infoprojet.columns[25]: 'AutresImpacts_ReportRST_InfosProjets',
                                    data_infoprojet.columns[26]: '10TravauxMajeur_ReportRST_InfosProjets',
                                    data_infoprojet.columns[27]: 'ArticulationSNA_ReportRST_InfosProjets',
                                    data_infoprojet.columns[28]: 'ArticulationAutresProjetsPEPR_ReportRST_InfosProjets',
                                    data_infoprojet.columns[29]: 'ArticulationAutresFinancementsFrance2030_ReportRST_InfosProjets',
                                    data_infoprojet.columns[30]: 'RéponsesRecommandationsJury_ReportRST_InfosProjets',
                                    data_infoprojet.columns[31]: 'CommentairesLibres_ReportRST_InfosProjets',
                                    data_infoprojet.columns[32]: 'CommentairesLibres2_ReportRST_InfosProjets'}
                           ,inplace=True)
    print(data_infoprojet)
    
    return(data_infoprojet)



#%%%% ----- 2) Résultats impacts ----------------------------------------------


## Feuillet ReportRST_ResultatsImpacts
def xlsx_resultatimpact(data_brevet,data_dataset,data_logiciel,data_startup,data_matpremat) :
    
    # On rassemble les différents résultats
    data_resultatimpact = pd.concat([data_brevet,data_dataset,data_logiciel,data_startup,data_matpremat])
    print(data_resultatimpact)
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_resultatimpact = annee_PEPR_projet_NaN(data_resultatimpact, annee, PEPR, projet)
    print(data_resultatimpact)
    # On renomme la dernière colonne
    data_resultatimpact.rename(columns={data_resultatimpact.columns[5]: 'Description_ReportRST_ResultatsImpacts'}
                          ,inplace=True)
    print(data_resultatimpact)
    
    return(data_resultatimpact)


#%%%% ----- 3) Technologies ---------------------------------------------------


## Feuillet ReportRST_TRL
def xlsx_techno(data_techno) :
    
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_techno = annee_PEPR_projet_NaN(data_techno, annee, PEPR, projet)
    print(data_techno)
    # On y rajoute les noms de colonnes nécessaires
    data_techno.rename(columns={data_techno.columns[3]: 'TRLDépart_ReportRST_TRL',
                                data_techno.columns[4]: 'TRLAtteintAnnéeCollecte_ReportRST_TRL',
                                data_techno.columns[5]: 'TRLArrivéeVisé_ReportRST_TRL',
                                data_techno.columns[6]: 'DefTechnologiesProduites_ReportRST_TRL',
                                data_techno.columns[7]: 'NuméroCatégorie_ReportRST_TRL',
                                data_techno.columns[8]: 'DescriptionCatégorie_ReportRST_TRL'}
                       ,inplace=True)
    print(data_techno)
    
    return(data_techno)


#%%%% ----- 4) Financements externes ------------------------------------------

## Feuillet ReportRST_Financements
def xlsx_financ(data_financ) : 
    
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_financ = annee_PEPR_projet_NaN(data_financ, annee, PEPR, projet)
    print(data_financ)
    # On y renomme les colonnes
    data_financ.rename(columns={data_financ.columns[3]: 'Etablissement_ReportRST_Financements',
                                    data_financ.columns[4]: 'TypeFinanceur_ReportRST_Financements',
                                    data_financ.columns[5]: 'NomFinanceur_ReportRST_Financements',
                                    data_financ.columns[6]: 'TypeFinancement_ReportRST_Financements',
                                    data_financ.columns[7]: 'Montant_ReportRST_Financements'}
                           ,inplace=True)
    print(data_financ)
    
    return(data_financ)



#%%%% ----- 5) Projets ERC ----------------------------------------------------


## Feuillet ReportRST_ERC
def xlsx_ERC(data_ERC) :
    
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_ERC = annee_PEPR_projet_NaN(data_ERC, annee, PEPR, projet)
    print(data_ERC)
    # On y renomme les colonnes
    data_ERC.rename(columns={data_ERC.columns[3]: 'Projet_ReportRST_ERC',
                             data_ERC.columns[4]: 'NomChercheur_ReportRST_ERC',
                             data_ERC.columns[5]: 'PrénomChercheur_ReportRST_ERC',
                             data_ERC.columns[6]: 'Retenu_ReportRST_ERC',
                             data_ERC.columns[7]: 'MontantFinancement_ReportRST_ERC',
                             data_ERC.columns[8]: 'LienProjets_ReportRST_ERC'}
                    ,inplace=True)
    print(data_ERC)
    
    return(data_ERC)



#%%%% ----- 6) Ressources humaines et formation -------------------------------

## Feuillet ReportRST_RH
def xlsx_RH(data_RH) :
    
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_RH = annee_PEPR_projet_NaN(data_RH, annee, PEPR, projet)
    print(data_RH)
    # On y rajoute les noms de colonnes nécessaires
    data_RH.rename(columns={data_RH.columns[3]: 'EC/C-PersPhysique_ReportRST_RH',
                            data_RH.columns[4]: 'EC/C-Femmes_ReportRST_RH',
                            data_RH.columns[5]: 'EC/C-ETPT_ReportRST_RH',
                            data_RH.columns[6]: 'ITA-PersPhysique_ReportRST_RH',
                            data_RH.columns[7]: 'ITA-Femmes_ReportRST_RH',
                            data_RH.columns[8]: 'ITA-ETPT_ReportRST_RH'}
                   ,inplace=True)
    print(data_RH)
    
    return(data_RH)


#%%%% ----- 7) Formation ------------------------------------------------------


## Feuillet ReportRST_Formations
def xlsx_formation(data_formation) :
    
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_formation = annee_PEPR_projet_NaN(data_formation, annee, PEPR, projet)
    print(data_formation)
    # On y renomme les colonnes
    data_formation.rename(columns={data_formation.columns[4]: 'NombreInscrits_ReportRST_Formations',
                                   data_formation.columns[5]: 'NombreFemmes_ReportRST_Formations'}
                          ,inplace=True)
    print(data_formation)
    
    return(data_formation)



#%%%% ----- 8) Doctorats et post-doctorats ------------------------------------


## Feuillet ReportRST_DocPostdoc
def xlsx_docpostdoc(data_doct,data_postdoc) :
    
    # On rassemble doctorants et postdoctorants
    data_docpostdoc = pd.concat([data_doct,data_postdoc])
    # On y met année, AcronymePEPR, et AcronymeProjet et les NaN
    data_docpostdoc = annee_PEPR_projet_NaN(data_docpostdoc, annee, PEPR, projet)
    print(data_docpostdoc)
    # On y renomme les colonnes
    data_docpostdoc.rename(columns={data_docpostdoc.columns[4]: 'Nom(Post)doctorant_ReportRST_DocPostdoc',
                                    data_docpostdoc.columns[5]: 'Prénom(Post)doctorant_ReportRST_DocPostdoc',
                                    data_docpostdoc.columns[6]: 'NuméroORCID_ReportRST_DocPostdoc',
                                    data_docpostdoc.columns[7]: 'BourseCIFREDoct_ReportRST_DocPostdoc',
                                    data_docpostdoc.columns[8]: 'NomPartenaireDoct_ReportRST_DocPostdoc',
                                    data_docpostdoc.columns[9]: 'SIRETPartenaireDoct_ReportRST_DocPostdoc'}
                           ,inplace=True)
    print(data_docpostdoc)
    
    return(data_docpostdoc)





#%% ====================== VARIABLES ==========================================
#%%% ====== I/ CHOOSE THE DIRECTORIES =========================================


## Directory de l'Excel en output
dir_Excel_output = "C:/Users/mjoigneau/Nextcloud/MyDrive/3_Françoise/4 - Système d'information décisionnel/2 - Extraction données PDF reporting projets/Excel en output/"
nom_Excel_exemple = "Restitutions_PEPR_PDF_2024.xlsx"
dir_Excel_exemple = dir_Excel_output + nom_Excel_exemple
print(dir_Excel_exemple)


## Directory de l'Excel PEPR Projets
dir_PEPR_projets = "C:/Users/mjoigneau/Nextcloud/MyDrive/3_Françoise/4 - Système d'information décisionnel/2 - Extraction données PDF reporting projets/code/PEPR_projets.xlsx"
print(dir_PEPR_projets)

# Directory de l'Excel Technologies clefs
dir_techno = "C:/Users/mjoigneau/Nextcloud/MyDrive/3_Françoise/4 - Système d'information décisionnel/2 - Extraction données PDF reporting projets/code/Liste_technologies.xlsx"

# Directory du PDF à extraire
dir_PDF_base = "C:/Users/mjoigneau/Nextcloud/MyDrive/3_Françoise/4 - Système d'information décisionnel/2 - Extraction données PDF reporting projets/PDF 2024 en input/"



#%%% ====== II/ MOTS CLES POUR SEPARER TEXTE ==================================

## Séparateurs des textes des mots-clés
sep_key = ["\n", " "]


#%%%% ----- 1) Informations du projet -----------------------------------------

## On met toutes les possibilités pour les mots clés
keytous_responsable = sep_keywords(
    ["RESPONSABLE SCIENTIFIQUE ET TECHNIQUE DU PROJET,",
     "REDACTEUR DU PRESENT RAPPORT",
     "Nom, Prénom"],
    sep_key
    )
keytous_resume1 = sep_keywords(
    ["RESUME PUBLIC / PUBLIC SUMMARY",
     "Résumé public et diﬀusable",
     "Ce résumé sera mis en ligne sur le site de l’ANR.",
     "Il doit être compréhensible par un public non-expert d’une part et clair sur les objectifs initiaux,",
     "les activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement",
     "atteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés",
     "rencontrées d’autre part.",
     "L’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement",
     "du projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année",
     "écoulée mais d’actualiser les informations.",
     "Maximum 2300 caractères"],
    sep_key
    )
keytous_resume2 = sep_keywords(
    ["RESUME PUBLIC / PUBLIC SUMMARY",
     "Résumé public et diﬀusable",
     "Ce résumé sera mis en ligne sur le site de l’ANR.",
     "Il doit être compréhensible par un public non-expert d’une part et clair sur les objectifs initiaux,",
     "les activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement",
     "atteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés",
     "rencontrées.",
     "L’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement",
     "du projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année",
     "écoulée mais d’actualiser les informations.",
     "Maximum 2300 caractères"],
    sep_key
    )
keytous_resume3 = sep_keywords(
    ["RESUME PUBLIC / PUBLIC SUMMARY",
     "Résumé public et diﬀusable",
     "Ce résumé sera mis en ligne sur le site de l’ANR.",
     "Il doit être compréhensible par un public non-expert.  Il doit être clair sur les objectifs initiaux,",
     "les activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement",
     "atteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés",
     "rencontrées.",
     "L’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement",
     "du projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année",
     "écoulée mais d’actualiser les informations.",
     "Maximum 2300 caractères"],
    sep_key)
keytous_activite = sep_keywords(
    ["ACTIVITÉS",
     "Activités du projet pour la période de collecte",
     "Présenter toutes les activités conduites pour la période de collecte : embauches, évènements,",
     "avancées majeures, valorisation, etc.",
     "Maximum 1100 caractères"],
    sep_key
    )
keytous_articulation = sep_keywords(
    ["Articulation avec d’autres ﬁnancements France 2030",
     "Indiquer comment ce projet interagit et s’articule avec d’autres projets ﬁnancés par France",
     "2030 (hors projets de ce PEPR) en termes d’actions, de projets, de relations partenariales, de",
     "mutualisations de moyens, etc.",
     "Maximum 4500 caractères"],
    sep_key
    )
keytous_comment = sep_keywords(
    ["COMMENTAIRES LIBRES SUR LES INFORMATIONS FOURNIES",
     "Commentaires libres",
     "Des commentaires sont attendus sur les informations que vous avez fournies en indiquant",
     "notamment les indicateurs pour lesquels les informations sont des estimations et le niveau de",
     "précision de ces estimations.",
     "Maximum 4500 caractères"],
    sep_key
    )


## On sépare les mots clés en plusieurs parties
part1general = [
    #PART 1 : INFORMATIONS SUR LE PROJET"
    ["Acronyme du projet"],
    ["Rapport couvrant la période du"],
    ["au"], # ATTENTION !
    ["Date de notiﬁcation du contrat attributif d’aide"],
    ["Titre complet du projet"],
    ["Mots clés"],
    ["Etablissement coordinateur"],
    ["Date de début du projet"],
    ["Date de ﬁn du projet"],
    ["Site web du projet"],
    
    # PART 2 : RESPONSABLE SCIENTIFIQUE ET TECHNIQUE DU PROJET
    #, REDACTEUR DU PRESENT RAPPORT
    #"RESPONSABLE SCIENTIFIQUE ET TECHNIQUE DU PROJET",
    #"Nom, Prénom",
    ["RESPONSABLE SCIENTIFIQUE ET TECHNIQUE DU PROJET,\nREDACTEUR DU PRESENT RAPPORT\nNom, Prénom"] + keytous_responsable,
    ["Téléphone :"],
    ["Courriel"],
    ["Date de rédaction"],
    
    # PART 3 : RESUME PUBLIC / PUBLIC SUMMARY
    # "RESUME PUBLIC / PUBLIC SUMMARY",
    # "Résumé public et diffusable",
    # "RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable",
    # "Maximum 2300 caractères",
    ["RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable\nCe résumé sera mis en ligne sur le site de l’ANR. Il doit être compréhensible par un public non-expert d’une part et clair sur les objectifs initiaux,\nles activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement\natteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés\nrencontrées d’autre part.\nL’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement\ndu projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année\nécoulée mais d’actualiser les informations.\nMaximum 2300 caractères",
      "RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable Ce résumé sera mis en ligne sur le site de l’ANR.\nIl doit être compréhensible par un public non-expert d’une part et clair sur les objectifs initiaux,\nles activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement\natteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés\nrencontrées d’autre part.\nL’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement\ndu projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année\nécoulée mais d’actualiser les informations.\nMaximum 2300 caractères",
      # (Différence 2024)
      "RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable\nCe résumé sera mis en ligne sur le site de l’ANR. Il doit être compréhensible par un public non-expert.  Il doit être clair sur les objectifs initiaux,\nles activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement\natteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés\nrencontrées.\nL’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement\ndu projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année\nécoulée mais d’actualiser les informations.\nMaximum 2300 caractères",
      "RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable Ce résumé sera mis en ligne sur le site de l’ANR.\nIl doit être compréhensible par un public non-expert.  Il doit être clair sur les objectifs initiaux,\nles activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement\natteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés\nrencontrées.\nL’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement\ndu projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année\nécoulée mais d’actualiser les informations.\nMaximum 2300 caractères",
      "RESUME PUBLIC / PUBLIC SUMMARY\nRésumé public et diﬀusable\nCe résumé sera mis en ligne sur le site de l’ANR.\nIl doit être compréhensible par un public non-expert.  Il doit être clair sur les objectifs initiaux,\nles activités conduites pour atteindre les résultats attendus, les résultats eﬀectivement\natteints, les réussites scientiﬁques, technologiques, économiques, etc. et les diﬃcultés\nrencontrées.\nL’idée du résumé est donc d’actualiser les informations présentes en fonction de l’avancement\ndu projet. Il ne s’agit donc pas de produire un rapport des activités conduites pour l’année\nécoulée mais d’actualiser les informations.\nMaximum 2300 caractères"] + keytous_resume1 + keytous_resume2 + keytous_resume3,
    
    # PART 4 : ACTIVITES
    # "ACTIVITÉS",
    # "Activités du projet pour la période de collecte",
    # "Maximum 1100 caractères",
    ["ACTIVITÉS Activités du projet pour la période de collecte\nPrésenter toutes les activités conduites pour la période de collecte : embauches, évènements,\navancées majeures, valorisation, etc.\nMaximum 1100 caractères",
      "ACTIVITÉS\nActivités du projet pour la période de collecte\nPrésenter toutes les activités conduites pour la période de collecte : embauches, évènements,\navancées majeures, valorisation, etc.\nMaximum 1100 caractères",
      "ACTIVITÉS\nActivités du projet pour la période de collecte\nPrésenter toutes les activités conduites pour la période de collecte : embauches, évènements,\navancées majeures, valorisation, etc. Maximum 1100 caractères",
      "ACTIVITÉS\nActivités du projet pour la période de collecte Présenter toutes les activités conduites pour la période de collecte : embauches, évènements,\navancées majeures, valorisation, etc.\nMaximum 1100 caractères",
      "ACTIVITÉS\nActivités du projet pour la période de collecte\nPrésenter toutes les activités conduites pour la période de collecte : embauches, évènements, avancées majeures, valorisation, etc.\nMaximum 1100 caractères"] + keytous_activite
    
    ]
    

part2_nonsimplifie = [
    
    # PARR 5 : ETAT D'AVANCEMENT DU PROJET
    # Mise en place, pilotage, suivi
    ["ETAT D’AVANCEMENT DU PROJET / PROGRESS OF THE PROJECT\nIl s’agit de la partie majeure du compte-rendu scientifique annuel. Chacun de ces paragraphes est à\nactualiser chaque année. Décrire ici l’état d’avancement du projet par rapport au contenu du contrat\net de ses annexes sur les différents volets. Mentionner les difficultés rencontrées, l’avancement des\ntravaux, les réorientations éventuelles, les perspectives pour l’année à venir, etc.\nMise en place / Pilotage / Suivi\nDécrire les conditions de lancement, les modalités de pilotage, les dispositifs de suivis mis en\nplace, etc.\nMaximum 1100 caractères",
     "ETAT D’AVANCEMENT DU PROJET / PROGRESS OF THE PROJECT\nIl s’agit de la partie majeure du compte-rendu scientifique annuel. Chacun de ces paragraphes est à\nactualiser chaque année. Décrire ici l’état d’avancement du projet par rapport au contenu du contrat\net de ses annexes sur les différents volets. Mentionner les difficultés rencontrées, l’avancement des\ntravaux, les réorientations éventuelles, les perspectives pour l’année à venir, etc.\nMise en place / Pilotage / Suivi Décrire les conditions de lancement, les modalités de pilotage, les dispositifs de suivis mis en\nplace, etc.\nMaximum 1100 caractères"],
    # Résultats obtenus dans l'année
    ["Résultats obtenus dans l’année\nLister, pour chaque work package, l’ensemble des avancées, des jalons et des livrables\nprogrammés pour l’année écoulée et qui ont été réalisés, abandonnés, ou modiﬁés.\nPréciser les facteurs et les contraintes justiﬁant les écarts par rapport à la proposition initiale.\nMaximum 9000 caractères",
     "Résultats obtenus dans l’année\nLister, pour chaque work package, l’ensemble des avancées, des jalons et des livrables programmés pour l’année écoulée et qui ont été réalisés, abandonnés, ou modiﬁés.\nPréciser les facteurs et les contraintes justiﬁant les écarts par rapport à la proposition initiale.\nMaximum 9000 caractères"],
    
    # PARTIES 6-7-8 : FICHIERS ET MOYENS HUMAINS
    # Fichier illustrant l'avancement du projet
    # Diagramme GANTT
    # Moyens humains
    ['''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être\njoints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous. \nDIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous.  MOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     # (Différence année 2024)
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être\njoints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous.  DIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous. \n MOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être\njoints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous. \nDIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous. \n MOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être joints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous. \nDIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous.  MOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être joints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous. \nDIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous.  MOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être\njoints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous.  DIAGRAMME DE GANTT *Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le\nﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous. \nMOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.''',
     '''FICHIERS ILLUSTRANT L\'AVANCEMENT DU PROJET\n*Aﬁn d\'illustrer l\'avancement du projet, 4 ﬁchiers en format .jpg peuvent être\njoints. Charger chaque ﬁchier (un par un) en cliquant sur le lien " Envoyer des\nﬁchiers " ci-dessous. \nDIAGRAMME DE GANTT\n*Aﬁn d\'illustrer l\'avancement du projet, merci de joindre obligatoirement le\ndiagramme de GANTT actualisé présentant l\'avancement du projet. Charger le ﬁchier (au format .jpg) en cliquant sur le lien " Envoyer des ﬁchiers " ci-dessous. \nMOYENS HUMAINS / HUMAN RESOURCES\nIl est recommandé d’effectuer un suivi annuel des emplois (nombre d’enseignants chercheurs,\nchercheurs, post doctorants, doctorants, administratifs, ingénieurs et techniciens). Ce suivi sera\ndemandé dans le cadre du rapport final afin de documenter l’adéquation entre l’atteinte des objectifs\net les moyens mobilisés.\nPersonnes mobilisées\nPrésenter le rôle et l’activité de l’équipe-projet dont le chef de projet. \nPrésenter le rôle des personnes hors équipe-projet mobilisées dans le cadre du projet (sans les\nnommer) dans les catégories suivantes : professeurs, directeurs de recherche, enseignants-\nchercheurs, chargés de recherche, ingénieurs et techniciens de recherche et de formation,\npostdoc, doctorants, étudiants en master, etc. \nIndiquer succinctement la nature de leurs interactions avec le projet : gouvernance, mise en\nœuvre, formation, etc. \nDes informations quantitatives sont demandées plus loin dans le rapport. Sont attendus ici des\néléments qualitatifs.'''],
    
    # PARTIE 9 : IMPACT DU PROJET
    # Diffusion des résultats
    ["IMPACT DU PROJET / PROJECT IMPACT\nDécrire tous les impacts du projet.\nDiﬀusion des résultats\nDécrire les actions de communication scientiﬁque : participations à des congrès, événements\ngrand public, etc. Mettre en avant des points remarquables et en indiquer les raisons (notoriété\nde l’événement, gain de visibilité pour le projet, etc.).\nMaximum 3400 caractères",
     "IMPACT DU PROJET / PROJECT IMPACT\nDécrire tous les impacts du projet.Diﬀusion des résultats\nDécrire les actions de communication scientiﬁque : participations à des congrès, événements\ngrand public, etc. Mettre en avant des points remarquables et en indiquer les raisons (notoriété\nde l’événement, gain de visibilité pour le projet, etc.).\nMaximum 3400 caractères",
     # (Différence année 2024)
     "IMPACT DU PROJET / PROJECT IMPACT\nDécrire tous les impacts du projet.\nDiﬀusion des résultats\nDécrire les actions de communication scientiﬁque : participations à des congrès, événements\ngrand public, etc. Mettre en avant des points remarquables et indiquer les raisons qui font\nqu'ils sont remarquables (notoriété de l’événement, gain de visibilité pour le projet, etc.).\nMaximum 3400 caractères",
     "IMPACT DU PROJET / PROJECT IMPACT\nDécrire tous les impacts du projet.\nDiﬀusion des résultats Décrire les actions de communication scientiﬁque : participations à des congrès, événements\ngrand public, etc. Mettre en avant des points remarquables et indiquer les raisons qui font\nqu'ils sont remarquables (notoriété de l’événement, gain de visibilité pour le projet, etc.).\nMaximum 3400 caractères"],
    # Actions entreprises pour favoriser la valorisation des résultats en lien avec la stratégie initiale et partenariats établis
    ["Actions entreprises pour favoriser la valorisation des résultats en lien avec la\nstratégie initiale et partenariats établis\nEtat d’avancement des actions conduites en matière de coordination avec les structures de\nvalorisation, de mise en œuvre des règles de partage et de gestion de la propriété\nintellectuelle.\nMaximum 3400 caractères"],
    # Valorisation des résultats et actions de transfert de technologie
    ["Valorisation des résultats et actions de transfert de technologie\nDéclarations d’invention, brevets, logiciels, savoir-faire, certiﬁcats d’obtention végétale,\nenveloppes SOLEAU, dépôts à l’Agence pour la protection des programmes, prototypes,\nlicences, cessions de licence d’exploitation, créations d’entreprise ou essaimages, thèses CIFRE\nou en codirection avec un acteur socio-économique, mise en œuvre de plateforme hors projet\nciblé (préciser la forme et le ﬁnancement).\nIndiquer en quoi les titres de propriété intellectuelle s’articulent avec les portefeuilles des\nacteurs. Des informations détaillées sur certains titres de PI seront demandées plus loin dans le\nrapport. Sont attendus ici des éléments qualitatifs.\nMaximum 3400 caractères",
     "Valorisation des résultats et actions de transfert de technologie\nDéclarations d’invention, brevets, logiciels, savoir-faire, certiﬁcats d’obtention végétale,\nenveloppes SOLEAU, dépôts à l’Agence pour la protection des programmes, prototypes,\nlicences, cessions de licence d’exploitation, créations d’entreprise ou essaimages, thèses CIFRE\nou en codirection avec un acteur socio-économique, mise en œuvre de plateforme hors projet\nciblé (préciser la forme et le ﬁnancement).\nIndiquer en quoi les titres de propriété intellectuelle s’articulent avec les portefeuilles des\nacteurs. Des informations détaillées sur certains titres de PI seront demandées plus loin dans le rapport. Sont attendus ici des éléments qualitatifs.\nMaximum 3400 caractères"],
    # Rayonnement aux niveaux européen et international
    ["Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de\ntravail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des\ninstances européennes, et les résultats découlant de ces démarches. .\nMaximum 2300 caractères",
     "Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de travail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des\ninstances européennes, et les résultats découlant de ces démarches. .\nMaximum 2300 caractères",
     "Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de travail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des\ninstances européennes, et les résultats découlant de ces démarches. .\nMaximum 2300 caractères",
     "Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de\ntravail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des\ninstances européennes, et les résultats découlant de ces démarches.\nMaximum 2300 caractères",
     # (Différence année 2024)
     "Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de\ntravail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des instances européennes, et les résultats découlant de ces démarches.\nMaximum 2300 caractères",
     "Rayonnement aux niveaux européen et international\nDécrire les actions engagées pour assurer le rayonnement international du projet : interactions\navec des acteurs, des structures ou des projets à l’étranger, mise en place de relations de\ntravail, recherche, valorisation, industrialisation, etc.\nPréciser également les activités conduites pour porter la thématique du projet au niveau des\ninstances européennes, et les résultats découlant de ces démarches. . Maximum 2300 caractères"],
    # Autres impacts
    ["Autres Impacts\nDécrire les autres impacts du projet : socio-culturels, socio-économiques, environnementaux,\nsanitaires et sociaux. Maximum 4500 caractères",
     "Autres Impacts\nDécrire les autres impacts du projet : socio-culturels, socio-économiques, environnementaux,\nsanitaires et sociaux.\nMaximum 4500 caractères"],
    
    # PARTIE 10 : LISTE DES 10 TRAVAUX MAJEURS
    ["LISTE DES 10 TRAVAUX MAJEURS ISSUS DU PROJET ET PUBLIES\nDANS L’ANNEE\nRenseigner jusqu’à 10 travaux majeurs\nParmi toute la production du projet au cours de l’année écoulée, lister 10 travaux majeurs en\njustiﬁant votre choix, par exemple : avancée scientiﬁque, fort impact sur la communauté\nscientiﬁque, diﬀusion auprès des décideurs publics, visibilité auprès du grand public, production\nde jeux de données ou de code réutilisés par des tiers, nouveau protocole, norme ou standard\ntechnique, etc.\nDans la mesure du possible, indiquer la date de publication ainsi qu’un identiﬁant pérenne (e.g.\nDOI).\nIl est attendu que les informations relatives aux publications soient déposées sur HAL (voir\nvade-mecum).\nMaximum 4500 caractères",
     "LISTE DES 10 TRAVAUX MAJEURS ISSUS DU PROJET ET PUBLIES\nDANS L’ANNEE\nRenseigner jusqu’à 10 travaux majeurs\nParmi toute la production du projet au cours de l’année écoulée, lister 10 travaux majeurs en\njustiﬁant votre choix, par exemple : avancée scientiﬁque, fort impact sur la communauté\nscientiﬁque, diﬀusion auprès des décideurs publics, visibilité auprès du grand public, production\nde jeux de données ou de code réutilisés par des tiers, nouveau protocole, norme ou standard\ntechnique, etc.\nDans la mesure du possible, indiquer la date de publication ainsi qu’un identiﬁant pérenne (e.g.\nDOI).\nIl est attendu que les informations relatives aux publications soient déposées sur HAL (voir vade-mecum).\nMaximum 4500 caractères",
     "LISTE DES 10 TRAVAUX MAJEURS ISSUS DU PROJET ET PUBLIES\nDANS L’ANNEE\nRenseigner jusqu’à 10 travaux majeurs\nParmi toute la production du projet au cours de l’année écoulée, lister 10 travaux majeurs en\njustiﬁant votre choix, par exemple : avancée scientiﬁque, fort impact sur la communauté\nscientiﬁque, diﬀusion auprès des décideurs publics, visibilité auprès du grand public, production\nde jeux de données ou de code réutilisés par des tiers, nouveau protocole, norme ou standard\ntechnique, etc.\nDans la mesure du possible, indiquer la date de publication ainsi qu’un identiﬁant pérenne (e.g.\nDOI).\nIl est attendu que les informations relatives aux publications soient déposées sur HAL (voir\nvade-mecum). Maximum 4500 caractères"],
    
    ]

part3_SNA = [
    
    # PARTIE 11 : ARTICULATION DU PROJET AVEC D’AUTRES FINANCEMENTS FRANCE 2030
    "ARTICULATION DU PROJET AVEC D’AUTRES FINANCEMENTS\nFRANCE 2030\nArticulation du projet avec la stratégie nationale\nDécrire les articulations du projet avec la stratégie nationale\nMaximum 4500 caractères"
    ]


part4_nonsimplifie = [
    
    # PARTIE 12 : ARTICULATION DU PROJET AVEC D’AUTRES FINANCEMENTS FRANCE 2030
    # Articulation du projet avec les autres projets de ce PEPR
    ["ARTICULATION DU PROJET AVEC D’AUTRES FINANCEMENTS\nFRANCE 2030\nArticulation du projet avec les autres projets de ce PEPR\nDécrire les articulations du projet avec d’autres projets ﬁnancés dans le cadre du PEPR\nMaximum 4500 caractères",
     # (Différence 2024)
     "ARTICULATION DU PROJET AVEC D’AUTRES FINANCEMENTS\nFRANCE 2030\nArticulation du projet avec les autres projets du PEPR\nDécrire les articulations du projet avec les autres projets de ce PEPR\nMaximum 4500 caractères",
     "Articulation du projet avec les autres projets de ce PEPR\nDécrire les articulations du projet avec d’autres projets ﬁnancés dans le cadre de ce PEPR\nMaximum 4500 caractères"],
    # Articulation avec d'autres financements France 2030
    ["Articulation avec d’autres ﬁnancements France 2030 Indiquer comment ce projet interagit et s’articule avec d’autres projets ﬁnancés par France\n2030 (hors projets de ce PEPR) en termes d’actions, de projets, de relations partenariales, de\nmutualisations de moyens, etc.\nMaximum 4500 caractères",
     "Articulation avec d’autres ﬁnancements France 2030\nIndiquer comment ce projet interagit et s’articule avec d’autres projets ﬁnancés par France\n2030 (hors projets de ce PEPR) en termes d’actions, de projets, de relations partenariales, de\nmutualisations de moyens, etc.\nMaximum 4500 caractères",
     "Articulation avec d’autres ﬁnancements France 2030\nIndiquer comment ce projet interagit et s’articule avec d’autres projets ﬁnancés par France\n2030 (hors projets de ce PEPR) en termes d’actions, de projets, de relations partenariales, de\nmutualisations de moyens, etc. Maximum 4500 caractères",
     "Articulation avec d’autres ﬁnancements France 2030\nIndiquer comment ce projet interagit et s’articule avec d’autres projets ﬁnancés par France\n2030 ( hors projets de ce PEPR ) en termes d’actions, de projets, de relations partenariales, de\nmutualisations de moyens, etc.\nMaximum 4500 caractères"] + keytous_articulation,
    
    # PARTIE 13 : EVALUATION
    ["EVALUATION\nRéponses aux recommandations du jury\nEn cas d’évaluation depuis le dernier rapport, mentionner les dispositions prises par le projet en\nréponse aux recommandations émises par le jury lors de l’évaluation.\nDans le cas contraire, indiquer « sans objet ».\nMaximum 4500 caractères",
     "EVALUATION\nRéponses aux recommandations du jury\nEn cas d’évaluation depuis le dernier rapport, mentionner les dispositions prises par le projet en\nréponse aux recommandations émises par le jury lors de l’évaluation.\nDans le cas contraire, indiquer « sans objet ». Maximum 4500 caractères"],
    
    # PARTIE 14 : COMMENTAIRES LIBRES
    ["COMMENTAIRES LIBRES / FREE COMMENTS\nCes commentaires libres peuvent inclure des commentaires sur le projet lui-même\net sa trajectoire, sur les indicateurs fournis, sur les aspects ﬁnanciers...\nIls peuvent également porter sur les interactions entre le projet et l’ANR ou sur les modalités de\ncollecte d’information. Ces informations sur la collecte sont de première importance pour\naméliorer les instructions qui sont fournies et simpliﬁer les collectes à venir.\nMaximum 4500 caractères"]
    ]

part5_general = [
    
    # PART 15 : INDICATEURS COMMUNS FRANCE 2030
    ["INDICATEURS COMMUNS FRANCE 2030"],
    
    # PART 16 : COMMENTAIRES LIBRES2
    ["COMMENTAIRES LIBRES SUR LES INFORMATIONS FOURNIES\nCommentaires libres Des commentaires sont attendus sur les informations que vous avez fournies en indiquant\nnotamment les indicateurs pour lesquels les informations sont des estimations et le niveau de\nprécision de ces estimations.\nMaximum 4500 caractères",
      "COMMENTAIRES LIBRES SUR LES INFORMATIONS FOURNIES\nCommentaires libres\nDes commentaires sont attendus sur les informations que vous avez fournies en indiquant\nnotamment les indicateurs pour lesquels les informations sont des estimations et le niveau de\nprécision de ces estimations.\nMaximum 4500 caractères"] + keytous_comment,
    ["VALIDATION"]
    
    ]



## Préparation des mots clés rassemblés selon le scénario
keywords_info = part1general + part5_general
keywords_info_complet = part1general + part2_nonsimplifie + part4_nonsimplifie + part5_general
keywords_info_complet_SNA = part1general + part2_nonsimplifie + part3_SNA + part4_nonsimplifie + part5_general



#%%%% ----- 2) Indicateurs du projet ------------------------------------------



## On met toutes les possibilités pour les mots clés
keytous_codesource = sep_keywords(
    ["Codes sources et logiciels",
     "URL, SWHID ou DOI du logiciel déposé rattaché au projet"],
    sep_key
    )
keytous_techno = sep_keywords(
    ["Technologies issues des projets",
     "Technologie",
     "CléTRL de",
     "départ",
     "déﬁni au",
     "début",
     "du",
     "projetTRL atteint",
     "l'année de",
     "la",
     "collecteTRL d'arrivée",
     "visé",
     "au",
     "moment",
     "du",
     "lancement",
     "du",
     "projetDéﬁnir plus précisément",
     "les",
     "technologies",
     "produites"],
    sep_key
    )
keytous_financ = sep_keywords(
    ["Financement externe :",
     "Etablissement",
     "(coordinateur",
     "ou",
     "partenaire*) ayant",
     "perçu",
     "le",
     "ﬁnancement",
     "externeType de",
     "ﬁnanceur ** Nom du",
     "ﬁnanceurType de",
     "ﬁnancement",
     "(monétaire, non",
     "monétaire : en",
     "nature)Montant",
     "perçu",
     "pendant",
     "l’année (€)"],
    sep_key
    )
keytous_financ2 = sep_keywords(
    ["Financement externe :",
     "Etablissement",
     "(coordinateur",
     "ou",
     "partenaire*) ayant",
     "perçu",
     "le",
     "ﬁnancement",
     "externeType de",
     "ﬁnanceur **Nom du",
     "ﬁnanceurType de",
     "ﬁnancement",
     "(monétaire, non",
     "monétaire : en",
     "nature)Montant",
     "perçu",
     "pendant",
     "l’année (€)"],
    sep_key
    )
keytous_financ3 = sep_keywords(
    ["Financement externe additionnel",
     "Etablissement",
     "(coordinateur",
     "ou",
     "partenaire*) ayant",
     "perçu",
     "le",
     "ﬁnancement",
     "externeType de",
     "ﬁnanceur **Nom du",
     "ﬁnanceurType de",
     "ﬁnancement",
     "(monétaire, non",
     "monétaire : en",
     "nature)Montant",
     "perçu",
     "pendant",
     "l’année (€)"],
    sep_key
    )
keytous_financ4 = sep_keywords(
    ["Financement externe additionnel",
     "Etablissement",
     "(coordinateur",
     "ou",
     "partenaire*) ayant",
     "perçu",
     "le",
     "ﬁnancement",
     "externeType de",
     "ﬁnanceur ** Nom du",
     "ﬁnanceurType de",
     "ﬁnancement",
     "(monétaire, non",
     "monétaire : en",
     "nature)Montant",
     "perçu",
     "pendant",
     "l’année",
     "(€)"],
    sep_key
    )
keytous_ERC = sep_keywords(
    ["Projets soumis / retenus au Conseil européen de la recherche (European Research",
     "Council – ERC)",
     "ProjetNom du",
     "chercheurPrénom du",
     "chercheurRetenuMontant du",
     "ﬁnancement",
     "obtenuLien du projet",
     "soumis à",
     "l\'ERC",
     "avec",
     "le projet",
     "ﬁnancé",
     "par France",
     "2030"],
    sep_key)
keytous_ERC2 = sep_keywords(
    ["Projets soumis / retenus au Conseil européen de la recherche (European Research",
     "Council – ERC)",
     "ProjetNom du",
     "chercheurPrénom du",
     "chercheurRetenuMontant du",
     "ﬁnancement",
     "obtenuLien du projet soumis",
     "à",
     '''l\'ERC''',
     "avec le projet",
     "ﬁnancé par",
     "France",
     "2030"
     ],
    sep_key)
keytous_ERC3 = sep_keywords(
    ["Projets soumis / retenus au Conseil européen de la recherche (European Research",
     "Council – ERC)",
     "ProjetNom du",
     "chercheurPrénom du",
     "chercheurRetenuMontant du",
     "ﬁnancement",
     "obtenuLien du projet",
     "soumis",
     "à",
     "l'ERC",
     "avec",
     "le projet",
     "ﬁnancé par",
     "France",
     "2030"
     ],
    sep_key)
keytous_RH = sep_keywords(
    ["Ressources humaines et formation :",
     "Personnes",
     "physiques",
     "mobilisées dans",
     "l’année*Dont",
     "femmes*ETPT tous genres",
     "confondus**",
     "Enseignant-chercheur et chercheur (professeur, maître de",
     "conférences, directeur de recherche, chargé de recherche)"],
    sep_key
    )
keytous_RHbis = sep_keywords(
    ["Ressources humaines",
     "Personnes",
     "physiques",
     "mobilisées dans",
     "l’annéeDont",
     "femmesETPT tous",
     "genres",
     "confondus",
     "Enseignant-chercheur et chercheur (professeur, maître de",
     "conférences, directeur de recherche, chargé de recherche)"],
     sep_key)
keytous_RH2 = sep_keywords(
    ["Ingénieur de recherche, ingénieur d’études, assistant",
     "ingénieur,",
     "technicien de recherche et de formation, adjoint",
     "technique de",
     "recherche et de formation"],
    sep_key
    )
keytous_formation = sep_keywords(
    ["Formation",
     "Nombre de personnes",
     "inscrites Dont Femmes",
     "Inscrits en première année pour une formation Bac+2"],
    sep_key
    )
keytous_formation2 = sep_keywords(
    ["Formation",
     "Nombre de personnes",
     "inscritesDont Femmes",
     "Inscrits en première année pour une formation Bac+2"],
    sep_key
    )
keytous_doct = sep_keywords(
    ["Doctorats",
     "Nom du",
     "DoctorantPrénom du",
     "DoctorantNuméro",
     "ORCIDDoctorat",
     "réalisé",
     "grâce",
     "à",
     "une",
     "bourse",
     "CIFRESi Thèse",
     "CIFRE,",
     "nom",
     "du",
     "PartenaireSi Thèse",
     "CIFRE,",
     "SIRET",
     "du",
     "Partenaire"],
    sep_key
    )



## Préparation des mots-clés
keywords_indic = [
    # PART 5 : INDICATEURS COMMUNS FRANCE 2030
    #"INDICATEURS COMMUNS FRANCE 2030",
    #"Toutes les données sont renseignées en année civile.",
    #"Brevets",
    #"Numéro de Demande",
    ["INDICATEURS COMMUNS FRANCE 2030\nToutes les données sont renseignées en année civile.\nBrevets\nNuméro de Demande",
     "INDICATEURS COMMUNS FRANCE 2030\nToutes les données sont renseignées en année civile. Brevets\nNuméro de Demande",
     "INDICATEURS COMMUNS FRANCE 2030\nToutes les données sont renseignées en année civile.\nBrevets Numéro de Demande"],
    
    #"Données de la recherche",
    #"DOI (identiﬁants uniques pérennes) du jeu de données issu du projet",
    ["Données de la recherche\nDOI (identiﬁants uniques pérennes) du jeu de données issu du projet",
     "Données de la recherche DOI (identiﬁants uniques pérennes) du jeu de données issu du projet"],
    
    #"Codes sources et logiciels",
    #"URL, SWHID ou DOI du logiciel déposé rattaché au projet",
    ["Codes sources et logiciels\nURL, SWHID ou DOI du logiciel déposé rattaché au projet",
     "Codes sources et logiciels URL, SWHID ou DOI du logiciel déposé rattaché au projet"] + keytous_codesource,
    
    
    # "Technologies issues des projets",
    # "Technologie Clé",
    # "TRL de départ\ndéﬁni au début\ndu projet",
    # "TRL atteint\nl\'année de la\ncollecte",
    # "TRL d\'arrivée visé au\nmoment du lancement\ndu projet",
    # "Déﬁnir plus précisément\nles technologies\nproduites",
    ["Technologies issues des projets\nTechnologie CléTRL de départ\ndéﬁni au début\ndu projetTRL atteint\nl\'année de la\ncollecteTRL d\'arrivée visé au\nmoment du lancement\ndu projetDéﬁnir plus précisément\nles technologies\nproduites",
     "Technologies issues des projets\nTechnologie CléTRL de\ndépart\ndéﬁni au\ndébut du\nprojetTRL atteint\nl'année de la\ncollecteTRL d'arrivée visé\nau moment du\nlancement du\nprojetDéﬁnir plus précisément les\ntechnologies produites",
     "Technologies issues des projets Technologie\nCléTRL de\ndépart\ndéﬁni au\ndébut du\nprojetTRL atteint\nl'année de\nla collecteTRL d'arrivée\nvisé au\nmoment du\nlancement du\nprojetDéﬁnir plus précisément les technologies\nproduites",
     "Technologies issues des projets Technologie\nCléTRL de\ndépart\ndéﬁni au\ndébut du\nprojetTRL atteint\nl\'année de\nla collecteTRL d\'arrivée\nvisé au\nmoment du\nlancement du\nprojetDéﬁnir plus précisément les technologies\nproduites",
     "Technologies issues des projets\nTechnologie CléTRL de\ndépart\ndéﬁni au\ndébut du\nprojetTRL\natteint\nl'année de\nla collecteTRL d'arrivée\nvisé au\nmoment du\nlancement du\nprojetDéﬁnir plus précisément les technologies\nproduites"] + keytous_techno,
    
    # "Start-up",
    # "SIRET",
    ["Start-up\nSIRET",
     "Start-up SIRET"],
    
    #"Financement externe :"
    #"Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur ** Nom du ﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)"
    ["Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur ** Nom du ﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement (coordinateur\nou partenaire*) ayant perçu\nle ﬁnancement externeType de\nﬁnanceur **Nom du\nﬁnanceurType de ﬁnancement\n(monétaire, non\nmonétaire : en nature)Montant perçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement (coordinateur ou\npartenaire*) ayant perçu le\nﬁnancement externeType de\nﬁnanceur **Nom du\nﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe : Etablissement (coordinateur\nou partenaire*) ayant perçu\nle ﬁnancement externeType de\nﬁnanceur **Nom du\nﬁnanceurType de ﬁnancement\n(monétaire, non\nmonétaire : en nature)Montant perçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant perçu\nle ﬁnancement externeType de ﬁnanceur **Nom du\nﬁnanceurType de ﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)"
     "Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur **Nom du\nﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur **Nom du\nﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant perçu le\nﬁnancement externeType de ﬁnanceur **Nom du\nﬁnanceurType de ﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe :\nEtablissement\n(coordinateur ou\npartenaire*) ayant perçu\nle ﬁnancement externeType de ﬁnanceur **Nom du\nﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     # (Différence année 2024)
     "Financement externe additionnel\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur **Nom du\nﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe additionnel Etablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le ﬁnancement\nexterneType de ﬁnanceur ** Nom du ﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe additionnel\nEtablissement\n(coordinateur ou\npartenaire*) ayant perçu\nle ﬁnancement externeType de ﬁnanceur ** Nom du ﬁnanceurType de\nﬁnancement\n(monétaire, non\nmonétaire : en\nnature)Montant\nperçu\npendant\nl’année (€)",
     "Financement externe additionnel\nEtablissement\n(coordinateur ou\npartenaire*) ayant\nperçu le\nﬁnancement\nexterneType de ﬁnanceur ** Nom du ﬁnanceurType de\nﬁnancement\n(monétaire,\nnon monétaire\n: en nature)Montant\nperçu\npendant\nl’année\n(€)"] + keytous_financ + keytous_financ2 + keytous_financ3 + keytous_financ4,
    
    # Projets ERC
    ["Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC)\nProjet Nom du chercheur Prénom du chercheur RetenuLien du projet soumis à l\'ERC avec le\nprojet ﬁnancé par France 2030",
     "Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC) Projet Nom du chercheur Prénom du chercheur RetenuLien du projet soumis à l\'ERC avec le\nprojet ﬁnancé par France 2030",
     # (Différence 2024)
     "Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC)\nProjetNom du\nchercheurPrénom du\nchercheurRetenuMontant du\nﬁnancement\nobtenuLien du projet soumis à\nl\'ERC avec le projet\nﬁnancé par France\n2030",
     "Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC)\nProjetNom du\nchercheurPrénom du\nchercheurRetenuMontant du\nﬁnancement\nobtenuLien du projet soumis à l'ERC\navec le projet ﬁnancé par\nFrance 2030",
     "Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC)\nProjetNom du\nchercheurPrénom du\nchercheurRetenuMontant du\nﬁnancement obtenuLien du projet soumis à\nl\'ERC avec le projet\nﬁnancé par France 2030",
     "Projets soumis / retenus au Conseil européen de la recherche (European Research\nCouncil – ERC)\nProjetNom du\nchercheurPrénom du\nchercheurRetenuMontant du\nﬁnancement\nobtenuLien du projet soumis\nà l'ERC avec le projet\nﬁnancé par France\n2030 "] + keytous_ERC + keytous_ERC2 + keytous_ERC3,
    
    # Ressources humaines et formation
    ["Ressources humaines et formation : Personnes\nphysiques\nmobilisées dans\nl’année*Dont\nfemmes*ETPT tous genres\nconfondus**\nEnseignant-chercheur et chercheur (professeur, maître de\nconférences, directeur de recherche, chargé de recherche)",
     "Ressources humaines et formation :\nPersonnes\nphysiques\nmobilisées dans\nl’année*Dont\nfemmes*ETPT tous genres\nconfondus**\nEnseignant-chercheur et chercheur (professeur, maître de\nconférences, directeur de recherche, chargé de recherche)",
     # (Différence année 2024)
     "Ressources humaines\nPersonnes\nphysiques\nmobilisées dans\nl’annéeDont\nfemmesETPT tous\ngenres\nconfondus\nEnseignant-chercheur et chercheur (professeur, maître de\nconférences, directeur de recherche, chargé de recherche)",
     "Ressources humaines Personnes\nphysiques\nmobilisées dans\nl’annéeDont\nfemmesETPT tous\ngenres\nconfondus\nEnseignant-chercheur et chercheur (professeur, maître de\nconférences, directeur de recherche, chargé de recherche)"] + keytous_RH + keytous_RHbis,
    ["Ingénieur de recherche, ingénieur d’études, assistant ingénieur,\ntechnicien de recherche et de formation, adjoint technique de\nrecherche et de formation",
     "Ingénieur de recherche, ingénieur d’études, assistant\ningénieur, technicien de recherche et de formation, adjoint\ntechnique de recherche et de formation"] + keytous_RH2,
    
    # Formation
    ["Formation\nNombre de personnes inscrites Dont Femmes\nInscrits en première année pour une formation Bac+2",
     "Formation Nombre de personnes inscrites Dont Femmes\nInscrits en première année pour une formation Bac+2",
     "Formation\nNombre de personnes\ninscritesDont Femmes\nInscrits en première année pour une formation Bac+2"] + keytous_formation + keytous_formation2,
    ["Inscrits en deuxième année pour une formation Bac+2"],
    ["Inscrits en première année pour une Licence ou Bac+3"],
    ["Inscrits en deuxième année pour une Licence ou Bac+3"],
    ["Inscrits en troisième année pour une Licence ou Bac+3"],
    ["Inscrits en première année pour un Master ou équivalent"],
    ["Inscrits en deuxième année pour un Master ou équivalent"],
    ["Inscrits en diplôme universitaire d’une année"],
    ["Inscrits en première année d’un diplôme universitaire de plus d’une année"],
    ["Inscrits en deuxième année d’un diplôme universitaire de plus d’une année"],
    ["Inscrits en troisième année d’un diplôme universitaire de plus d’une année"],
    
    
    # Doctorat
    ["Doctorats\nNom du\nDoctorantPrénom du\nDoctorantNuméro ORCIDDoctorat\nréalisé grâce à\nune bourse\nCIFRESi Thèse CIFRE,\nnom du\nPartenaireSi Thèse CIFRE,\nSIRET du\nPartenaire",
     "Doctorats\nNom du\nDoctorantPrénom du\nDoctorantNuméro ORCIDDoctorat\nréalisé\ngrâce à\nune bourse\nCIFRESi Thèse\nCIFRE, nom\ndu\nPartenaireSi Thèse\nCIFRE, SIRET\ndu\nPartenaire",
     "Doctorats\nNom du\nDoctorantPrénom du\nDoctorantNuméro\nORCIDDoctorat réalisé\ngrâce à une\nbourse CIFRESi Thèse CIFRE,\nnom du\nPartenaireSi Thèse CIFRE,\nSIRET du\nPartenaire",
     "Doctorats\nNom du\nDoctorantPrénom du\nDoctorantNuméro ORCIDDoctorat\nréalisé\ngrâce à une\nbourse\nCIFRESi Thèse\nCIFRE, nom\ndu\nPartenaireSi Thèse\nCIFRE, SIRET\ndu\nPartenaire",
     "Doctorats\nNom du\nDoctorantPrénom du\nDoctorantNuméro\nORCIDDoctorat\nréalisé grâce\nà une bourse\nCIFRESi Thèse CIFRE,\nnom du\nPartenaireSi Thèse CIFRE,\nSIRET du\nPartenaire",
     "Doctorats Nom du\nDoctorantPrénom du\nDoctorantNuméro\nORCIDDoctorat réalisé\ngrâce à une\nbourse CIFRESi Thèse CIFRE,\nnom du\nPartenaireSi Thèse CIFRE,\nSIRET du\nPartenaire"] + keytous_doct,
    ["Post-doctorats\nNom du post-doctorant Prénom du post-doctorant Numéro ORCID",
     "Post-doctorats Nom du post-doctorant Prénom du post-doctorant Numéro ORCID"],
    
    # PART 6 : INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS PRIORITAIRES DE RECHERCHE
    # Programmes de maturation / prématuration
    ["INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS\nPRIORITAIRES DE RECHERCHE\nTransfert aux programmes de Maturation / Prématuration : Nombre de projets transférés vers des programmes de Maturation / Prématuration",
     "INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS\nPRIORITAIRES DE RECHERCHE\nTransfert aux programmes de Maturation / Prématuration :\nNombre de projets transférés vers des programmes de Maturation / Prématuration",
     # (Différence 2024)
     "INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS\nPRIORITAIRES DE RECHERCHE\nTransfert aux programmes de Maturation / Prématuration\nNombre de projets transférés vers des programmes de Maturation / Prématuration",
     "INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS\nPRIORITAIRES DE RECHERCHE\nTransfert aux programmes de Maturation / Prématuration Nombre de projets transférés vers des programmes de Maturation / Prématuration",
     "INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS\nPRIORITAIRES DE RECHERCHE Transfert aux programmes de Maturation / Prématuration :\nNombre de projets transférés vers des programmes de Maturation / Prématuration",
     "INDICATEURS COMMUNS AUX PROGRAMMES ET EQUIPEMENTS PRIORITAIRES DE RECHERCHE\nTransfert aux programmes de Maturation / Prématuration\nNombre de projets transférés vers des programmes de Maturation / Prématuration"],
    ["Fichier détaillé des projets transmis aux programmes de maturations",
     "Fichier détaillé des projets transmis aux programmes de Maturations"]
    ]






#%% ====================== MAIN ===============================================
#%%% ====== I/ CHOOSE THE DIRECTORIES =========================================

## Liste des PDF
# Directory du PDF à extraire
onlyfiles = [f for f in listdir(dir_PDF_base) if isfile(join(dir_PDF_base, f))]
#idx_PDF = 38

## On initialise les dataframe
data_infoprojet_xlsx = pd.DataFrame()
data_resultatimpact_xlsx = pd.DataFrame()
data_techno_xlsx = pd.DataFrame()
data_financ_xlsx = pd.DataFrame()
data_ERC_xlsx = pd.DataFrame()
data_RH_xlsx = pd.DataFrame()
data_formation_xlsx = pd.DataFrame()
data_docpostdoc_xlsx = pd.DataFrame()


## On fait tourner sur tous les PDF
#for idx_PDF in range(len(onlyfiles)) :
for idx_PDF in range(0,len(onlyfiles)) :
#for idx_PDF in range(7) :
    
    print(idx_PDF)
    
    idx_PDF_k = idx_PDF
    #idx_PDF = 2
    
    nom_PDF_exemple = onlyfiles[idx_PDF]
    dir_PDF_exemple = dir_PDF_base + nom_PDF_exemple
    print(dir_PDF_exemple)


    #%%% ====== II/ EXTRAIRE LE TEXTE =============================================
    
    ### Extraire le texte des pages du PDF
    ### https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html
    reader = PyPDF2.PdfReader(dir_PDF_exemple)
    # printing number of pages in pdf file
    #print(len(reader.pages))
    # On extrait le texte de toutes les pages
    text = ""
    for num_page in range(len(reader.pages)):
        # getting a specific page from the pdf file
        page = reader.pages[num_page]
        # extracting text from page
        text = text + " " + page.extract_text()
    # Texte en str
    #print(text)



    #%%% ====== III/ EXTRACTIONS ===================================================
    
    
    ## Infos du projets
    data_infoprojet = extract_data_from_text(keywords_info)
    # Extraction textuelle partie 2
    info_indic = extract_data_from_text(keywords_indic)



    #%%% ====== V/ INDICATEURS ====================================================

    
    ## Année
    annee = indic_annee(data_infoprojet)
    ## Projet
    projet = indic_projet(data_infoprojet)
    ## Simplifie ou non
    reporting_simplifie = simplifie(dir_PEPR_projets, projet)
    # PEPR en SNA ou non
    SNA_PEPR = SNA(dir_PEPR_projets, projet)
    
    
    ## Si c'est un reporting pas simplifié, on refait le data_infoprojet
    if reporting_simplifie == "Non" and SNA_PEPR == "Non" :
        print("Non simplifie + pas SNA")
        data_infoprojet = extract_data_from_text(keywords_info_complet)
    elif reporting_simplifie == "Non" and SNA_PEPR == "Oui" :
        print("Non simplifie + SNA")
        data_infoprojet = extract_data_from_text(keywords_info_complet_SNA)
    
    
    ## PEPR
    PEPR = indic_PEPR(dir_PEPR_projets, projet)
    ## Infos du projets
    data_infoprojet_indic = indic_infoprojet(data_infoprojet, reporting_simplifie, SNA_PEPR)
    print(data_infoprojet_indic.iloc[0])
    ## Brevet
    data_brevet = indic_brevet(info_indic)
    ## Données de la recherche
    data_dataset = indic_donneesrecherche(info_indic)
    ## Codes sources logiciel
    data_logiciel = indic_logiciel(info_indic)
    ## Technologie
    data_techno = indic_techno(info_indic)
    ## Start-up
    data_startup = indic_startup(info_indic)
    ## Financement externe
    data_financ = indic_financ(info_indic)
    ## Projets ERC
    data_ERC = indic_ERC(info_indic)
    ## Ressource humaine et formation
    data_RH = indic_RH(info_indic)
    ## Formation
    data_formation = indic_formation(info_indic)
    ## Doctorat
    data_doct = indic_doct(info_indic)
    ## Post-doctorat
    data_postdoc = indic_postdoc(info_indic)
    ## Projets transférés vers des programmes de maturation / prématuration
    data_matpremat = indic_matpremat(info_indic)




#%%% ====== VI/ FEUILLETS EXCEL ===============================================
    

    ### Dataframes du PDF k
    ## Feuillet ReportRST_InfosProjets
    data_infoprojet_xlsx_k = xlsx_infoprojet(data_infoprojet_indic)
    ## Feuillet ReportRST_ResultatsImpacts
    data_resultatimpact_xlsx_k = xlsx_resultatimpact(data_brevet,data_dataset,data_logiciel,data_startup,data_matpremat)
    ## Feuillet ReportRST_TRL
    data_techno_xlsx_k = xlsx_techno(data_techno)
    ## Feuillet ReportRST_Financements
    data_financ_xlsx_k = xlsx_financ(data_financ)
    ## Feuillet ReportRST_ERC
    data_ERC_xlsx_k = xlsx_ERC(data_ERC)
    ## Feuillet ReportRST_RH
    data_RH_xlsx_k = xlsx_RH(data_RH)
    ## Feuillet ReportRST_Formations
    data_formation_xlsx_k = xlsx_formation(data_formation)
    ## Feuillet ReportRST_DocPostdoc
    data_docpostdoc_xlsx_k = xlsx_docpostdoc(data_doct,data_postdoc)



    ### On met ensemble les dataframes
    data_infoprojet_xlsx = pd.concat([data_infoprojet_xlsx, 
                                      data_infoprojet_xlsx_k], 
                                     axis=0, 
                                     ignore_index=False)
    data_resultatimpact_xlsx = pd.concat([data_resultatimpact_xlsx,
                                          data_resultatimpact_xlsx_k],
                                         axis=0, 
                                         ignore_index=False)
    data_techno_xlsx = pd.concat([data_techno_xlsx,
                                  data_techno_xlsx_k],
                                 axis=0,
                                 ignore_index=False)
    data_financ_xlsx = pd.concat([data_financ_xlsx,
                                  data_financ_xlsx_k],
                                 axis=0,
                                 ignore_index=False)
    data_ERC_xlsx = pd.concat([data_ERC_xlsx,
                               data_ERC_xlsx_k],
                              axis=0,
                              ignore_index=False)
    data_RH_xlsx = pd.concat([data_RH_xlsx,
                              data_RH_xlsx_k],
                             axis=0,
                             ignore_index=False)
    data_formation_xlsx = pd.concat([data_formation_xlsx,
                                     data_formation_xlsx_k],
                                    axis=0,
                                    ignore_index=False)
    data_docpostdoc_xlsx = pd.concat([data_docpostdoc_xlsx,
                                      data_docpostdoc_xlsx_k],
                                     axis=0, 
                                     ignore_index=False)




#%%% ====== VII/ CONVERTIR EN EXCEL ===========================================


sheetname_and_alldata = [
    ["ReportRST_DocPostdoc", data_docpostdoc_xlsx],
    ["ReportRST_ERC", data_ERC_xlsx],
    ["ReportRST_Financements", data_financ_xlsx],
    ["ReportRST_Formations", data_formation_xlsx],
    ["ReportRST_InfosProjets", data_infoprojet_xlsx],
    ["ReportRST_ResultatsImpacts", data_resultatimpact_xlsx],
    ["ReportRST_RH", data_RH_xlsx],
    ["ReportRST_TRL", data_techno_xlsx]
    ]


with pd.ExcelWriter(dir_Excel_exemple) as writer:    
    for elem in sheetname_and_alldata:
        print(elem)
        elem[1].to_excel(writer,sheet_name=elem[0], 
                         index=False,
                         engine='openpyxl')



