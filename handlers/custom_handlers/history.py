from states.history_state import History_state
from telebot.types import Message
from keyboards.inline import need_photo
from loader import bot


@bot.message_handler(commands=['history'])
def draw_number(message: Message) -> None:
    bot.set_state(message.from_user.id, History_state.need_photo, message.chat.id)
    markup = need_photo.need_photo()
    bot.send_message(message.from_user.id, f"Нужны ли вам фотографии отелей?", reply_markup=markup)
