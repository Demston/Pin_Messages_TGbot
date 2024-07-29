"""ТГ бот. Закрепляет и удаляет крайнее сообщение в чате в заданном промежутке времени."""

import datetime
import telebot
import schedule
import threading
from config import *

bot = telebot.TeleBot(TOKEN)

# Считываем данные с файла со временем
lines_to_read = [3, 6, 9]
pin_time = [line.strip() for i, line in enumerate(open('time_of_messages.txt', encoding='UTF-8'))
            if i in lines_to_read]
pin_time_begin = str(pin_time[0])   # Время начала отсчёта
unpin_time = str(pin_time[1])       # Время открепления
pin_time_end = str(pin_time[2])     # Время окончания отсчёта, закрепление


@bot.message_handler(content_types=['text', 'photo'])
def dialog(message):
    """Добавляет сообщения в список"""
    x_chat_id = open('x_chat_id.txt', 'w')
    x_chat_id.write(str(message.chat.id))
    x_chat_id.close()
    if pin_time_begin <= datetime.datetime.today().strftime('%H:%M') < pin_time_end:
        open('messages_id_for_pin.txt', 'a', encoding='UTF-8').write(str(message.message_id) + '\n')


if __name__ == '__main__':
    def start_polling():
        """Работа бота"""
        print('Работает бот по закрепу сообщений в ТГ-чате')
        bot.polling(none_stop=True)


    polling_thread = threading.Thread(target=start_polling)
    polling_thread.start()


    def pin_func():
        """Закрепляет крайнее сообщение"""
        try:
            messages_file = open('messages_id_for_pin.txt', 'r+', encoding='UTF-8')
            last_message = str([line.strip() for line in messages_file][-1])
            bot.pin_chat_message(chat_id=open('x_chat_id.txt').read(), message_id=int(last_message))
            messages_file.truncate(0)   # Очищает файл со списком id сообщений
        except IndexError:
            pass


    def unpin_func():
        """Открепляет все сообщения (либо крайнее)"""
        bot.unpin_all_chat_messages(chat_id=open('x_chat_id.txt').read())
        # messages_file = open('messages_id_for_pin.txt', 'r+', encoding='UTF-8')
        # last_message = str([line.strip() for line in messages_file][-1])
        # for mes in last_message:
        #     bot.unpin_chat_message(chat_id=open('x_chat_id.txt').read(), message_id=int(mes))


    schedule.every().day.at(pin_time_end).do(pin_func)  # Исполнение функции (закреп)
    schedule.every().day.at(unpin_time).do(unpin_func)  # Исполнение функции (откреп)

    while True:
        schedule.run_pending()
