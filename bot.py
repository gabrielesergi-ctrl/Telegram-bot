import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Legge le variabili ambiente
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# Cartella dove salvare i video
VIDEO_DIR = "videos"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# Lista dei video salvati
def lista_video():
    return [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo bot. Puoi caricare MP4, usare /lista e /cerca <titolo>.")

# Comando /lista
async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    videos = lista_video()
    if videos:
        await update.message.reply_text("Video disponibili:\n" + "\n".join(videos))
    else:
        await update.message.reply_text("Nessun video disponibile.")

# Comando /cerca <titolo>
async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usa: /cerca <titolo>")
        return
    query = " ".join(context.args).lower()
    results = [v for v in lista_video() if query in v.lower()]
    if results:
        await update.message.reply_text("Risultati trovati:\n" + "\n".join(results))
    else:
        await update.message.reply_text("Nessun video trovato con quel titolo.")

# Gestione upload MP4 (solo admin)
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Solo l'admin può caricare video.")
        return
    file = await update.message.video.get_file()
    path = os.path.join(VIDEO_DIR, update.message.video.file_name)
    await file.download_to_drive(path)
    await update.message.reply_text(f"Video {update.message.video.file_name} salvato!")

# Funzione principale
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(CommandHandler("cerca", cerca))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("🤖 Bot in esecuzione...")
    app.run_polling()

if __name__ == "__main__":
    main()
