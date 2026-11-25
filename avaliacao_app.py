
import os
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_bootstrap import Bootstrap


# CONFIGURAÇÕES

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "avaliacao.db")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "troque-esta-chave-antes-de-publicar"
)

app.config["STUDENT_NAME"] = os.environ.get(
    "STUDENT_NAME",
    "Fabio Teixeira"
)

app.config["STUDENT_RECORD"] = os.environ.get(
    "STUDENT_RECORD",
    "PT23820X"
)

Bootstrap(app)


# DISCIPLINAS DOS PROFESSORES

DISCIPLINES = ["DSWA5", "IHCA5", "SODA5", "PJIA5"]


# CONEXÃO COM O BANCO

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CRIAÇÃO DAS TABELAS

def init_db():

    with get_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                disciplina TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina TEXT NOT NULL,
                semestre INTEGER NOT NULL
            )
        """)

        # Cadastro inicial de professores

        count = conn.execute(
            "SELECT COUNT(*) FROM professores"
        ).fetchone()[0]

        if count == 0:

            sample = [
                ("Fabio Teixeira", "DSWA5"),
                ("Professor Fabio Teixeira", "IHCA5"),
                ("Professor André Rufino", "SODA5"),
                ("Marcos", "DSWA5"),
                ("Rosana", "IHCA5"),
                ("fabio", "DSWA5"),
                ("TesteProf123", "DSWA5"),
                ("Professor 1", "PJIA5"),
                ("Mario", "SODA5"),
                ("asfsaf", "DSWA5"),
            ]

            conn.executemany(
                """
                INSERT INTO professores (nome, disciplina)
                VALUES (?, ?)
                """,
                sample
            )


# INICIALIZAR BANCO

init_db()


# INFORMAÇÕES COMPARTILHADAS

@app.context_processor
def inject_common_data():

    return {
        "student_name": app.config["STUDENT_NAME"],
        "student_record": app.config["STUDENT_RECORD"],
        "local_datetime": datetime.now().astimezone().strftime(
            "%B %d, %Y %I:%M %p"
        ),
    }


# PÁGINA PRINCIPAL

@app.route("/")
def index():

    return render_template("index.html")


# CADASTRO DE PROFESSORES

@app.route("/professores", methods=["GET", "POST"])
def professores():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        disciplina = request.form.get("disciplina", "").strip()

        if not nome:

            flash("Informe o nome do professor.", "danger")

        elif disciplina not in DISCIPLINES:

            flash("Selecione uma disciplina válida.", "danger")

        else:

            with get_db() as conn:

                conn.execute(
                    """
                    INSERT INTO professores (nome, disciplina)
                    VALUES (?, ?)
                    """,
                    (nome, disciplina)
                )

            flash(
                "Professor cadastrado com sucesso!",
                "success"
            )

            return redirect(url_for("professores"))

    with get_db() as conn:

        lista = conn.execute(
            """
            SELECT nome, disciplina
            FROM professores
            ORDER BY id
            """
        ).fetchall()

    return render_template(
        "professores.html",
        professores=lista,
        disciplines=DISCIPLINES
    )


# CADASTRO DE DISCIPLINAS

@app.route("/disciplinas", methods=["GET", "POST"])
def disciplinas():

    if request.method == "POST":

        nome = request.form.get(
            "disciplina", ""
        ).strip()

        semestre = request.form.get(
            "semestre", ""
        ).strip()

        if not nome:

            flash(
                "Informe o nome da disciplina.",
                "danger"
            )

        elif semestre not in ["1", "2", "3", "4", "5", "6"]:

            flash(
                "Selecione um semestre válido.",
                "danger"
            )

        else:

            try:

                with get_db() as conn:

                    conn.execute(
                        """
                        INSERT INTO disciplinas
                        (disciplina, semestre)
                        VALUES (?, ?)
                        """,
                        (nome, int(semestre))
                    )

                flash(
                    "Disciplina cadastrada com sucesso!",
                    "success"
                )

                return redirect(url_for("disciplinas"))

            except sqlite3.Error:

                flash(
                    "Erro ao cadastrar a disciplina.",
                    "danger"
                )

    with get_db() as conn:

        lista_disciplinas = conn.execute(
            """
            SELECT disciplina, semestre
            FROM disciplinas
            ORDER BY id
            """
        ).fetchall()

    return render_template(
        "disciplinas.html",
        disciplinas=lista_disciplinas
    )


# ERRO 404

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "error.html",
        code=404,
        message="Página não encontrada."
    ), 404


# ERRO 500

@app.errorhandler(500)
def internal_error(error):

    return render_template(
        "error.html",
        code=500,
        message="Ocorreu um erro interno. Tente novamente."
    ), 500


# EXECUTAR A APLICAÇÃO

if __name__ == "__main__":

    app.run(debug=True)
