"""
PROJET D'ANNEE FDO, simulateur de mémoire cache à un niveau
SECUNDAR ISMAEL
504107
mohammad.ik.secundar@ulb.be
"""


import sys

M = [i for i in range(32)]

L1Data = [0]*8                                  # contenu d'une case mémoire

L1Addr = [0]*8                                  # adresse qui stock en mémoire les valeurs qui correspondent

L1Dirt = [False]*8                              # Change dans le cache mais pas dans la mémoire

LastUse= [0]*8

compteur = 1                                    # initialisé à 1 pour l'utiliser dans les fonctions


def lecture(adresse):
    """
    Fonction qui permet de lire une valeur à une certaine adresse dans la mémoire mais avant cela il vérifie si cette adresse
    est dans la cache.

    Args:
        adresse: adresse à laquelle une valeur i est stockée en mémoire

    Returns: Retourne la valeur LU

    """
    global compteur

    if adresse in L1Addr:

        k = L1Addr.index(adresse)
        valeur = L1Data[k]
        LastUse[k] = compteur
        print_read(adresse,valeur,k, LastUse[k])

    else:
        v = M[adresse]
        k = LastUse.index(min(LastUse))         # On demande l'index de la plus petite valeur de LastUse
        if L1Dirt[k]:
            M[L1Addr[k]] = L1Data[k]

        x = L1Data[k]
        b = L1Addr[k]
        L1Addr[k] = adresse
        L1Data[k] = v
        L1Dirt[k] = False
        LastUse[k] = compteur
        print_read(adresse, v, k, LastUse[k], True, x, b)
        valeur = L1Data[k]
    compteur += 1                               # On incrémente le compteur pour savoir quelle valeur l'on a utilisé le plus récemment
    return valeur

def ecriture(adresse,v):
    """
    Fonction qui permet d'écrire une valeur v à une certaine adresse dans la mémoire.
    Si celle ci n'a pas été modifiée précédement . L'on choisi une case à sacrifier dans la cache, on prend la case qui doit être sacrifiée
    et on stock la valeur de cette case dans la mémoire si elle n'a pas été modifiée précédement
    Args:
        adresse:
        v:

    Returns:

    """
    global compteur

    if adresse in L1Addr:
        k = L1Addr.index(adresse)
        L1Data[k] = v
        LastUse[k] = compteur
        if L1Dirt[k]:
            is_new_dirt = False
        else:
            is_new_dirt = True
        L1Dirt[k] = True

        print_write(adresse,v,k,LastUse[k],is_new_dirty=is_new_dirt)

    else:
        M[adresse] = v
        k = LastUse.index(min(LastUse))     # On demande l'index de la plus petite valeur de LastUse

        if L1Dirt[k]:
            M[L1Addr[k]] = L1Data[k]
        x = L1Data[k]
        b = L1Addr[k]
        L1Addr[k] = adresse
        L1Data[k] = v

        L1Dirt[k] = False

        if LastUse[k] == 0:
            x = None
            b = None
        LastUse[k] = compteur

        print_write(adresse,v,k,LastUse[k],True,x,b)
    compteur += 1


"""
Args:
            a (int): Adresse mémoire écrite
            v (int): Valeur écrite à cette adresse
            c (int): Case du cache affectée
            l (int): LU (LastUse) de la case du cache affectée
            miss (bool): True si un cache miss a eu lieu, False sinon
            x (int): valeur dirty écrite en mémoire
            b (int): addresse ou la valeur dirty a été écrite
            is_new_dirty (bool): True si la case du cache affectée est devenue dirty"""
#i = adresse
#j = index


def main():
    file_name = sys.argv[1]
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for i in lines:
            line = i.strip().split()

            if line[0] == "W":
                ecriture(int(line[2]),int(line[1]))
            else:
                lecture(int(line[1]))


def print_read(a, v, c, l, miss=False, x=None, b=None):
    """ Affiche un méssage déscriptif du read effectué au format:

        "RD `v` from `a`\t(miss: victime|hit: case) `c` (LU `l`)\t[dirty WR `x` to `b`]"

        Si `miss` est `True`, 'miss: victime' est imprimé, sinon 'hit: case' est imprimé

        Le suffixe 'dirty WR `x` to `b`' ne sera affiché que si une de ces deux
        variables n'est pas `None`

        Args:
            a (int): Adresse mémoire lue
            v (int): Valeur lue à cette adresse
            c (int): Case du cache affectée
            l (int): LU (LastUse) de la case du cache affectée
            miss (bool): True si un cache miss a eu lieu, False sinon
            x (int): valeur dirty écrite en mémoire
            b (int): addresse ou la valeur dirty a été écrite
    """
    output = "RD {} from {}\t{} {} (LU {})".format(
        v, a, 'miss: victim' if miss else 'hit: cell', c, l)
    if x is not None or b is not None:
        output += "\t\tdirty WR {} to {}".format(x, b)
    print(output)


def print_write(a, v, c, l, miss=False, x=None, b=None, is_new_dirty=False):
    """ Affiche un méssage déscriptif du write effectué au format:

        "WR `v` to `a`\t(miss: victime|hit: case) `c` (LU `l`)\t[dirty WR `x` to `b`|dirty!]"

        Si `miss` est `True`, 'miss: victime' est imprimé, sinon 'hit: case' est imprimé

        Le suffixe 'dirty WR `x` to `b`' ne sera imprimé que si une de ces deux
        variables n'est pas `None`

        Le suffixe 'dirty!' ne sera imprimé que si `is_new_dirty` est vrai.

        Args:
            a (int): Adresse mémoire écrite
            v (int): Valeur écrite à cette adresse
            c (int): Case du cache affectée
            l (int): LU (LastUse) de la case du cache affectée
            miss (bool): True si un cache miss a eu lieu, False sinon
            x (int): valeur dirty écrite en mémoire
            b (int): addresse ou la valeur dirty a été écrite
            is_new_dirty (bool): True si la case du cache affectée est devenue dirty
    """
    output = "WR {} to {}\t{} {} (LU {})".format(
        v, a, 'miss: victim' if miss else 'hit: cell', c, l)
    if x is not None or b is not None:
        output += "\t\tdirty WR {} to {}".format(x, b)
    if is_new_dirty:
        assert not miss, "is_new_dirty ne peut être vrai qu'en cas de cache hit"
        output += "\t\tdirty!"

    print(output)

if __name__ == '__main__':
    main()