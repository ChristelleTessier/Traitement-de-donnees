def boucle_01():
    """
    Demande à l'utilisateur de réponse oui(1) et non(0).

    Returns:
        str: '1' si l'utilisateur veut zoomer, '0' sinon.
    """

    while True:
        rep = input("0 : non, 1: oui. Votre choix ?")
        if rep == '0' or rep == '1':
            # Réponse valide
            break
        else:
            print("Valeur saisie invalide (0 ou 1 attendu).")

    return rep

def sortie():
    return False
