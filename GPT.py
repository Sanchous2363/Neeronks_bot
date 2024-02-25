from openai import OpenAI
from config import MAX_TOKENS, TOKEN
import telebot
import requests
bot = telebot.TeleBot(TOKEN)
from dannie import load_user_data, save_user_data
data_path = "users.json"
users_history = load_user_data(data_path)
def GPT_message_generate(message):

  client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
  assistant_content = "Напишем код и объяснение:"
  completion = client.chat.completions.create(
    model="local-model",  # this field is currently unused
    messages=[
      {"role": "system", "content": "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python"},
      {"role": "user", "content": message.text},
      {"role": "assistant", "content": assistant_content}
    ],
    temperature=0.7,
    max_tokens=MAX_TOKENS
  )
  response = requests.post("http://localhost:1234/v1")
  if response.status_code == 200:
    answer = completion.choices[0].message.content
    bot.send_message(message.chat.id, answer + "🐍")
    if message.from_user.id not in users_history or users_history[message.from_user.id] == {}:
      users_history[message.from_user.id] = {
        'system_content': "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python",
        "user_content": message.text,
        "assistant_content": assistant_content + answer}
      save_user_data(users_history, data_path)
  else:
    bot.send_message(message.chat.id,"Ошибка:", response.text)
    users_history[message.chat.id]['system_content'] = "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python"
    users_history[message.chat.id]["user_content"] = ''

def addition_GPT(message):
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
  assistant_content = "Продолжи объяснение:"
  completion = client.chat.completions.create(
    model="local-model",  # this field is currently unused
    messages=[
      {"role": "system",
       "content": "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python"},
      {"role": "user", "content": users_history[message.from_user.id]["assistant_content"]},
      {"role": "assistant", "content": assistant_content}
    ],
    temperature=0.7,
    max_tokens=MAX_TOKENS
  )
  response = requests.post("http://localhost:1234/v1")
  if response.status_code == 200:
    answer = completion.choices[0].message.content
    bot.send_message(message.chat.id, answer + "🐍")
    if message.from_user.id not in users_history or users_history[message.from_user.id] == {}:
      users_history[message.from_user.id] = {
        'system_content': "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python",
        "user_content": message.text,
        "assistant_content": assistant_content + answer}
      save_user_data(users_history, data_path)
  else:
    bot.send_message(message.chat.id, "Ошибка:", response.text)
    users_history[message.chat.id][
      'system_content'] = "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python"
    users_history[message.chat.id]["user_content"] = ''
def stop(message):
  users_history[message.chat.id]['system_content'] = "Ты - русский помощник, который пишет пояснения к коду на русском, а сам код на английском, на языке Python"
  users_history[message.chat.id]["user_content"] = ''









