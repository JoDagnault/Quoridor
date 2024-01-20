"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
"""
from copy import deepcopy

from quoridor_error import QuoridorError

from graphe import construire_graphe

import networkx as nx


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        état (dict): état du jeu tenu à jour.
    """

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Appel la méthode `vérification` pour valider les données et assigne
        ce qu'elle retourne à l'attribut `self.état`.

        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
        """
        self.état = deepcopy(self.vérification(joueurs, murs))

    def vérification(self, joueurs, murs):
        """Vérification d'initialisation d'une instance de la classe Quoridor.

        Valide les données arguments de construction de l'instance et retourne
        l'état si valide.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de list [x, y] uniquement.
        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """

        #Test si joueurs n'est pas une liste
        if not isinstance(joueurs, list):
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")

        #Test si joueurs ne contient pas deux joueurs
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux.")

        for i, joueur in enumerate(joueurs):
            #Test si les joueurs sont des dictionnaires
            if isinstance(joueur, dict):
                #Test si le nombre de murs n'est pas entre 10 et 0
                if joueur['murs'] > 10 or joueur['murs'] < 0:
                    raise QuoridorError("Le nombre de murs qu'un" +\
                    "joueur peut placer est plus grand que 10, ou négatif.")
                #Test si la position x (joueur[pos][0]) et la position y
                #(joueur[pos][1]) ne sont pas entre 1 et 9
                if joueur['pos'][0] < 1 or joueur['pos'][0] > 9 or +\
                    joueur['pos'][1] < 1 or joueur['pos'][1] > 9:
                    raise QuoridorError("La position d'un joueur est invalide.")

            #Si le joueur a juste un nom, on lui assigne une position
            #initiale et un nombre de murs initial
            if isinstance(joueur, str):
                joueurs[i] = {"nom": joueur, "murs": 10, "pos": None}

                #Position = [5,1] pour joueur premier rang et [5,9] pour joueur deuxieme rang
                if i == 0:
                    joueurs[i]['pos'] = [5, 1]
                elif i == 1:
                    joueurs[i]['pos'] = [5, 9]

        #Test si murs est present
        if murs:
            #Test si murs n'est pas un dictionnaire
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
            #Test si le nombre de mur total n'est pas egal a 20
            if len(murs['horizontaux']) + len(murs['verticaux']) +\
                + joueurs[0]['murs'] + joueurs[1]['murs'] != 20:
                raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20")

            for mur in murs['horizontaux']:
                #Test si la position x (mur[0]) du mur horizontal n'est pas entre 1 et 8
                #Test si la position y  (mur[1]) du mur horizontal n'est pas entre 2 et 9
                if mur[0] < 1 or mur[0] > 8 or mur[1] < 2 or mur[1] > 9:
                    raise QuoridorError("La position d'un mur est invalide.")

            for mur in murs['verticaux']:
                #Test si la position x (mur[0]) du mur vertical n'est pas entre 2 et 9
                #Test si la position y  (mur[1]) du mur vertical n'est pas entre 1 et 8
                if mur[0] < 2 or mur[0] > 9 or mur[1] < 1 or mur[1] > 8:
                    raise QuoridorError("La position d'un mur est invalide.")
        else:
            murs = {'horizontaux': [], 'verticaux': []}

        return {"joueurs" : joueurs, "murs" : murs}

        #A faire :
        #Tester si position est de forme [x, y] ???


    def formater_légende(self):
        """Formater la représentation graphique de la légende.

        Returns:
            str: Chaîne de caractères représentant la légende.
        """

        legende = "Légende:\n"
        longest_player_name = ''

        #Boucle pour tester le plus long nom dans les joueurs
        for joueur in self.état['joueurs']:
            if len(joueur["nom"]) > len(longest_player_name):
                longest_player_name = joueur["nom"]

        #Boucle pour formatter la legende
        for i, joueur in enumerate(self.état['joueurs']):
            #On ajoute le numero du joueur ainsi que son nom
            #On ajouter un nombre d'espace egal a la difference entre la
            #longueur du nom du joueur et la longueur du nom le plus long
            #On ajoute le nombre de murs de chaque joueurs
            legende += f"""   {i+1}={joueur['nom']}, {' ' * (len(longest_player_name) -
            len(joueur['nom']) )}{'murs=' + '|' * joueur['murs']}\n"""

        return legende

    def formater_damier(self):
        """Formater la représentation graphique du damier.

        Returns:
            str: Chaîne de caractères représentant le damier.
        """

        #La logique est de passer a travers chaque colonne de chaque
        #ligne donc chaque case de gauche a droite et de haut en bas.
        #Ex. [1,9], [2,9], [3,9] ... [9,9], [1,8], [2,8] ...

        #Il y a toujours 1 espace a gauche et a droite de chaque case
        #Il y a soit un espace ou un mur entre deux cases
        #L'espace entre deux cases est soit ".   ." ou ". | ."

        joueurs = self.état['joueurs']
        murs = self.état['murs']

        #Ligne en haut du damier
        damier = "   -----------------------------------\n"

        #ligne = position en y
        for ligne in range(9):

            #On ajoute le numero de la ligne avec la barre verticale
            #Puisque le damier est formatter de haut en bas, on inverse la
            #ligne donc la ligne 0 est la ligne 9 et la ligne 8 est la ligne 1
            damier += str(9 - ligne) + " |"

            #colonne = position en x
            for colonne in range(9):

                #A chaque case on test si un des deux joueurs a sa position a cette case
                for i, joueur in enumerate(joueurs):
                    #Si un des joueurs est a cette case, on ajoute le numero du joueur " num "
                    if joueur['pos'] == [colonne + 1, 9 - ligne]:
                        damier += f' {i + 1} '
                        break
                #Si aucun des deux joueur n'est a cette case, on ajoute une case vide " . "
                else:
                    damier += ' . '

                #Si on est arrive a la derniere colonne,
                #il faut donc ajouter une barre et nouvelle ligne
                if colonne == 8:
                    damier += '|\n'

                #Sinon, il faut tester si un mur est present entre les cases
                else:
                    #Pour chaque entre case, on doit regarde si un mur est present
                    for mur in murs["verticaux"]:

                        #Puisque les murs font deux cases de longueur,
                        #on regarde alors a la position actuelle ainsi qu'une plus basse
                        #si un mur est present on ajoute une barre '|'
                        if mur == [colonne + 2, 9 - ligne ]:
                            damier += '|'
                            break

                        if mur == [colonne + 2, 9 - ligne  - 1]:
                            damier += '|'
                            break

                    #Si aucun mur n'est present, on ajoute un espace
                    else:
                        damier += ' '

            #A la fin du formattage d'un ligne, on a ajoute une nouvelle ligne
            #donc maintenant nous formattons les entre lignes qui continnent les murs horizontaux
            if ligne != 8:
                damier += '  |'


                #Pour les entre lignes, chaque case contient soit un mur "---" ou rien "   "
                #Chaque entre case est soit separe d'un espace ou d'un mur vertical comme les lignes

                #colonne = position en x
                for colonne in range(9):

                    #Pour chaque case de l'entre ligne, on regarde si un mur est present
                    for mur in murs["horizontaux"]:

                        #Puisque les murs font 2 cases de longueur,
                        #on regarde la position actuelle et une plus a droite
                        #Si un mur est present on ajoute "---"
                        if mur == [colonne + 1, 9 - ligne]:
                            damier += "---"
                            break
                        if mur == [colonne, 9 - ligne]:
                            damier += "---"
                            break

                    #Si aucun mur n'est present, on ajoute 3 espaces "   "
                    else:
                        damier += '   '

                    #Si on est rendu a la derniere colonne, on ajoute une nouvelle ligne
                    if colonne == 8:
                        damier += '|\n'
                        break

                    #Si nous ne sommes pas a la derniere colonne,
                    #il faut regarder si un mur vertical est present
                    #puique les murs font 2 cases de longueur
                    for mur in murs["verticaux"]:
                        if mur == [colonne + 2, 9 - ligne  - 1]:
                            damier += '|'
                            break

                    #Si aucun mur vertical est present dans l'entre case,
                    #on reagrde alors si un mur horizontal est present
                    else:
                        for mur in murs["horizontaux"]:

                            if mur == [colonne + 1, 9 - ligne]:
                                damier += "-"
                                break

                        else:
                            damier += ' '
            #A la fin on ajoute les 2 dernieres lignes du damier
            else:
                damier += "--|-----------------------------------\n"
                damier += "  | 1   2   3   4   5   6   7   8   9\n"

        return damier

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        #Retourne la legende et le damier combine ensemble
        return self.formater_légende() + self.formater_damier()

    def état_courant(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
            Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(self.état)

    def est_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        #Aucun gagnant de base
        gagnant = False

        #Test si un joueur est rendu a l'oppose du damier
        if self.état['joueurs'][0]['pos'][1] == 9:
            gagnant = self.état['joueurs'][0]['nom']
        elif self.état['joueurs'][1]['pos'][1] == 1:
            gagnant = self.état['joueurs'][1]['nom']

        return gagnant

    def récupérer_le_coup(self, joueur):
        """Récupérer le coup

        Notez que seul 2 questions devrait être posée à l'utilisateur.

        Notez aussi que cette méthode ne devrait pas modifier l'état du jeu.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La position est invalide (en dehors du damier).

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
            Le type de coup est une chaîne de caractères.
            La position est une liste de 2 entier [x, y].
        """
        if not joueur in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        coups_possibles = ['D', 'MH', 'MV']
        type_coup = input("Quel type de coup voulez-vous jouer? ('D', 'MH', 'MV'): ")

        if type_coup not in coups_possibles:
            raise QuoridorError("Le type de coup est invalide.")

        pos = input("Donnez la position où appliquer ce coup (x,y): ")
        pos_x, pos_y = pos.split(",")
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if pos_x < 1 or pos_x > 9 or pos_y < 1 or pos_y > 9:
            raise QuoridorError("La position est invalide (en dehors du damier).")

        position = [pos_x, pos_y]

        return type_coup, position

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (List[int, int]): La liste [x, y] de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        if not joueur in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        joueur = joueur - 1

        if position[0] < 1 or position[0] > 9 or position[1] < 1 or position[1] > 9:
            raise QuoridorError("La position est invalide (en dehors du damier).")

        position_joueurs = []

        for i in self.état['joueurs']:
            position_joueurs.append(i['pos'])

        graphe = construire_graphe(position_joueurs, self.état['murs']['horizontaux'],
            self.état['murs']['verticaux'])

        pos_x = self.état['joueurs'][joueur]['pos'][0]
        pos_y = self.état['joueurs'][joueur]['pos'][1]

        if tuple(position) not in list(graphe.successors((pos_x, pos_y))):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

        self.état['joueurs'][joueur]['pos'] = position

    def placer_un_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (List[int, int]): la liste [x, y] de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """


        #Vérifier si le numéro du joueur est autre que 1 ou 2.
        if not joueur in (1, 2):
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        #Vérifier si un mur occupe déjà cette position (horizontal).
        if orientation == 'horizontal':
            for mur in self.état['murs']['horizontaux']:
                if position[1] == mur[1] and (position[0] == mur[0] or +\
                position[0] + 1 == mur[0] or position[0] == mur[0] + 1):
                    raise QuoridorError('Un mur occupe déjà cette position.')
            for mur in self.état['murs']['verticaux']:
                if position[0] + 1 == mur[0] and position[1] == mur[1] + 1:
                    raise QuoridorError('Un mur occupe déjà cette position.')

        #Vérifier si un mur occupe déjà cette position (vertical).
        if orientation == 'vertical':
            for mur in self.état['murs']['verticaux']:
                if position[0] == mur[0] and (position[1] == mur[1] or +\
                position[1] + 1 == mur[1] or position[1] == mur[1] + 1):
                    raise QuoridorError('Un mur occupe déjà cette position.')

            for mur in self.état['murs']['horizontaux']:
                if position[0] == mur[0] + 1 and position[1] + 1 == mur[1]:
                    raise QuoridorError('Un mur occupe déjà cette position.')

        #Vérifier si la position es t invalide pour cette orientation.
        if orientation == 'horizontal':
            if position[0] < 1 or position[0] > 8:
                raise QuoridorError('La position est invalide pour cette orientation.')
            if position[1] < 2 or position[1] > 9:
                raise QuoridorError('La position est invalide pour cette orientation.')

        if orientation == 'vertical':
            if position[0] < 2 or position[0] > 9:
                raise QuoridorError('La position est invalide pour cette orientation.')
            if position[1] < 1 or position[1] > 8:
                raise QuoridorError('La position est invalide pour cette orientation.')

        #Vérifier si le joueur a déjà placé tous ses murs.
        if self.état['joueurs'][joueur - 1]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')


        #Ajoute un mur à la liste de murs (soit vertical ou horizontal)
        if orientation == 'horizontal':
            self.état['murs']['horizontaux'].append(position)
        else:
            self.état['murs']['verticaux'].append(position)

        #Vérifier si les murs emprisonnent un joueur.
        position_joueurs = []

        for i in self.état['joueurs']:
            position_joueurs.append(i['pos'])

        graphe = construire_graphe(position_joueurs,
            self.état['murs']['horizontaux'], self.état['murs']['verticaux'])

        pos_x_1 = self.état['joueurs'][0]['pos'][0]
        pos_y_1 = self.état['joueurs'][0]['pos'][1]
        pos_x_2 = self.état['joueurs'][1]['pos'][0]
        pos_y_2 = self.état['joueurs'][1]['pos'][1]

        if nx.has_path(graphe, (pos_x_1, pos_y_1), 'B1') is False:
            if orientation == 'horizontal':
                self.état['murs']['horizontaux'] = self.état['murs']['horizontaux'][:-1]
            else:
                self.état['murs']['verticaux'] = self.état['murs']['verticaux'][:-1]
            raise QuoridorError('Un joueur est emprisonné par les murs.')

        if nx.has_path(graphe, (pos_x_2, pos_y_2), 'B2') is False:
            if orientation == 'horizontal':
                self.état['murs']['horizontaux'] = self.état['murs']['horizontaux'][:-1]
            else:
                self.état['murs']['verticaux'] = self.état['murs']['verticaux'][:-1]
            raise QuoridorError('Un joueur est emprisonné par les murs.')

        #Soustrait un mur au joueur
        self.état['joueurs'][joueur - 1]['murs'] -= 1

    def jouer_le_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.

        Returns:
            Tuple[str, List[int, int]]: Un tuple composé du type et de la position du coup joué.

        Strategie
            1. Regarder shortest_path pour chaque joueurs
            2. Si le serveur a une path plus court placer un mur
            (S'assurer de ne pas placer un mur ou il y en a deja un)
            3. Si le joueur a une path plus court deplacer le joueur
        """

        if not joueur in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        if self.est_terminée() is not False:
            raise QuoridorError("La partie est déjà terminée.")

        position_joueurs = []

        for i in self.état['joueurs']:
            position_joueurs.append(i['pos'])

        graphe = construire_graphe(position_joueurs,
            self.état['murs']['horizontaux'], self.état['murs']['verticaux'])

        paths = []

        for i, j in enumerate(self.état['joueurs']):
            pos_x = j['pos'][0]
            pos_y = j['pos'][1]

            paths.append(nx.shortest_path(graphe, (pos_x,pos_y), f'B{i+1}')[:-1])

        i = 1

        if len(paths[0]) > len(paths[1]) and (len(paths[0]) - len(paths[1]) > 2):
            next_move = paths[1][i]
            pos_mur = list(next_move)

            #Test si mouvement horizontal
            if paths[1][0][0] - next_move[0] != 0:
                pos_mur[1] -= 1
                #placer mur vertical
                while True:

                    try:
                        self.placer_un_mur(joueur,
                        pos_mur,
                        'vertical')

                        type_coup = 'MV'
                        pos =  pos_mur

                    except QuoridorError as e:
                        if str(e) == 'Un mur occupe déjà cette position.':

                            i += 1
                            pos_mur = list(paths[1][i])

                        else:
                            self.déplacer_jeton(joueur, paths[0][1])
                            type_coup = 'D'
                            pos = paths[0][1]
                            break
                        continue
                    break
            else:
                #placer mur horizontal
                while True:

                    try:
                        self.placer_un_mur(joueur,
                        pos_mur,
                        'horizontal')

                        type_coup = 'MH'
                        pos =  pos_mur

                    except QuoridorError as e:
                        if str(e) == 'Un mur occupe déjà cette position.':

                            i += 1
                            pos_mur = list(paths[1][i])

                        else:
                            self.déplacer_jeton(joueur, paths[0][1])
                            type_coup = 'D'
                            pos = paths[0][1]
                            break
                        continue
                    break

        else:
            self.déplacer_jeton(joueur, paths[0][1])
            type_coup = 'D'
            pos = paths[0][1]
        return (type_coup, pos)

if __name__ == "__main__":
    etat = {
            "joueurs": [
                {"nom": "Alfred", "murs": 10, "pos": [5, 1]},
                {"nom": "Robin", "murs": 10, "pos": [5, 9]},
            ],
            "murs": {},
        }

    quoridor = Quoridor(etat['joueurs'], etat['murs'])
    quoridor.jouer_le_coup(1)
