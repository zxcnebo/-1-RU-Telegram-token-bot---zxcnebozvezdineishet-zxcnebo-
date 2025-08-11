import telebot

class Person:
    def __init__(self, name, money=0):
        self.__name = name
        self.__money = money

    def add_money(self, amount):
        self.__money += amount

    def get_money(self):
        return self.__money

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


bot = telebot.TeleBot('token')

users = {}  # user_id -> Person

promo_codes = {
    "PROMO25": 25,
    "TELEBOT20": 20,
    "JAJCADANIKA": 400
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users: 
        bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
        bot.register_next_step_handler(message, ask_name)
    else:
        bot.send_message(message.chat.id, f"Привет, {users[user_id].get_name()}! Твои деньги: {users[user_id].get_money()}\n/help — список команд")

def ask_name(message):
    user_id = message.from_user.id
    name = message.text
    users[user_id] = Person(name, 0)
    bot.send_message(message.chat.id, f"Рад знакомству, {name}!\nТеперь ты можешь использовать команды. Твой баланс: 0 монет\n/help — список команд")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, message.chat.id)

@bot.message_handler(commands=['my_promo'])
def my_promo(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "Сначала введи имя: /start")
        return
    coins = users[user_id].get_money()
    bot.send_message(message.chat.id, f"💰 Твой баланс: {coins} монет")

@bot.message_handler(commands=['promo'])
def promo_command(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "Сначала введи имя: /start")
        return
    bot.send_message(message.chat.id, "Введи промокод:")
    bot.register_next_step_handler(message, process_promo)

def process_promo(message):
    user_id = message.from_user.id
    code = message.text.strip().upper()
    if code in promo_codes:
        amount = promo_codes.pop(code)  # удаляем после использования
        users[user_id].add_money(amount)
        bot.send_message(message.chat.id, f"✅ Промокод принят! Тебе начислено {amount} монет.")
    else:
        bot.send_message(message.chat.id, "❌ Промокод недействителен.")
    # Покажем баланс
    bot.send_message(message.chat.id, f"💰 Твой баланс: {users[user_id].get_money()} монет")


bot.polling()
