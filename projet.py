import Labyrinthe
import tkdraw.basic as graph 

def rectangle(x1, x2, y1, y2, color="black"):
    for y in range(y1, y2):
        for x in range(x1, x2):
            graph.plot(y, x, color)
            
def dessiner(laby, taille):
    for i in range(len(laby)):
        for j in range(len(laby[i])):
            if laby[i][j] == 0:
                rectangle(i*taille, i*taille+taille, j*taille, j*taille+taille)
            elif laby[i][j] == 2:
                rectangle(i*taille, i*taille+taille, j*taille, j*taille+taille, "blue")
            elif laby[i][j] == 3:
                rectangle(i*taille, i*taille+taille, j*taille, j*taille+taille, "red")           

def voisins_accessibles(cellule, laby):
    lig, col = cellule
    tous_voisins =[(lig+1, col), (lig-1, col), (lig, col+1), (lig, col-1)] 
    voisins_acc = []
    for v in tous_voisins:
        i, j = v
        if laby[i][j] != 0:
            voisins_acc += [v]
    return voisins_acc


def explorer_voie(cellule, sortie, laby, dernier_voie=[]):
    # Chercher les voisins accessibles de ce cellule
    # voisins_acc: une liste contenant les voisins soit vaut 1(voie) soit vaut 3(la sortie)
    voisins_acc = voisins_accessibles(cellule, laby)
    # Cette liste est utilise par enrigester chaque partie du itinéraire vers une sortie réussie,
    # qui est reinitialise chaque recursion.
    voisins_fin = []
    
    if len(dernier_voie) != 0:
        # Si on a deja passe un cellule, on va pas le passer encore une fois
        for i in dernier_voie:
            if i in voisins_acc:
                voisins_acc.remove(i)
        # bifurication, car toutes ses voisins accessibles(pas mur) sont deja passes
        if len(voisins_acc) == 0:
            return None
    # Apres "nettoyer", si voisins_acc n'est pas vide, c-a-dire il y a voisins on peut parcourir
    for v in voisins_acc:
        # Si l'un des voisins accessibles est la sortie, on fini de parcourir et retourner le cellule
        # de la sortie
        if v == sortie:
            return [v]
        # Si le cellule n'est pas la sortie, c-a-dire on doit toujours parcourir
        else:
            # Puisque ce cellule est accessible et il n'est pas la sortie ni dans la dernier_voie,
            # on doit l'ajouter a la dernier_voie
            dernier_voie += [cellule]
            # On recure cette fonction avec ce cellule, apres la recursion elle va retourner "voisins_temp"
            # "voisins_temp" - 1.soit vaut None: c-a-dire lorsque cette recursion d'appeler explorerVoie 
            # encore une fois, apres "nettoyer", len(voisins_acc) dans ce cas recursive == 0, il n'y a 
            # pas de voisins accessibles de ce cellule, c'est signifie que ce cellule est recontre un 
            # bifurication. Dans ce cas, on neglige ce cellule, et parcourir le voisin porchain de voisins_acc.
            voisins_temp = explorer_voie(v, sortie, laby, dernier_voie)
            if voisins_temp == None:
                pass
            #"voisins_temp" - 2.soit une liste(voisins_fin): 
            # On neglige tous les voisins qui dans la situation de bifurication(leurs voisins_temp retourne
            # par le niveau prochain de recursion est None), jusqu'a qui arrive a la sortie, c-a-dire, 
            # dans tous les retournes de recursions ici (sans bifurication, c'est la voie reussi) 
            # voisins_temp contenant la sortie. A chaque retour, on ajoute donc le voisin et 
            # voisins_temp de chaque recursion a voisins_fin, et retourner voisins_fin a le niveau 
            # précédent de la recursion. Jusqu'a le premier niveau, qui est le itinéraire complet 
            # vers une sortie réussie.
            else:
                voisins_fin += [v] + voisins_temp
                return voisins_fin


def dessinerVoie(lst, taille):
    for v in lst:
        lgn, col = v
        rectangle(lgn*taille+5, lgn*taille+15, col*taille+5, col*taille+15, "#F264B7")
        
def sortie(laby):
    for i in range(len(laby)):
        for j in range(len(laby[i])):
            if laby[i][j] == 3:
                return (i, j)
        
def entree(laby):
    for i in range(len(laby)):
        for j in range(len(laby[i])):
            if laby[i][j] == 2:
                return (i, j)
    
taille_cellule = 20
haut = taille_cellule*15
larg = taille_cellule*15
laby = Labyrinthe.creer(15, 15)
for ligne in laby:
    print(ligne)
                        
cellule_sortie = sortie(laby)
cellule_entree = entree(laby)
graph.open_win(haut, larg)

dessiner(laby, taille_cellule)
lst = explorer_voie(cellule_entree, cellule_sortie, laby)
print(lst)
dessinerVoie(lst, taille_cellule)

graph.wait()

