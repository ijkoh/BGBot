import schedule
from telebot import types
from links import *
import sqlite3
import telebot
import os
from sqlrequests import *
from dotenv.main import load_dotenv
import time
import threading
import logging

userWithRoots = [502643682]
logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)
conn = sqlite3.connect('newUsers.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY autoincrement,
   surname TEXT,
   name TEXT,
   secondname TEXT,
   idtelegram TEXT,
   startdate DATE,
   mentor TEXT DEFAULT 'nobody');
 """)
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = "Страница новичка🧑‍💻"
    btn2 = "Документы"
    btn3 = "Отпуск/Больничный/Отгул"
    btn4 = "Плюшки"
    btn5 = "Службы"
    btn6 = "Идеи"
    reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id,
                     "Привет-привет!\nМеня зовут БОТ CARGO.RUN\nРад приветствовать тебя.\nЯ помогу тебе найти "
                     "ответы на твои вопросы.\nЧто тебя интересует?", reply_markup=reply_markup, timeout=60)

@bot.message_handler(commands=['instruction'])
def instruction(message):
    bot.send_message(message.chat.id, '''
    1)Для добавления стажера введите команду "/add (Фамилия) (Имя) (Отчество) (ID Telegram) (Дата первого рабочего дня) (Юзернейм ментора)".
Обратите внимание, что дату нужно вводить в формате(ГГГГ-ММ-ДД).В случае некорректного ввода, может неправильно присылаться рассылка(или вообще не присылаться)
Добавляйте стажера только после его регистрации в боте!

2) Для просмотра всех стажёров введите "/show"

3) Для удаления стажера из списка стажеров введите команду "/delete (ID Telegram)"
''', timeout=60)


@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            if len(user_items) == 7:
                entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5], user_items[6])
                insertsql1(entity, cur)
            else:
                entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5])
                insertsql2(entity, cur)
            conn.commit()
        else:
            bot.send_message(message.chat.id, "У вас нет прав", timeout=60)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка", timeout=60)


@bot.message_handler(commands=["show"])
def show(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            show_sql(bot, user_id, cur)
        else:
            bot.send_message(user_id, "У вас нет прав", timeout=60)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка", timeout=60)


@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        user_id = message.chat.id
        if user_id in userWithRoots:
            user_items = message.text.split(" ")
            print(user_items[1])
            delete_user(user_items[1], cur)
            conn.commit()
        else:
            bot.send_message(user_id, "У вас нет прав", timeout=60)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка", timeout=60)


# @bot.message_handler(commands=['update'])
# def update(message):
#     try:
#         user_id = message.chat.id
#         if user_id in userWithRoots:
#             user_items = message.text.split(" ")
#             print(user_items)
#             entity = (user_items[1], user_items[2], user_items[3], user_items[4], user_items[5])
#             updatesql(entity, cur)
#             conn.commit()
#         else:
#             bot.send_message(message.chat.id, "У вас нет прав")
#     except Exception:
#         bot.send_message(message.chat.id, "Ошибка")


def check_dates():
    list_of_users7 = selectsql7(cur)
    if len(list_of_users7) != 0:
        for user in list_of_users7:
            bot.send_message(user[0], "Hello my friends", timeout=60)
    list_of_users30 = selectsql30(cur)
    if len(list_of_users30) != 0:
        for user in list_of_users30:
            bot.send_message(user[0], "Hello my niggas", timeout=60)
    list_of_users92 = selectsql92(cur)
    if len(list_of_users92) != 0:
        for user in list_of_users92:
            bot.send_message(user[0], "Hello my niggas", timeout=60)


schedule.every().day.at("10:30").do(check_dates)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Вернуться в главное меню ↩":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Страница новичка🧑‍💻"
        btn2 = "Документы"
        btn3 = "Отпуск/Больничный/Отгул"
        btn4 = "Плюшки"
        btn5 = "Службы"
        btn6 = "Идеи"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, text="Что Вы хотите узнать?", reply_markup=reply_markup, timeout=60)

   
    if message.text == "Страница новичка🧑‍💻":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Страничка новичка"
        btn2 = "Страничка нового аналитика"
        btn3 = "Страничка нового разработчика"
        btn4 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         "Здесь собрана вся информация, которая будет полезна для новичка.\nЕсли останутся вопросы, "
                         "можешь обратиться к наставнику/рукводителю/HR",
                         reply_markup=reply_markup, timeout=60)
    if message.text == "Страничка нового аналитика":
        bot.send_message(message.chat.id, f"{an_url}", parse_mode='HTML', timeout=60)
    if message.text == "Страничка нового разработчика":
        bot.send_message(message.chat.id, f"{newpie_utl}", parse_mode='HTML', timeout=60)

   
    if message.text == "Документы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Шаблоны"
        btn2 = "Справки"
        btn3 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Здесь собраны самые актуальные документы, которые тебе могут понадобиться",
                         reply_markup=reply_markup, timeout=60)
    if message.text == "Шаблоны":
        bot.send_message(message.chat.id,
                         f"По этой {templates_url} ты можешь найти самые акуальные и нужные шаблоны документов",
                         parse_mode='HTML', timeout=60)
    if message.text == "Справки":
        bot.send_message(message.chat.id,
                         f"Что можно заказать по этой {references_url}: 2-НДФЛ, копия трудовой книжи/договора, вопрос по отпуску, запрос для военкомата. Обращения обрабатываются в течение 3х рабочих дней после оформления заявки",
                         parse_mode="HTML", timeout=60)

   
    if message.text == "Отпуск/Больничный/Отгул":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Отпуск 🏖"
        btn2 = "Больничный"
        btn3 = "Отгул"
        btn4 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Оформи отпуск/больничный/отгул правильно, чтоб тебя не беспокоили в эти дни",
                         reply_markup=reply_markup, timeout=60)
    if message.text == "Отпуск 🏖":
        bot.send_message(message.chat.id,
                         f'Уйти в {vacation_url} так, чтоб тебя потом  "не дергали" с оформленем документов - это талант) И мы тебя этому научим',
                         parse_mode='HTML', timeout=60)
    if message.text == "Больничный":
        bot.send_message(message.chat.id, f"Если есть необходимость взять {sickleave_url}, то загляни сюда",
                         parse_mode='HTML', timeout=60)
    if message.text == "Отгул":
        bot.send_message(message.chat.id, f"{otgyl_url} на битрикс - страницу с инструкцией по действиям (если есть переработки за отгул, если есть договоренности, если…. Если нет договоренностей, то отправка на инструкцию и описание отпуска без сохранения з/п)",
                         parse_mode='HTML', timeout=60)
    
   
    if message.text == "Плюшки":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Реферальная программа"
        btn2 = "Партнерские скидки"
        btn3 = "Библиотека"
        btn4 = "Шоко-бот"
        btn5 = "Мерч"
        btn6 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, "Выберите:", reply_markup=reply_markup, timeout=60)
    if message.text == "Реферальная программа":
        bot.send_message(message.chat.id,
                         f"Классно работать с друзьями бок о бок! Ты можешь пригласить их к нам и получить за это выплату. Все условия {referalprogram_url}",
                         parse_mode="HTML", timeout=60)
    if message.text == "Партнерские скидки":
        bot.send_message(message.chat.id,
                         f"Уникальная система скидок от партнеров. Все условия {partner_url}",
                         parse_mode="HTML", timeout=60)
    if message.text == "Библиотека":
        bot.send_message(message.chat.id,
                         f"Большая коллекция профессиональной литературы в одном {biblio_url}.",
                         parse_mode="HTML", timeout=60)
    if message.text == "Шоко-бот":
        bot.send_message(message.chat.id,
                         f"Инструкция к нашему холодильнику и вкусностям в нём. По всем вопросам связанных с Шокоботом, обращаться к Саше Широкову @ShirokovAE",
                         parse_mode="HTML", timeout=60)
    if message.text == "Мерч":
        bot.send_message(message.chat.id,
                         f"Ещё не придумали...",
                         parse_mode="HTML", timeout=60)

   
    if message.text == "Службы":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = "Бухгалтерия и кадры"
        btn2 = "Техподдержка"
        btn3 = "Пропуск 🪪"
        btn4 = "Канц.товары и техника"
        btn5 = "Вернуться в главное меню ↩"
        reply_markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выберите:",
                         reply_markup=reply_markup, timeout=60)
    if message.text == "Бухгалтерия и кадры":
        bot.send_message(message.chat.id,
                         f"Тебе нужно заказать справку 2-НДФЛ или есть вопросы по начислению ЗП, узнать, сколько дней отпуска, нужен пакет документов для военкомата, или справка с места работы, кроме того, если у тебя изменились данные личных документов, то со всеми этими вопросами поможет разобраться Бухгалтерия. Наталья @Natalya_0604",
                         parse_mode="HTML", timeout=60)
    if message.text == "Техподдержка":
        bot.send_message(message.chat.id, 
                         f"Дать доступ к серверам, установить технику, подключить VPN...Это лишь малая часть того, чем занимается СТП. Нужна помощь-создай задачу. Марина @Motherofk8s",
                         parse_mode="HTML", timeout=60)
    if message.text == "Пропуск 🪪":
        bot.send_message(message.chat.id,
                         f"Пропуск перестал работать или необходим пропуск на велопарковку? В этом случае необходимо поставить задачу {propusk_url}",
                         parse_mode="HTML", timeout=60)
    if message.text == "Канц.товары и техника":
        bot.send_message(message.chat.id,
                         f"Необходима канцелярия, техника или мебель: обратись к {tovar_url} или @",
                         parse_mode="HTML", timeout=60)
    if message.text == "Идеи":
        bot.send_message(message.chat.id,
                         f"Если у тебя  есть идеи, пиши {ideas_url}.Мы обязательно рассмотрим твою идею, а ты получишь классный мерч!",
                         parse_mode="HTML", timeout=60)
       

def func1():
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            logging.error(e)
            time.sleep(15)

def func2():
    while True:
        schedule.run_pending()
        time.sleep(1)


bot_thread = threading.Thread(target=func1)
while_tread = threading.Thread(target=func2)

bot_thread.start()
while_tread.start()
