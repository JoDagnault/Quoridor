""" Module de la classe QuoridorX

Classes:
    * QuoridorX - Classe pour encapsuler et afficher le jeu quoridor
"""
import turtle
import math
from quoridor import Quoridor

class QuoridorX(Quoridor):
    """Classe pour encapsuler et afficher le jeu quoridor

    Attributes:
        état (dict) : état du jeu tenu à jour.
    """

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe QuoridorX.

        Fait appel au constructeur de la classe Quoridor.

        Fait les vérifications nécessaires et initialise l'état

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
        """

        Quoridor.__init__(self, joueurs, murs)

        #Initialisation de la fenetre
        self.fen = turtle.Screen()
        self.fen.title("Quoridor")
        self.fen.setup(width=1100, height=800)

        #Met l"origine (0,0) au coin en haut a gauche
        #Il ya toujours un espace de 10 pixel a gauche et en haut de la fenetre
        self.fen.setworldcoordinates(0, 800, 1100, 0)

        self.affichage()

        #Doit etre le dernier argument de la fonction
        #Garde la fenetre ouvert
        #turtle.mainloop()

    def affichage(self):
        """Affichage graphique de l'état de jeu
            Inspiration :
                http://modelai.gettysburg.edu/2014/mpgames/website.html
        """

        pen = turtle.Turtle()
        turtle.tracer(0)
        pen.ht()

        #dessine une case du damier
        def dessine_case():
            """Dessine une case du damier
            """
            for _ in range(4):
                pen.down()
                pen.forward(70)
                pen.left(90)
                pen.up()

        pen.up()
        pen.setpos(30,30)
        pen.down()

        #boucle pour dessiner contour damier
        for _ in range(4):
            pen.forward(730)
            pen.left(90)

        #boucle pour ecrire numero lignes
        for ligne in range(9):
            pen.up()
            pen.setpos(10, (720/9) * (9 - ligne) + 10)
            pen.write(f"{ligne + 1}", font="10")

        #boucle pour ecrire numero colonne
        for colonne in range(9):
            pen.up()
            pen.setpos((720/9) * (colonne + 1) - 10, 790)
            pen.write(f"{colonne + 1}", font="10")

        #boucle pour dessiner le damier
        for ligne in range(9):
            for colonne in range(9):

                pen.up()
                pen.setpos(40 + math.ceil(720/9 * colonne), 40 + math.ceil(720/9 * ligne))

                if ligne == 0:
                    col = 'blue'
                elif ligne == 8:
                    col = 'red'
                else:
                    col = 'white'

                pen.fillcolor(col)
                pen.begin_fill()
                dessine_case()
                pen.end_fill()

        #boucle pour dessin joueurs
        for i, joueur in enumerate(self.état['joueurs']):
            pos_x, pos_y = joueur['pos']
            rayon = 25

            pos_x = 30 + 70 * (pos_x - 1) + 10 * pos_x + 0.5 * 70
            pos_y = 770 - 70 * pos_y - 10 * (pos_y + 1) + rayon/2

            pen.setpos(pos_x, pos_y)


            if self.est_terminée() == joueur['nom']:
                col = 'lime'
            elif i == 0:
                col = 'blue'
            elif i == 1:
                col = 'red'

            pen.fillcolor(col)
            pen.begin_fill()
            pen.down()
            pen.circle(rayon)
            pen.end_fill()
            pen.up()

        def dessine_mur_horizontal():
            """Dessine un mur horizontal
            """
            for _ in range(2):
                pen.forward(70*2+10)
                pen.right(90)
                pen.forward(10)
                pen.right(90)

        #boucle pour dessiner murs horizontaux
        for _, mur in enumerate(self.état['murs']['horizontaux']):
            pos_x, pos_y = mur

            pos_x = 30 + 10 * pos_x + 70 * (pos_x - 1)
            pos_y = 770 - 10 * pos_y - 70 * (pos_y - 1)

            pen.setpos(pos_x, pos_y)

            pen.fillcolor('grey')
            pen.begin_fill()
            pen.down()

            dessine_mur_horizontal()

            pen.end_fill()
            pen.up()

        def dessine_mur_vertical():
            """Dessine un mur vertical
            """
            for _ in range(2):
                pen.forward(10)
                pen.right(90)
                pen.forward(70*2+10)
                pen.right(90)

        #boucle pour dessiner murs verticaux
        for _, mur in enumerate(self.état['murs']['verticaux']):
            pos_x, pos_y = mur

            pos_x = 30 + 10 * (pos_x - 1) + 70 * (pos_x - 1)
            pos_y = 770 - 10 * (pos_y + 1) - 70 * (pos_y - 1)

            pen.setpos(pos_x, pos_y)

            pen.fillcolor('grey')
            pen.begin_fill()
            pen.down()

            dessine_mur_vertical()

            pen.end_fill()
            pen.up()

        #Dessin legende

        pen.setpos(770, 300)
        pen.write(self.formater_légende(), move=True, font='20')

    def afficher(self):
        """Met a jour la representation graphique
        """
        self.fen.clear()
        self.affichage()
        self.fen.update()
