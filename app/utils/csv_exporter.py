"""
Utilitaire d'export CSV, partagé par toutes les vues (Maitre, Classe,
Talibe, Progression). Génère une réponse HTTP téléchargeable.
"""
import csv
import io
from flask import make_response


def exporter_csv(nom_fichier: str, entetes: list, lignes: list):
    """
    Construit une réponse Flask contenant un fichier CSV téléchargeable.

    :param nom_fichier: nom du fichier proposé au téléchargement (ex: 'maitres.csv')
    :param entetes: liste des noms de colonnes (ligne d'en-tête)
    :param lignes: liste de listes/tuples, une par enregistrement
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(entetes)
    for ligne in lignes:
        writer.writerow(ligne)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={nom_fichier}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response
