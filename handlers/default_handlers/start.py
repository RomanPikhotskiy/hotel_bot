from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.full_name}! Я бот по поиску отелей. Смогу "
                                           f"подобрать для вас подходящие отели, где бы вы ни были. Для более "
                                           f"детального изучения моего функционала введите команду /help")
