import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

GROQ_API_KEY = "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"
TELEGRAM_BOT_TOKEN = "8830581649:AAEIqBR9vDW670zpjqaGVbbM6qwfCFERneM"

WORKING_MODELS = [
    "groq/compound-mini",
    "openai/gpt-oss-20b"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! البوت متصل وجاهز للرد.")

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    reply_found = False
    
    for model_name in WORKING_MODELS:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 500
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                ai_text = data['choices'][0]['message']['content']
                await update.message.reply_text(ai_text)
                reply_found = True
                break
        except Exception:
            continue

    if not reply_found:
        await update.message.reply_text("عذراً، يتعذر الحصول على رد حالياً.")

if __name__ == '__main__':
    request = HTTPXRequest(connect_timeout=20, read_timeout=20)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).request(request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    
    app.run_polling()
  
