import os
from flask import Flask
from threading import Thread

# 1. Servidor web falso para o Render não dar erro de porta
app = Flask('')

@app.route('/')
def home():
    return "Bot está online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ==========================================
# 2. COLE TODO O RESTO DO SEU CÓDIGO ANTIGO AQUI
# (Suas 200+ linhas com o Token, bot, handlers, Pix, etc.)
# ==========================================
import telebot
from telebot import types

# ==========================
# CONFIGURAÇÕES (ALTERE AQUI)
# ==========================

TOKEN = "8719924690:AAH9tzDmztgBGFiq9iT4PERKFoy0eIjZXf4"
ADMIN_ID = 8577165097  # O seu ID numérico do Telegram
ID_GRUPO_VIP = - 1003314477346  # ID do seu Grupo VIP (o bot precisa ser admin lá)
CHAVE_PIX = "e41ef017-2eb7-460e-aa78-49a34a1f9f92"  # A sua chave Pix

bot.send_video(message.chat.id, "8577165097", caption="Assista ao vídeo de demonstração")

bot = telebot.TeleBot(TOKEN)

# ==========================
# MENU INICIAL (/start)
# ==========================

@bot.message_handler(commands=['start'])
def start(message):
    teclado = types.ReplyKeyboardMarkup(resize_keyboard=True)
    teclado.add("🛒 Comprar Acesso VIP")

    bot.send_message(
        message.chat.id,
        "👋 **Bem-vindo ao Bot de Vendas!**\n\nClique no botão abaixo para ver os planos disponíveis.",
        reply_markup=teclado,
        parse_mode="Markdown"
    )

# ==========================
# MENU DE COMPRA E VÍDEO
# ==========================

@bot.message_handler(func=lambda m: m.text == "🛒 Comprar Acesso VIP")
def comprar(message):
    try:
        with open(VIDEO_PATH, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="🎥 Assista ao vídeo de demonstração antes de escolher o seu plano."
            )
    except:
        pass

    teclado = types.InlineKeyboardMarkup()
    teclado.add(types.InlineKeyboardButton("🗓️ Plano Semanal - R$ 4,50", callback_data="plano_semanal"))
    teclado.add(types.InlineKeyboardButton("📅 Plano Mensal - R$ 9,75", callback_data="plano_mensal"))
    teclado.add(types.InlineKeyboardButton("♾️ Plano Vitalício - R$ 14,50", callback_data="plano_vitalicio"))

    bot.send_message(
        message.chat.id,
        "📦 **Escolha o plano ideal para si:**",
        reply_markup=teclado,
        parse_mode="Markdown"
    )

# ==========================
# EXIBIÇÃO DA CHAVE PIX
# ==========================

@bot.callback_query_handler(func=lambda call: call.data.startswith("plano_"))
def planos(call):
    if call.data == "plano_semanal":
        nome_plano, valor = "Plano Semanal", "R$ 4,50"
    elif call.data == "plano_mensal":
        nome_plano, valor = "Plano Mensal", "R$ 9,75"
    else:
        nome_plano, valor = "Plano Vitalício", "R$ 14,50"

    bot.answer_callback_query(call.id, f"Selecionado: {nome_plano}")

    texto = f"""
✅ **{nome_plano}**

💵 **Valor:** {valor}

💰 **Chave Pix (Copia e Cola):**
<code>{CHAVE_PIX}</code>

📤 **Como proceder:**
1. Copie a chave Pix acima e faça o pagamento no aplicativo do seu banco.
2. Tire print da tela ou salve o comprovante.
3. **Envie o comprovante aqui no chat** (como foto ou documento PDF).

Assim que o pagamento for conferido, o seu link de acesso será enviado!
"""

    bot.send_message(
        call.message.chat.id,
        texto,
        parse_mode="HTML"
    )

# ==========================
# RECEBER COMPROVANTE (FOTO OU DOCUMENTO)
# ==========================

@bot.message_handler(content_types=["photo", "document"])
def receber_comprovante(message):
    bot.forward_message(
        ADMIN_ID,
        message.chat.id,
        message.message_id
    )
    
    bot.send_message(
        ADMIN_ID,
        f"📩 **Novo comprovante recebido!**\nID do Utilizador: `{message.chat.id}`\n\n_Para aprovar, responda a esta mensagem com `/aprovar`._\n_Para rejeitar, responda com `/rejeitar`._",
        parse_mode="Markdown"
    )

    bot.reply_to(
        message,
        "✅ **Comprovante recebido com sucesso!**\n\nAguarde um momento enquanto conferimos o pagamento.",
        parse_mode="Markdown"
    )

# ==========================
# COMANDOS DO ADMIN (APROVAR / REJEITAR)
# ==========================

@bot.message_handler(commands=['aprovar'])
def aprovar_pagamento(message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.reply_to_message:
        try:
            if message.reply_to_message.forward_from:
                cliente_id = message.reply_to_message.forward_from.id
            else:
                cliente_id = message.reply_to_message.chat.id
        except:
            bot.reply_to(message, "⚠️ Não foi possível identificar o cliente desta mensagem.")
            return

        try:
            link_convite = bot.create_chat_invite_link(
                chat_id=ID_GRUPO_VIP,
                member_limit=1
            )

            bot.send_message(
                cliente_id,
                f"🎉 **Pagamento Aprovado com Sucesso!**\n\nAqui está o seu link de acesso exclusivo para o Grupo VIP:\n\n{link_convite.invite_link}\n\n⚠️ _Este link é individual e só pode ser utilizado uma única vez._",
                parse_mode="Markdown"
            )

            bot.reply_to(message, "✅ Pagamento aprovado e link enviado para o cliente com sucesso!")

        except Exception as e:
            bot.reply_to(message, f"❌ Erro ao gerar o link de convite. Verifique se o bot é administrador do grupo VIP. Erro: {e}")
    else:
        bot.reply_to(message, "⚠️ Você precisa usar o comando **Responder (Reply)** em cima do comprovante do cliente e digitar `/aprovar`.")

@bot.message_handler(commands=['rejeitar'])
def rejeitar_pagamento(message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.reply_to_message:
        try:
            if message.reply_to_message.forward_from:
                cliente_id = message.reply_to_message.forward_from.id
            else:
                cliente_id = message.reply_to_message.chat.id
        except:
            bot.reply_to(message, "⚠️ Não foi possível identificar o cliente.")
            return

        try:
            bot.send_message(
                cliente_id,
                "❌ **Comprovante Recusado ou Inválido.**\n\nO pagamento não foi confirmado ou o comprovante enviado não é válido. Verifique os dados e tente novamente ou entre em contato com o suporte.",
                parse_mode="Markdown"
            )

            bot.reply_to(message, "🚫 Comprovante rejeitado e aviso enviado ao cliente.")
        except Exception as e:
            bot.reply_to(message, f"❌ Erro ao enviar mensagem para o cliente: {e}")
    else:
        bot.reply_to(message, "⚠️ Você precisa usar o comando **Responder (Reply)** em cima do comprovante e digitar `/rejeitar`.")

# ==========================
# MENSAGENS DESCONHECIDAS
# ==========================

@bot.message_handler(func=lambda m: True)
def desconhecido(message):
    if message.chat.id == ADMIN_ID:
        return

    bot.send_message(
        message.chat.id,
        "⚠️ Use o botão **🛒 Comprar Acesso VIP** no menu inferior para iniciar.",
        parse_mode="Markdown"
    )

# ==========================
# INICIAR BOT
# ==========================

print("-----------------------------------")
print("🤖 Bot manual com /aprovar rodando!")
print("-----------------------------------")

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30
          )
