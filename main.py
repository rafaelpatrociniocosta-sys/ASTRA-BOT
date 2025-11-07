import customtkinter as ctk
import google.generativeai as genai
import sqlite3
import datetime

# Configurações da API
genai.configure(api_key="AIzaSyAyP5B1-4W7icRFpx2seq52-0u_rICIlDg")
model = genai.GenerativeModel("gemini-2.0-flash")

# Banco de dados local
conn = sqlite3.connect("cleiton_chat.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remetente TEXT,
    mensagem TEXT,
    data TEXT
)
""")
conn.commit()

# Função pra salvar mensagens
def salvar_mensagem(remetente, mensagem):
    cursor.execute("INSERT INTO historico (remetente, mensagem, data) VALUES (?, ?, ?)",
                   (remetente, mensagem, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

# Função pra carregar histórico
def carregar_historico():
    cursor.execute("SELECT remetente, mensagem FROM historico ORDER BY id ASC")
    return cursor.fetchall()

# Enviar mensagem
def enviar():
    user_input = entrada.get().strip()
    if not user_input:
        return

    chatbox.insert("end", f"Você: {user_input}\n", "usuario")
    salvar_mensagem("Você", user_input)
    entrada.delete(0, "end")

    try:
        response = model.generate_content(user_input)
        resposta = response.text.strip()
    except Exception as e:
        resposta = f"Erro: {e}"

    chatbox.insert("end", f"Cleiton: {resposta}\n\n", "cleiton")
    salvar_mensagem("Cleiton", resposta)
    chatbox.see("end")

# Interface moderna
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

janela = ctk.CTk()
janela.title("Cleiton - Seu assistente IA")
janela.geometry("700x600")

chatbox = ctk.CTkTextbox(janela, width=680, height=480, wrap="word")
chatbox.pack(pady=10)
chatbox.tag_config("usuario", foreground="#00ffcc")
chatbox.tag_config("cleiton", foreground="#ffcc00")

# Carrega histórico anterior
for remetente, mensagem in carregar_historico():
    chatbox.insert("end", f"{remetente}: {mensagem}\n\n")

frame_inferior = ctk.CTkFrame(janela)
frame_inferior.pack(fill="x", padx=10, pady=10)

entrada = ctk.CTkEntry(frame_inferior, placeholder_text="Digite sua mensagem...", width=500)
entrada.pack(side="left", padx=10)
botao_enviar = ctk.CTkButton(frame_inferior, text="Enviar", command=enviar)
botao_enviar.pack(side="left")

janela.mainloop()
