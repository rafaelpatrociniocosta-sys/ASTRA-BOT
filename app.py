from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Caminhos
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Funções de banco ---
def salvar_mensagem(remetente, mensagem):
    conn = sqlite3.connect("cleiton_chat.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historico (remetente, mensagem) VALUES (?, ?)", (remetente, mensagem))
    conn.commit()
    conn.close()

def carregar_historico():
    conn = sqlite3.connect("cleiton_chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT remetente, mensagem FROM historico ORDER BY id ASC")
    mensagens = cursor.fetchall()
    conn.close()
    return mensagens

# --- Rotas ---
@app.route("/")
def index():
    mensagens = carregar_historico()
    return render_template("index.html", mensagens=mensagens)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg_user = data.get("message", "").strip()
    if not msg_user:
        return jsonify({"response": "Mensagem vazia."})
    
    salvar_mensagem("user", msg_user)

    # Aqui entra tua lógica de IA (resposta simples por enquanto)
    resposta = f"Entendido, você disse: {msg_user}"
    salvar_mensagem("assistant", resposta)

    return jsonify({"response": resposta})

@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"reply": "Nenhum arquivo enviado."})

    caminho = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(caminho)

    resposta = f"Arquivo '{file.filename}' recebido com sucesso."
    salvar_mensagem("user", f"Enviou o arquivo: {file.filename}")
    salvar_mensagem("assistant", resposta)
    return jsonify({"reply": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
