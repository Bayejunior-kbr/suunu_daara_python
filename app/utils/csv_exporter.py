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


def exporter_progressions_csv(progressions):
    """
    Export CSV dédié au module Progression (travail d'Astou).
    Conservé tel quel (délimiteur ';', colonnes spécifiques) plutôt que
    fusionné dans exporter_csv() pour ne pas casser sa vue déjà fonctionnelle.
    """
    from flask import Response

    output = io.StringIO()

    writer = csv.writer(output, delimiter=";")

    # En-têtes
    writer.writerow([
        "ID",
        "Talibe",
        "Sourate",
        "Nombre versets",
        "Date evaluation",
        "Observations",
    ])

    # Données
    for p in progressions:
        writer.writerow([
            p.id,
            f"{p.talibe.prenom} {p.talibe.nom}",
            p.sourate,
            p.nombre_versets,
            p.date_evaluation,
            p.observations,
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=progressions.csv"

    return response
