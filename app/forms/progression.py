from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    NumberRange
)


class ProgressionForm(FlaskForm):

    sourate = StringField(
        "Sourate",
        validators=[DataRequired()]
    )


    nombre_versets = IntegerField(
        "Nombre de versets",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )


    date_evaluation = DateField(
        "Date évaluation",
        validators=[DataRequired()]
    )


    observations = StringField(
        "Observations"
    )


    talibe_matricule = SelectField(
        "Talibé",
        validators=[DataRequired()]
    )


    submit = SubmitField(
        "Enregistrer"
    )