# testbot mit youtube-video-hilfe
# 1. Telegram-Bot-Library importieren:
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import random
from telegram import ReplyKeyboardMarkup
from datetime import datetime
import pytz
import sqlite3

# updater holt sich die updates vom bot-nutzer
# commandhandler verarbeitet alles mit slash davor, also alle Befehle
# Messagehandler verarbeitet alles was kein Befehl ist
# Filters filtert den Text

# liest die Bot-ID aus, über die der Bot gesteuert werden kann.
bot_auth_id = open("../../bb_id/bb_config.txt").read()

# establish connection to sqlite database:
# not working, yet
#conn = sqlite3.connect('bierbot_datenbank.db')
# sql-lite:
conn = sqlite3.connect(':memory:')
#creates a cursor
c = conn.cursor()


# in der Funktion hier werden die Parameter update zum updaten und context
# zum verwenden von Daten von außerhalb der Funktion übergeben.

# this function returns a funny german toast. try to pronounce it correctly.
def toast():
    # get the number of lines of the toast.txt-file
    num_lines = sum(1 for line in open('toast.txt'))
    # open the file with the funny german toasts
    toast_file = open('toast.txt')
    lines = toast_file.readlines()
    # in the lines statement, 0 represents the first line of the toast.txt-file.
    # That's why we need a random integer between 0 and num_lines-1
    # we have to use iso-8859 to avoid problems with german umalauts. .decode function is necessary to interpret
    # backslashes
    funny_german_toast = bytes(lines[random.randint(0, num_lines - 1)], "iso-8859-1").decode("unicode_escape") # python3)
    # the print statement would print the toast to the server's command-line.
    print(funny_german_toast)
    # this statement returns the funny german toast to the text interpreter function.
    # the text interpreter function sends it to the telegram-user (the beer drinker)
    return funny_german_toast

# This function does the database entries (in earlier development-stage it will only write to a file called log.txt
def db_entry(user_ID, user_FIRSTNAME, berlin_date, berlin_time, amount):
    log_entry = str(user_ID) + ";" + str(user_FIRSTNAME) + ";" + str(berlin_date) + ";" + str(
        berlin_time) + ";" + amount + ";" + "\n"
    print(log_entry)
    text_file = open("../log.txt", "a")
    n = text_file.write(log_entry)
    text_file.close()

# muss noch an custom-keyboards angepasst werden...
def help(update, context):
    update.message.reply_text(
        "[english version below]\n schreibe /register und drücke auf senden. Dann wähle die gezapfte Größe aus.")

# the custom-keyboard function
def custom_keyboard(update, context):
    keyboard = [["0,1l  \n 🍺", "0,2l \n 🍺🍺"], ["0,4l \n 🍺🍺 \n 🍺🍺", "1l \n 🍺🍺🍺🍺🍺 \n🍺🍺🍺🍺🍺"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Wieviel?", reply_markup=reply_markup)

new_keg_infos = {}
# the function text interpreter handles inputs of the user
def text_interpreter(update, context):
    # variables for info about the user and the time
    user = update.message.from_user
    user_ID = format(user['id'])
    user_FIRSTNAME = format(user['first_name'])
    berlin = pytz.timezone('Europe/Berlin')
    berlin_date = datetime.now(berlin).strftime("%d.%m.%y")
    berlin_time = datetime.now(berlin).strftime("%X")
    received_message = update.message.text
    # handling of user inputs regarding the amounts of beer they took:
    if received_message == '0,1l  \n 🍺':
        db_entry(user_ID, user_FIRSTNAME, berlin_date, berlin_time, '0.1')
        # lets get a funny german toast and send it to the users device:
        update.message.reply_text(toast())
    elif received_message == '0,2l \n 🍺🍺':
        db_entry(user_ID, user_FIRSTNAME, berlin_date, berlin_time, '0.2')
        # lets get a funny german toast and send it to the users device:
        update.message.reply_text(toast())
    elif received_message == '0,4l \n 🍺🍺 \n 🍺🍺':
        db_entry(user_ID, user_FIRSTNAME, berlin_date, berlin_time, '0.4')
        # lets get a funny german toast and send it to the users device:
        update.message.reply_text(toast())
    elif received_message == '1l \n 🍺🍺🍺🍺🍺 \n🍺🍺🍺🍺🍺':
        db_entry(user_ID, user_FIRSTNAME, berlin_date, berlin_time, '1.0')
        # lets get a funny german toast and send it to the users device:
        update.message.reply_text(toast())
    elif received_message == 'zurück zur Bier-Tastatur':
        custom_keyboard(update, context)
    elif received_message == '1 Fass zufuegen':
        keg_eigenschaften = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        add_keg_brand(update, context)
    elif received_message == 'zurück zum Keg-Menü':
        keg_main_menu(update, context)
    elif received_message == 'Breznak':
        print("Gern füge ich Breznak der Datenbank hinzu")
        add_keg_volume(update, context)
        new_keg_infos['brand'] = "Breznak"
        print(new_keg_infos)
    elif received_message == 'Billig-Pils':
        print("Gern füge ich Billig-Pils der Datenbank hinzu")
        add_keg_volume(update, context)
        new_keg_infos['brand'] = "Billig-Pils"
    elif received_message == 'andere Biersorte':
        print("Es wird vermerkt, dass es sich um eine andere Biersorte handelt.")
        add_keg_volume(update, context)
        new_keg_infos['brand'] = "unspecified brand"
    elif received_message == '30 Liter':
        print("ok, du hast ein 30 Liter Fass ausgewählt")
        new_keg_infos['volume'] = 30
        print(new_keg_infos)
        add_deposit_buyer(update, context)
    elif received_message == '50 Liter':
        print("ok, du hast ein 50 Liter Fass ausgewählt")
        new_keg_infos['volume'] = 50
        print(new_keg_infos)
        add_deposit_buyer(update, context)
    elif received_message == '25 Liter':
        print("ok, du hast ein 25 Liter Fass ausgewählt")
        new_keg_infos['volume'] = 25
        print(new_keg_infos)
        add_deposit_buyer(update, context)
    elif received_message == 'andere Menge':
        print("ok, du hast die Menge erst einmal auf 0 gesetzt.")
        new_keg_infos['volume'] = 0
        print(new_keg_infos)
        add_deposit_buyer(update, context)
    elif received_message == 'Pfand: Till':
        print("Danke Till!")
        new_keg_infos['deposit_buyer'] = 'Till'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Pfand: Martin':
        print("Danke Martin!")
        new_keg_infos['deposit_buyer'] = 'Martin'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Pfand: Jan':
        print("Danke Jan!")
        new_keg_infos['deposit_buyer'] = 'Jan'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Pfand: Erik':
        print("Danke Erik!")
        new_keg_infos['deposit_buyer'] = 'Erik'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Pfand: Marie':
        print("Danke Marie!")
        new_keg_infos['deposit_buyer'] = 'Marie'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Pfand: großzügige(r) Spender(in)':
        print("Danke Pfand: großzügige(r) Spender(in)!")
        new_keg_infos['deposit_buyer'] = 'Pfand: großzügige(r) Spender(in)'
        print(new_keg_infos)
        add_beer_buyer(update, context)
    elif received_message == 'Bier: Till':
        print("Danke Till!")
        new_keg_infos['beer_buyer'] = 'Till'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif received_message == 'Bier: Martin':
        print("Danke Martin!")
        new_keg_infos['beer_buyer'] = 'Martin'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif received_message == 'Bier: Jan':
        print("Danke Jan!")
        new_keg_infos['beer_buyer'] = 'Jan'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif received_message == 'Bier: Erik':
        print("Danke Erik!")
        new_keg_infos['beer_buyer'] = 'Erik'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif received_message == 'Pfand: Marie':
        print("Danke Marie!")
        new_keg_infos['beer_buyer'] = 'Marie'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif received_message == 'Bier: großzügige(r) Spender(in)':
        print("Danke großzügige(r) Spender(in)! für das Bier")
        new_keg_infos['beer_buyer'] = 'großzügige(r) Spender(in)'
        print(new_keg_infos)
        update.message.reply_text("Wie teuer war das Fass? (inkl. Steuer und ohne Pfand). Am Ende bitte ein €-Zeichen!", reply_markup=telegram.ReplyKeyboardRemove())
    elif "€" in received_message:
        price_in_euro = received_message.split("€")
        update.message.reply_text("Gut. Das Fass hat also " + price_in_euro[0] + " gekostet. Jetzt gib bitte das "
                                                                                 "Mindesthaltbarkeitsdatum des Fasses "
                                                                                 "ein. Schreib dazu MHD: und dann das "
                                                                                 "Datum in folgendem Format: DD.MM.YYYY)")
        new_keg_infos['price'] = price_in_euro[0]
        print(new_keg_infos)

    elif "MHD:" in received_message:
        mhd = received_message.split(':')
        update.message.reply_text(
            "ok. Das Bier ist also haltbar bis zum " + mhd[1] + " als leztes gib bitte "
                                                                              "an, wann du das Bier "
                                                                              "gekauft hast. Schreibe "
                                                                              "bitte dazu EK: und dann "
                                                                              "das Datum im Format "
                                                                              "DD.MM.YYYY")
        new_keg_infos['best_before'] = mhd[1]
        print(new_keg_infos)

    elif "EK:" in received_message:
        date_of_purchase = received_message.split(':')
        update.message.reply_text("Kauftag: " + date_of_purchase[1])
        new_keg_infos['date_of_purchase'] = date_of_purchase[1]
        update.message.reply_text("Marke: " + new_keg_infos['brand'])
        update.message.reply_text("Liter: " + str(new_keg_infos['volume']))
        update.message.reply_text("Käufer: " + new_keg_infos['deposit_buyer'])
        update.message.reply_text("Bier zahlte: " + new_keg_infos['beer_buyer'])
        update.message.reply_text("Bier kostete: " + new_keg_infos['price'])
        update.message.reply_text("Bier ist haltbar bis: " + new_keg_infos['best_before'])
        update.message.reply_text("Kaufdatum:" + new_keg_infos['date_of_purchase'])
        keyboard_keg_entry = [["Fass eintragen", "Fass fehlerhaft - alles neu eingeben"]]
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard_keg_entry)
        update.message.reply_text(text="alles korrekt? dann mit dem button eintragen bestätigen?", reply_markup=reply_markup)
    elif received_message == "Fass eintragen":
        print("Fass könnte jetzt eingetragen werden.")
    else:
        update.message.reply_text(
            "Du hast '" + received_message + "' geschrieben. Damit kann ich leider nix anfangen. Gib /help ein und ich sag dir was ich verstehe...")

#def auskunft(infos):
    #print(infos)
    #print(infos['brand'])
    #print(infos['volume'])
    #print(infos['deposit_buyer'])
    #print(infos['beer_buyer'])
    #print(infos['price'])
    #print(infos['best_before'])
    #print(infos['date_of_purchase'])






def keg_main_menu(update, context):
    keyboard = [["1 Fass zufuegen", "1 Fass aktivieren"], ["1 Fass leer (deaktivieren)", "zurück zur Bier-Tastatur"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Was willst du tun?", reply_markup=reply_markup)

def add_keg_brand(update, context):
    keyboard = [["Breznak", "Billig-Pils"], ["andere Biersorte", "zurück zum Keg-Menü"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Welche Sorte?", reply_markup=reply_markup)
    #return keg_eigenschaften

def add_keg_volume(update, context):
    keyboard = [["30 Liter", "50 Liter"], ["25 Liter", "andere Menge"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Wieviel?", reply_markup=reply_markup)
    #print(new_keg_infos)

def add_deposit_buyer(update, context):
    keyboard = [["Pfand: Till", "Pfand: Martin"], ["Pfand: Erik", "Pfand: Jan"],
                ["Pfand: Marie  ", "Pfand: großzügige(r) Spender(in)"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Wer hat DEN PFAND bezahlt?", reply_markup=reply_markup)
    #print(new_keg_infos)

def add_beer_buyer(update, context):
    keyboard = [["Bier: Till", "Bier: Martin"], ["Bier: Erik", "Bier: Jan"],
                ["Bier: Marie  ", "Bier: großzügige(r) Spender(in)"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Wer hat DEN PFAND bezahlt?", reply_markup=reply_markup)
    #print(new_keg_infos)

# the main function does only call the other functions. Programming should be done outside (above)
def main():
    updater = Updater(bot_auth_id, use_context=True)
    # dispatcher versendet infos an server:
    dp = updater.dispatcher

    # hier folgen die Handler
    # handler teilt den Befehlen / dem Text der bei Telegram eingegeben wird Funktionen zu
    # Beispiel-Handler: in Telegram wird der Befehl /start eingegeben
    # ausgeführt wird dann in diesem Skript die Funktion, die dem Befehl zugeteilt wird

    # Help-Handler (erklärt wie man sich sein Bier einträgt)
    dp.add_handler(CommandHandler("help", help))

    # custom keyboard - wichtig!
    dp.add_handler(CommandHandler("register", custom_keyboard))

    # custom keg management keyboard:
    dp.add_handler(CommandHandler("keg", keg_main_menu))

    # Message-Handler -> ruft die Funktion text_interpreter auf, wichtig!:
    dp.add_handler(MessageHandler(Filters.text, text_interpreter))

    # start_polling bedeutet, dass der updater beginnt nach updates zu gucken
    updater.start_polling()

    # Note: As you have read earlier, the Updater runs in a separate thread. That is very nice for this tutorial, but if you are writing a script, you probably want to stop the Bot by pressing Ctrl+C or sending a signal to the Bot process. To do that, use updater.idle(). It blocks execution until one of those two things occur, then calls updater.stop() and then continues execution of the script.
    updater.idle()

    # Python files can act as either reusable modules, or as standalone programs.

if __name__ == '__main__':
    main()