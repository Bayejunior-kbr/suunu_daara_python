import csv
from io import StringIO
from flask import Response


def exporter_progressions_csv(progressions):

    output = StringIO()

    writer = csv.writer(
        output,
        delimiter=";"
    )


    # En-têtes
    writer.writerow([
        "ID",
        "Talibe",
        "Sourate",
        "Nombre versets",
        "Date evaluation",
        "Observations"
    ])


    # Données
    for p in progressions:

        writer.writerow([
            p.id,
            f"{p.talibe.prenom} {p.talibe.nom}",
            p.sourate,
            p.nombre_versets,
            p.date_evaluation,
            p.observations
        ])


    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )


    response.headers["Content-Disposition"] = (
        "attachment; filename=progressions.csv"
    )


    return response