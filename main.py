import os
from dotenv import load_dotenv
import asyncio
import pyodbc
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

nest_asyncio.apply()
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
user_selected_students = {}

# Подключение к базе данных
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=School12db;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()


# Стартовое сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name
    logger.info(f"Start command received from {user_name} (ID: {user_id})")
    keyboard = [["📋 МЕНЮ"], ["ℹ️ИНСТРУКЦИЯ"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Добро пожаловать! Выберите действие:", reply_markup=reply_markup)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.full_name
    logger.info(f"Menu command received from {user_name} (ID: {update.message.from_user.id})")

    keyboard = [["📜 СОЗДАТЬ СПИСОК"], ["📂 ПРОШЛЫЕ СПИСКИ"], ["🔙 Назад"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("📋 Главное меню", reply_markup=reply_markup)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.full_name
    logger.info(f"Info command received from {user_name} (ID: {update.message.from_user.id})")

    await update.message.reply_text("ℹ️ Этот бот помогает создавать списки учеников!!!"
                                    "\n\n"
                                    "Главное меню:\n"
                                    "• Создать список — создайте новый список учеников.\n"
                                    "• Прошлые списки — посмотрите ранее сохранённые списки.\n"
                                    "• Назад — вернуться в предыдущее меню.\n"
                                    "\n"
                                    "Создание списка:\n"
                                    "• Выберите класс и добавьте учеников.\n"
                                    "• Вы можете просмотреть текущий список, редактировать его (добавить/удалить учеников) или сохранить в Excel.\n"
                                    "\n"
                                    "Редактирование:\n"
                                    "• Добавьте или удалите учеников из списка.\n"
                                    "\n"
                                    "Просмотр старых списков:\n"
                                    "• Перейдите в раздел Прошлые списки для доступа к ранее сохранённым.\n"
                                    "\n"
                                    "После выбора класса вы сможете добавить учеников в список, отредактировать его и затем нажать кнопку 'Сохранить и отправить.'"
                                    "\n\n"
                                    "!!!!! ДЛЯ ТОГО ЧТОБЫ ОТРЕДАКТИРОВАТЬ УЖЕ ОТПРАВЛЕННЫЙ СПИСОК, ПРОСТО СОЗДАЙТЕ НОВЫЙ. ОТПРАВЛЕН БУДЕТ ПОСЛЕДНИЙ СОЗДАННЫЙ СПИСОК.")


# Выбор класса
async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT ClassID, ClassName FROM Classes")
    classes = cursor.fetchall()

    keyboard = [
        [InlineKeyboardButton(c.ClassName, callback_data=f"class_{c.ClassID}")] for c in classes
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите класс:", reply_markup=reply_markup)


async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler('info', info))
    await app.run_polling()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
