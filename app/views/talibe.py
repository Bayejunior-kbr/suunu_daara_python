from flask import Blueprint, render_template, flash, redirect, url_for, request,Response
import io
import csv

from app.extension import db
from app.models.talibe import Talibe
from app.forms.talibe import TalibeForm

from app.models.classe import Classe

talibes_bp=Blueprint("talibe",__name__,url_prefix="/talibes")

def classe_choix(form):
    """listes deroulant du classe"""
    form.classe_id.choices=[(c.id,c.nom) for c in Classe.query.all()]
#lister
@talibes_bp.route("/")
def liste():#pour liste les talibes
    talibes=Talibe.query.all()
    return render_template("talibes/liste.html",talibes=talibes)

# ajouter
@talibes_bp.route("/ajouter",methods=["GET","POST"])
def ajouter():
    form=TalibeForm()
    classe_choix(form)
     #validate_on_submil sa vien directement elle vient directement de Flask-WTF sa verifie est ce ke tous les champs sont verifier et est ce ke l'utilisateur vient de clique sur enregistre
    if form.validate_on_submit():
        talibe = Talibe(
            nom=form.nom.data,  #.data c'est l'attribut qui contient la vraie valeur que l'utilisateur a saisie ou choisie
            prenom=form.prenom.data,
            date_naissance=form.date_naissance.data,
            telephone_tuteur=form.telephone_tuteur.data,
            adresse=form.adresse.data,
            classe_id=form.classe_id.data,
        )
        db.session.add(talibe)
        db.session.commit()
        flash("Taibe enregistre avec !","success") #fait qu'enregistrer un message temporaire côté serveur (dans la session de l'utilisateur)
        return redirect(url_for("talibe.liste"))
    return render_template("talibes/formulaire.html",form=form,titre="ajouter un talibes")


@talibes_bp.route("/modifier/<int:id>",methods=["GET","POST"])
def modifier(id):
    talibe=Talibe.query.get_or_404(id) # cherche le talibes avec son id si introuvable eureur directe
    form=TalibeForm(obj=talibe) #cree le formulaire et le pre remplit avec les donnes du talibes
    classe_choix(form) #remplit le liste deroulant de classe

    if form.validate_on_submit(): #renvoi vrai si c'est post et les validator sont normals...
        talibe.nom=form.nom.data # mettre a jour les donner avec le nouveau nom saisit
        talibe.prenom=form.prenom.data
        talibe.date_naissance=form.date_naissance.data
        talibe.telephone_tuteur=form.date_naissance.data
        talibe.adresse=form.adresse.data
        talibe.classe_id=form.classe_id.data

        db.session.commit() #sauvegarder definitivement les modification en base de donne

        flash('talibe modifie avec succes !') #enregistre un message temporaire affiché après la redirection
        return redirect(url_for("talibe.liste"))
    return render_template("talibes/formulaire.html",form=form,titre="modifier un talibes")



@talibes_bp.route("/supprimer/<int:id>" , methods=["POST"])
def supprimer(id):
    talibe=Talibe.query.get_or_404(id) #recuprer l'etudiant a supprimer avec son id
    db.session.delete(talibe) # marquer pour etre supprimer
    db.session.commit()# le supprimer en base de donner reelement
    flash("talibes supprime avec succes !")
    return redirect(url_for("talibe.liste"))


@talibes_bp.route("/rechercher")
def rechercher():
    mot_cle=request.args.get("q","")
    talibes=Talibe.query.filter(Talibe.nom.contains(mot_cle)).all()
    return render_template("talibes/liste.html",talibes=talibes ,recherche=mot_cle)


@talibes_bp.route("/export")  # URL /talibes/export
def export_csv():
    talibes = Talibe.query.all()  # récupère TOUS les talibés de la base de données

    output = io.StringIO()  # crée un "fichier texte virtuel" en mémoire (pas sur le disque dur)
    writer = csv.writer(output)  # crée un "écrivain CSV" qui va écrire dans notre fichier virtuel "output"
    writer.writerow(["ID", "Nom", "Prénom", "Date de naissance", "Téléphone tuteur", "Adresse", "Classe"])
    # écrit la première ligne du CSV : les en-têtes de colonnes (titres)

    for t in talibes:  # on boucle sur chaque talibé récupéré
        writer.writerow([  # écrit UNE ligne CSV par talibé, avec les valeurs dans le même ordre que les en-têtes
            t.id, t.nom, t.prenom,
            t.date_naissance, t.telephone_tuteur, t.adresse,
            t.classe.nom if t.classe else ""
            # si le talibé a une classe (relation), on prend son nom ; sinon on met une chaîne vide (évite un crash si classe_id est manquant)
        ])

    return Response(  # on construit et renvoie une réponse HTTP spéciale
        output.getvalue(),  # récupère tout le contenu texte écrit dans notre "fichier virtuel"
        mimetype="text/csv",  # dit au navigateur : "ce que je t'envoie est un fichier CSV"
        headers={"Content-Disposition": "attachment; filename=talibes.csv"}
        # "attachment" force le navigateur à TÉLÉCHARGER le fichier au lieu de l'afficher dans la page
        # "filename=talibes.csv" donne le nom du fichier qui sera proposé au téléchargement
    )