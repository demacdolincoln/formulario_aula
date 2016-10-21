from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required, Optional
import dataset

################################################################################
#                           configurando o servidor                            #
################################################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = "UmaPalavraQualquer"

################################################################################
#                          configurando o formulario                           #
################################################################################
class Questionario_form(Form):
    nome = StringField("Nome: ", validators=[Optional()])
    
    _choices = [(str(i), i) for i in range(6)]
    p1 = RadioField("Comédia", choices=_choices, validators=[Required()]) 
    p2 = RadioField("ação", choices=_choices, validators=[Required()])
    p3 = RadioField("Terror", choices=_choices, validators=[Required()])
    p4 = RadioField("Suspense", choices=_choices, validators=[Required()])
    p5 = RadioField("Drama", choices=_choices, validators=[Required()])

    submit = SubmitField("Enviar")

################################################################################
#                         configurando a base de dados                         #
################################################################################
def database(resp):
    conn = dataset.connect("sqlite:///respostas.db")
    table = conn["respostas_teste"]
    try:
        table = conn.get_table("respostas_teste")
    except Exception as e:
        table = conn.create_table("respostas_teste")
    table.insert(resp)
    conn.commit()
    
################################################################################
#                             formatando a pagina                              #
################################################################################
@app.route("/", methods=["GET", "POST"])
def index():
    form = Questionario_form()
    if form.validate_on_submit():
        database(form.data)
        return render_template("ok.html")
    return render_template("index.html", form=form)

################################################################################
#                              iniciando o servidor                            #
################################################################################
if __name__ == '__main__':
    app.run(debug=True)
