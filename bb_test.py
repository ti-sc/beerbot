# testbot mit youtube-video-hilfe
# 1. Telegram-Bot-Library importieren:
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from telegram import ReplyKeyboardMarkup
# updater holt sich die updates vom bot-nutzer
# commandhandler verarbeitet alles mit slash davor, also alle Befehle
# Messagehandler verarbeitet alles was kein Befehl ist
# Filters filtert den Text

# liest die Bot-ID aus, über die der Bot gesteuert werden kann.
bot_auth_id = open("../../bb_id/bb_config.txt").read()

# in der Funktion hier werden die Parameter update zum updaten und context
# zum verwenden von Daten von außerhalb der Funktion übergeben.
def start(update, context):
    # der folgende Befehl antwortet an den Nutzer:
    update.message.reply_text("Bitte trag dein Bier ein: ")

# muss noch an custom-keyboards angepasst werden...
def help(update, context):
    update.message.reply_text("[english version below]\n schreibe /register und drücke auf senden. Dann wähle die gezapfte Größe aus.")

# die Funktion text_interpreter verarbeitet den text
def text_interpreter(update, context):
    received_message = update.message.text
    if received_message == '0,1l  \n 🍺':
        update.message.reply_text("Das nenne ich mal verantwortungsbewussten Alkoholkonsum")
    elif received_message == '0,2l \n 🍺🍺':
        update.message.reply_text("Misch noch Sprite o.Ä. dazu, dann hast du ein volles Glas Radler")
    elif received_message == '0,4l \n 🍺🍺 \n 🍺🍺':
        update.message.reply_text("Standard")
    elif received_message == '1l \n 🍺🍺🍺🍺🍺 \n🍺🍺🍺🍺🍺':
        update.message.reply_text("Trink nicht zuviel davon")
    else:
        update.message.reply_text("Du hast '" + received_message + "' geschrieben. Damit kann ich leider nix anfangen. Gib /help ein und ich sag dir was ich verstehe...")

# so später nicht notwendig, aber erstmal hilfreich um zu verstehen wie username usw abgerufen werden können.
def deinname(update,context):
    user = update.message.from_user
    user_ID = format(user['id'])
    user_NAME = format(user['username'])
    user_FIRSTNAME = format(user['first_name'])
    user_LASTNAME = format(user['last_name'])  # die bequeme Variante user['full_name'] funktioniert aus irgendeinem Grund nicht.
    #user_FULLNAME = format(user['full_name'])
    print("You talk with " + user_NAME + " his/her user ID is " + user_ID + " his/her real name is " + user_FIRSTNAME + " " + user_LASTNAME)
    update.message.reply_text(user_FIRSTNAME + " du solltest deinen Alkoholkonsum überdenken!")

# die custom-keyboard Funktion
def custom_keyboard(update, context):
    keyboard = [[ "0,1l  \n 🍺", "0,2l \n 🍺🍺"], ["0,4l \n 🍺🍺 \n 🍺🍺", "1l \n 🍺🍺🍺🍺🍺 \n🍺🍺🍺🍺🍺" ]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text = "Wieviel?", reply_markup = reply_markup)

# die "Master-Funktion"
def main():
    updater = Updater(bot_auth_id, use_context=True)
    # dispatcher versendet infos an server:
    dp = updater.dispatcher

    # hier folgen die Handler
    # handler teilt den Befehlen / dem Text der bei Telegram eingegeben wird Funktionen zu
    # Beispiel-Handler: in Telegram wird der Befehl /start eingegeben
    # ausgeführt wird dann in diesem Skript die Funktion, die dem Befehl zugeteilt wird
    # hier als Beispiel wird der Befehl start mit der Funktion start assoziiert.
    dp.add_handler(CommandHandler("start", start))
    # Help-Handler (erklärt wie man sich sein Bier einträgt)
    dp.add_handler(CommandHandler("help", help))

    # nur zur Illustration - nicht bierbot-relevant:
    dp.add_handler(CommandHandler("ich", deinname))

    # custom keyboard - wichtig!
    dp.add_handler(CommandHandler("register", custom_keyboard))

    # Message-Handler -> ruft die Funktion text_interpreter auf, wichtig!:
    dp.add_handler(MessageHandler(Filters.text, text_interpreter))

    # start_polling bedeutet, dass der updater beginnt nach updates zu gucken
    updater.start_polling()

    # Note: As you have read earlier, the Updater runs in a separate thread. That is very nice for this tutorial, but if you are writing a script, you probably want to stop the Bot by pressing Ctrl+C or sending a signal to the Bot process. To do that, use updater.idle(). It blocks execution until one of those two things occur, then calls updater.stop() and then continues execution of the script.
    updater.idle()

    # Python files can act as either reusable modules, or as standalone programs.
if __name__=='__main__':
        main()
