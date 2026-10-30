import telebot
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ Sentinel Core Bot Online! Aguardando comandos...")

@bot.message_handler(commands=['status'])
def send_status(message):
    # Aqui ele poderia ler os dados do psutil futuramente
    bot.reply_to(message, "Servidor Online. Nenhum ataque recente detectado.")

if __name__ == '__main__':
    print("Bot Sentinel Core rodando...")
    bot.polling()