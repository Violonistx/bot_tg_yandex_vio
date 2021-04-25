from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os
import pydub
import librosa


token = '1755517201:AAFujFilNayicrcBA16mCPlxvLrO28zb7es'


def start(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text="Привет, я обрабатываю аудио файлы в формате .mp3")


def text(update, context):

    update.message.reply_text('✅ Загружаю аудио для будущей обратботки.')

    file_info = requests.get('https://api.telegram.org/bot{0}/getFile?file_id={1}'.format(token,
                                                                                          update.message.audio.file_id))
    tmp = file_info.text
    file_path = tmp[tmp.find('"file_path":') + 13:-3]
    file_save = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_path))
    print(file_path)
    with open(update.message.audio.file_id + '.mp3', 'wb') as f:
        f.write(file_save.content)

        with open(update.message.audio.file_id + '.mp3', 'rb') as audio:
            payload = {
                'chat_id': update.message.chat.id,
                'title': 'audio.mp3',
                'parse_mode': 'HTML'
            }
            files = {
                'audio': audio.read(),
            }
            resp = requests.post(
                "https://api.telegram.org/bot{token}/sendAudio".format(token=token),
                data=payload,
                files=files).json()

            update.message.reply_text('✅ Аудио обработано.')

            # удаление файла чтобы не засорять память компьютера

            '''os.remove(update.message.audio.file_id + '.mp3')'''


def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.audio, text))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
