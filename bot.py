from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from config import TOKEN, MAX_TOKENS
from GPT import GPT_message_generate, addition_GPT, stop, users_history
bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS
users_history = {}
smiles = "🐍📵🤖👾👽👻🧞‍♂️™🚩"

# Функция для создания клавиатуры с нужными кнопочками
def create_keyboard(buttons_list):
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


# Приветственное сообщение /start
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text=f"Привет, {user_name}! Я бот-помощник для написание кода на Python!🐍📵\n"
                          f"Ты можешь прислать условие  а я постараюсь ниписать тебе код)🤖👾.\n"
                          "Иногда ответы получаются слишком длинными - в этом случае ты можешь попросить продолжить.",
                     reply_markup=create_keyboard(["/solve_task", '/help', '/addition', '/stop']))


# Команда /help
@bot.message_handler(commands=['help'])
def support(message):
    bot.send_message(message.from_user.id,
                     text="Чтобы приступить к решению задачи: нажми /solve_task, а затем напиши условие задачи",
                     reply_markup=create_keyboard(["/solve_task"]))

@bot.message_handler(commands=['solve_task'])
def get_promt_and_work(message):
    bot.send_message(message.chat.id, "Напиши условие новой задачи:")
    user_id = message.from_user.id
    if message.content_type != "text":
        bot.send_message(user_id, "Необходимо отправить именно текстовое сообщение")
        bot.register_next_step_handler(message, get_promt_and_work)
        return
    if len(message.text) > MAX_LETTERS:
        bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
        bot.register_next_step_handler(message, message.text)
        return
    if user_id not in users_history or users_history[user_id] == {}:
        # Сохраняем промт пользователя и начало ответа GPT в словарик users_history
        users_history[user_id] = {
            'system_content': "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python",
            "user_content": message.text,
            "assistant_content": ""
        }
        bot.register_next_step_handler(message, GPT_message_generate)
    else:
        bot.register_next_step_handler(message, GPT_message_generate)

@bot.message_handler(commands=['addition', "additio"])
def addition_prompt(message):
    bot.send_message(message.chat.id, "P.s. Если что, я могу продолжать решение только последней задачи! А точнее продолжение появится прямо сейчас, я активно над ним работаю)")
    bot.register_next_step_handler(message, addition_GPT)

@bot.message_handler(commands=["stop_gnenerate"])
def stop_generate(message):
    if users_history[message.from_user.id]["assistant_content"] != "":
        bot.send_message(message.chat.id, "Все данные стерты). Но не волнуйся на мою результативность это никак не повлияет!")
        bot.register_next_step_handler(message, stop)
    else:
        bot.send_message(message.chat.id, "Чтобы дополнить, нужно создать промт, подробнее в /help")


bot.polling()






