"""quoridor Quoridor

Ce programme permet de joueur au quoridor Quoridor.
"""
from api import débuter_partie, jouer_coup
from quoridor import Quoridor
from utilitaire import analyser_commande
from quoridorx import QuoridorX

# Mettre ici votre secret récupéré depuis le site de PAX
SECRET = "51b83499-4716-4a14-86f0-801cb99d7ae2"

if __name__ == "__main__":
    args = analyser_commande()
    id_partie, état = débuter_partie(args.idul, SECRET)

    if args.graphique:

        quoridor = QuoridorX(état['joueurs'])

        if args.automatique:

            while True:
                #Afficher partie
                quoridor.afficher()

                #Test si partie terminer
                if quoridor.est_terminée() is not False:
                    print("Le gagnant est : " + quoridor.est_terminée())
                    break

                # Joue le meilleur coup
                type_coup, position = quoridor.jouer_le_coup(1)

                # Envoyez le coup au serveur
                id_partie, quoridor.état = jouer_coup(
                    id_partie,
                    type_coup,
                    position,
                    args.idul,
                    SECRET,
                )

        else:

            while True:

                #Afficher partie
                quoridor.afficher()

                if quoridor.est_terminée() is not False:
                    print("Le gagnant est : " + quoridor.est_terminée())
                    break

                # Demander au joueur de choisir son prochain coup
                type_coup, position = quoridor.récupérer_le_coup(1)

                if type_coup == 'D':
                    quoridor.déplacer_jeton(1, position)

                if type_coup == 'MH':
                    quoridor.placer_un_mur(1, position, 'horizontal')

                if type_coup == 'MV':
                    quoridor.placer_un_mur(1, position, 'vertical')

                # Envoyez le coup au serveur
                id_partie, quoridor.état = jouer_coup(
                    id_partie,
                    type_coup,
                    position,
                    args.idul,
                    SECRET,
                )


    else:
        quoridor = Quoridor(état['joueurs'])

        if args.automatique:
            while True:
                #Afficher partie
                print(quoridor.__str__())

                #Test si partie terminer
                if quoridor.est_terminée() is not False:
                    print("Le gagnant est : " + quoridor.est_terminée())
                    break

                # Joue le meilleur coup
                type_coup, position = quoridor.jouer_le_coup(1)

                # Envoyez le coup au serveur
                id_partie, quoridor.état = jouer_coup(
                    id_partie,
                    type_coup,
                    position,
                    args.idul,
                    SECRET,
                )

        else:

            while True:

                #Afficher partie
                print(quoridor.__str__())

                if quoridor.est_terminée() is not False:
                    print("Le gagnant est : " + quoridor.est_terminée())
                    break

                # Demander au joueur de choisir son prochain coup
                type_coup, position = quoridor.récupérer_le_coup(1)

                if type_coup == 'D':
                    quoridor.déplacer_jeton(1, position)

                if type_coup == 'MH':
                    quoridor.placer_un_mur(1, position, 'horizontal')

                if type_coup == 'MV':
                    quoridor.placer_un_mur(1, position, 'vertical')

                # Envoyez le coup au serveur
                id_partie, quoridor.état = jouer_coup(
                    id_partie,
                    type_coup,
                    position,
                    args.idul,
                    SECRET,
                )
