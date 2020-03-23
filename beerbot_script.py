# testbot mit youtube-video-hilfe
# 1. Telegram-Bot-Library importieren:
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# updater holt sich die updates vom bot-nutzer
# commandhandler verarbeitet alles mit slash davor, also alle Befehle
# Messagehandler verarbeitet alles was kein Befehl ist
# Filters filtert den Text


# in der Funktion hier werden die Parameter update zum updaten und context
# zum verwenden von Daten von außerhalb der Funktion übergeben.
def start(update, context):
    # der folgende Befehl antwortet an den Nutzer:
    update.message.reply_text("Bitte trag dein Bier ein: ")

def help(update, context):
    update.message.reply_text("[english version below]\n Mit /join <WG-Mitbewohner> kannst du festlegen, welcher Mitbewohner für dein Bier bezahlt. \nVerwende folgende Syntax um dein Bier einzutragen: '/add <Menge in Litern>'. \nIch lese dann deinen Namen aus und füge das Bier automatisch deinem Konto hinzu. Falls du noch kein Konto hast, wird eines angelegt. \n \n English version: use /join to define who (of the roommates) is paying for your beer. Use /add <amount in litres> to add your beer to the tap.")

def nixverstehen(update, context):
    update.message.reply_text("Du hast '" + update.message.text + "' geschrieben. Damit kann ich leider nix anfangen. Gib /help ein und ich sag dir was ich verstehe...")

# die "Master-Funktion"
def main():
    updater = Updater("962316800:AAGf-v6vfhVnNytOfC_7t_KPrGu1T3jA8Wk", use_context=True)
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

    # Message-Handler:
    dp.add_handler(MessageHandler(Filters.text, nixverstehen))

    # start_polling bedeutet, dass der updater beginnt nach updates zu gucken
    updater.start_polling()

    # Note: As you have read earlier, the Updater runs in a separate thread. That is very nice for this tutorial, but if you are writing a script, you probably want to stop the Bot by pressing Ctrl+C or sending a signal to the Bot process. To do that, use updater.idle(). It blocks execution until one of those two things occur, then calls updater.stop() and then continues execution of the script.
    updater.idle()

    # Python files can act as either reusable modules, or as standalone programs.
if __name__=='__main__':
        main()
