from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar_banco():
    return sqlite3.connect("banco.db")

def criar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            local TEXT NOT NULL,
            contato TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente'
        )
    """)

    conexao.commit()
    conexao.close()

@app.route("/")
def index():
    filtro = request.args.get("filtro", "Todos")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if filtro == "Todos":
        cursor.execute("SELECT * FROM itens ORDER BY id DESC")
    else:
        cursor.execute(
            "SELECT * FROM itens WHERE tipo = ? ORDER BY id DESC",
            (filtro,)
        )

    itens = cursor.fetchall()
    conexao.close()

    return render_template("index.html", itens=itens, filtro=filtro)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    tipo = request.form["tipo"]
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    local = request.form["local"]
    contato = request.form["contato"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO itens (tipo, nome, descricao, local, contato)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, nome, descricao, local, contato))

    conexao.commit()
    conexao.close()

    return redirect("/")

@app.route("/resolver/<int:id>")
def resolver(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE itens SET status = 'Resolvido' WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
