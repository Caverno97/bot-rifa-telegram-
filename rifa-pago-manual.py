from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json, os, random

TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
DB_FILE = "participantes.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        participantes = json.load(f)
else:
    participantes = {}

def start(update, context):
    msg = (
        "🎉 *Bienvenido al Bot de Rifas* 🎉\n\n"
        "💳 Transfiere $5 a:\n"
        "`Carlos Cabrera`\n"
        "`Banco Ejemplo`\n"
        "`1234 5678 9012 3456`\n\n"
        "📤 Luego envía comprobante como texto o foto.\n"
        "✅ Usa /registrarme para entrar."
    )
    update.message.reply_text(msg, parse_mode='Markdown')

def recibir_comprobante(update, context):
    user = update.effective_user
    if update.message.text or update.message.photo:
        info = f"📩 Comprobante de {user.username or user.first_name} (ID: {user.id})"
        context.bot.send_message(chat_id=ADMIN_ID, text=info)
        update.message.forward(chat_id=ADMIN_ID)
        update.message.reply_text("✅ Comprobante enviado.")
    else:
        update.message.reply_text("❌ Envía texto o foto como comprobante.")

def registrarme(update, context):
    user = update.effective_user
    uid = str(user.id)
    name = user.username or user.first_name
    if uid in participantes:
        update.message.reply_text("✅ Ya estás registrado.")
    else:
        participantes[uid] = name
        with open(DB_FILE, "w") as f:
            json.dump(participantes, f)
        update.message.reply_text(f"🎟 Registrado, {name}!")

def participantes_list(update, context):
    if not participantes:
        update.message.reply_text("❌ No hay participantes.")
    else:
        text = "\n".join(participantes.values())
        update.message.reply_text(f"🎟 Participantes:\n{text}")

def sortear(update, context):
    if not participantes:
        update.message.reply_text("❌ No hay participantes.")
    else:
        winner = random.choice(list(participantes.values()))
        update.message.reply_text(f"🏆 El ganador es: {winner} 🎉")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("registrarme", registrarme))
    dp.add_handler(CommandHandler("participantes", participantes_list))
    dp.add_handler(CommandHandler("sortear", sortear))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, recibir_comprobante))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
