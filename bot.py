import os
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler
from parser import parse_courses

app = FastAPI()

TOKEN = "8225066593:AAHjgyqPsqkvSNNm-H5z6B9NOYKJWX_v1pc"  # Aapka token yahan hardcoded hai (secure nahi, sirf testing ke liye)
WEBHOOK_PATH = '/webhook'

BOT_APPLICATION = Application.builder().token(TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Welcome to the Course Uploader Bot! Send /upload to upload courses from the text file.")

async def upload(update, context):
    try:
        courses = parse_courses('data/courses.txt')
        for course in courses:
            caption = f"Course: {course['title']}\nDescription: {course['description']}"
            path = course['path']
            if course['type'] == 'video':
                if path.startswith('http'):
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=path,
                        caption=caption
                    )
                elif os.path.exists(path):
                    with open(path, 'rb') as video:
                        await context.bot.send_video(
                            chat_id=update.effective_chat.id,
                            video=video,
                            caption=caption
                        )
                else:
                    await update.message.reply_text(f"Video not found: {path}")
            elif course['type'] == 'lecture':
                if path.startswith('http'):
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=path,
                        caption=caption
                    )
                elif os.path.exists(path):
                    with open(path, 'rb') as document:
                        await context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=document,
                            caption=caption
                        )
                else:
                    await update.message.reply_text(f"Document not found: {path}")
        await update.message.reply_text("All courses uploaded successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error uploading courses: {str(e)}")

BOT_APPLICATION.add_handler(CommandHandler("start", start))
BOT_APPLICATION.add_handler(CommandHandler("upload", upload))

@app.post(WEBHOOK_PATH)
async def process_webhook(request: Request) -> Response:
    json_data = await request.json()
    update = Update.de_json(json_data, BOT_APPLICATION.bot)
    await BOT_APPLICATION.process_update(update)
    return Response(status_code=200)

@app.get("/")
async def health_check():
    return "Bot is alive!"

@app.on_event("startup")
async def startup_event():
    webhook_url = os.getenv('WEBHOOK_URL') + WEBHOOK_PATH
    await BOT_APPLICATION.bot.set_webhook(url=webhook_url)

if __name__ == '__main__':
    # Local testing ke liye polling
    BOT_APPLICATION.run_polling()
