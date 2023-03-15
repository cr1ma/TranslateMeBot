!pip install --upgrade python-telegram-bot 
!pip install python-telegram-bot==13.0
!pip install deepl
!pip install deep_translator
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

DEEPL_API_ENDPOINT = 'https://api-free.deepl.com/v2/translate'
DEEPL_API_KEY = 'Insert the key here'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='🇺🇦 Вітаю! Я вам допоможу перекласти текст! Напишіть мені текст, і я з радістю перекладу його для вас.\n🇬🇧 Greetings! I can help you translate your text! Send me your text and I will be happy to translate it for you. ')
    context.bot.send_message(chat_id=update.effective_chat.id, text='🇺🇦 Я використовую передові технології машинного навчання, щоб забезпечити точність та якість перекладу. Так, мій перекладач ґрунтується на нейронних мережах, зокрема, на ядрі DeepL, але мій алгоритм був написаний за допомогою потужної мережі GPT-4. Якщо вас цікавить технічна сторона роботи, весь код мого перекладача буде доступний на GitHub.\n🇬🇧 I use advanced machine learning technologies to ensure translation accuracy and quality. Yes, my translator is based on neural networks, in particular the DeepL kernel, but my algorithm was written using the powerful GPT-4 network. If you are interested in the technical side of the work, the full code of my translator will be available on GitHub. \ngithub.com/cr1ma/TranslateMeBot')
    context.bot.send_message(chat_id=update.effective_chat.id, text='🇺🇦 Бажаю вам успішного використання!\n🇬🇧 I wish you a successful use!')

def translate(update, context):
    text = update.message.text
    context.user_data['text_to_translate'] = text

    button_labels = ["Українська", "English", "Русский"]
    keyboard_buttons = [InlineKeyboardButton(label, callback_data=label) for label in button_labels]
    reply_markup = InlineKeyboardMarkup([keyboard_buttons])

    context.bot.send_message(chat_id=update.effective_chat.id, text="🇺🇦 Будь ласка, виберіть мову для перекладу вашого повідомлення\n🇬🇧 Please select a language to translate your message", reply_markup=reply_markup)

def button_callback(update, context):
    query = update.callback_query
    target_lang = query.data
    language_codes = {'Українська': 'UK', 'English': 'EN', 'Русский': 'RU'}

    text = context.user_data.get('text_to_translate', '')

    response = requests.post(DEEPL_API_ENDPOINT, data={
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': language_codes[target_lang]
    })

    if response.status_code == 200:
        translation = response.json()['translations'][0]['text']
        context.bot.send_message(chat_id=query.message.chat_id, text=translation)
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text='🇺🇦 Вибачте, сталася помилка.\n🇬🇧 Sorry, an error occurred.')

if __name__ == '__main__':
    updater = Updater(token='Insert the key here', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    translate_handler = MessageHandler(Filters.text & ~Filters.command, translate)
    dispatcher.add_handler(translate_handler)

    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()