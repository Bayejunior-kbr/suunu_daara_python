import click
from flask.cli import with_appcontext
from app.extension import db
from app.models.user import User

@click.command("create-admin")
@click.argument("nom_utilisateur")
@click.argument("mot_de_passe")
@with_appcontext
def create_admin(nom_utilisateur, mot_de_passe):
    if User.query.filter_by(nom_utilisateur=nom_utilisateur).first():
        click.echo("Cet utilisateur existe déjà.")
        return
    admin = User(nom_utilisateur=nom_utilisateur, role="admin")
    admin.set_password(mot_de_passe)
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Admin '{nom_utilisateur}' créé avec succès.")