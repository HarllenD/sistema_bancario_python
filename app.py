from flask import Flask, render_template, request, redirect, flash, session
from banco import *

app = Flask(__name__)
app.secret_key = "segredo"

criar_tabela()
criar_tabela_usuarios() 


if not login_usuario("admin", "123"):
    criar_usuario("admin", "123")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        user = login_usuario(nome, senha)

        if user:
            session["user_id"] = user[0]
            return redirect("/")
        else:
            flash("Login inválido")

    return render_template("login.html")


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    contas = listar_contas(session["user_id"])
    total = total_saldo()
    qtd = total_contas()

    nomes = [c[1] for c in contas]
    saldos = [c[2] for c in contas]

    return render_template(
        "index.html",
        contas=contas,
        total=total,
        qtd=qtd,
        nomes=nomes,
        saldos=saldos
    )


# ➕ CRIAR CONTA
@app.route("/criar", methods=["POST"])
def criar():
    if "user_id" not in session:
        return redirect("/login")

    nome = request.form["nome"]

    if nome == "":
        flash("Nome não pode ser vazio!")
    else:
        criar_conta(nome, session["user_id"])
        flash("Conta criada com sucesso!")

    return redirect("/")


@app.route("/depositar", methods=["POST"])
def depositar_web():
    if "user_id" not in session:
        return redirect("/login")

    try:
        id = int(request.form["id"])
        valor = float(request.form["valor"])

        if valor <= 0:
            flash("Valor inválido!")
        else:
            depositar(id, valor)
            flash("Depósito realizado!")

    except:
        flash("Erro no depósito!")

    return redirect("/")


@app.route("/sacar", methods=["POST"])
def sacar_web():
    if "user_id" not in session:
        return redirect("/login")

    try:
        id = int(request.form["id"])
        valor = float(request.form["valor"])

        if valor <= 0:
            flash("Valor inválido!")
        else:
            sacar(id, valor)
            flash("Saque realizado!")

    except:
        flash("Erro no saque!")

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]

        if nome == "" or senha == "":
            flash("Preencha todos os campos!")
        else:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
            existe = cursor.fetchone()

            conn.close()

            if existe:
                flash("Usuário já existe!")
            else:
                criar_usuario(nome, senha)
                flash("Conta criada! Faça login.")
                return redirect("/login")

    return render_template("cadastro.html")

app.run(debug=True)