import requests

import pandas as pd
import matplotlib.pyplot as plt
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "es_ES")

bot = Updater("729687786:AAGblY3R2fwxaQ_0ClfPwZ70ghH1BO0dJlU",
              use_context=True)


def CoronavirusEnArgentina(mensaje, context):
    pais = "argentina"
    response = requests.get(
        "https://api.covid19api.com/country/{}".format(pais))
    if response.status_code == 200:
        covid = response.json()
    else:
        pais = "argentina"
        covid = requests.get(
            "https://api.covid19api.com/country/{}".format(pais)).json()

    actual = covid[-1]
    fecha_ultima_actualizacion = datetime.fromisoformat(
        actual["Date"].split("T")[0]).strftime("%A, %d de %B del %Y")
    respuesta = "Fecha: {} \n\
        😷Casos: {} \n\
        🚑Recuperados: {} \n\
        💀Muertes: {} \n\
        ".format(fecha_ultima_actualizacion, actual["Confirmed"], actual["Recovered"], actual["Deaths"])

    #mensaje.message.reply_text(respuesta)

    try:

        bot.bot.send_message(mensaje.message.chat_id, respuesta)

        covid = pd.DataFrame(covid)

        covid["Date"] = pd.to_datetime(covid["Date"])

        covid = covid[["Confirmed", "Recovered", "Deaths", "Date"]]

        covid = covid.set_index("Date").sort_index()

        fecha_inicio = covid[covid["Confirmed"] != 0].head(1).index[0]

        covid = covid[covid.index >= fecha_inicio]

        plt.rc('font', size=14)

        plt.figure(figsize=(20, 10))


        plt.subplot(1, 2, 1)

        plt.plot(covid.index.values, covid["Confirmed"].values)

        plt.plot(covid.index.values, covid["Recovered"].values, color="green")

        plt.plot(covid.index.values, covid["Deaths"].values, color="red")

        plt.title("El primer caso registrado fue el {}".format(

            fecha_inicio.strftime("%A, %d de %B del %Y")))

        plt.xlabel("Fecha")

        plt.ylabel("Casos")

        plt.legend(["Confirmados", "Recuperados", "Muertos"])

        plt.subplot(1, 2, 2)

        plt.title("Variación porcentual de casos confirmados")

        plt.xlabel("Fecha")

        plt.ylabel("Porcentaje de cambio")

        aux = (covid["Confirmed"].pct_change() * 100)

        plt.plot(aux.index.values, aux.values)

        plt.savefig("grafica.png", )

        file = open("grafica.png", 'rb')


        bot.bot.send_photo(mensaje.message.chat_id, file)

    except Exception as e:

        print("Se rompio por {}".format(e))

        bot.bot.send_message(
            mensaje.message.chat_id, "Bot fuera de funcionamiento, intente de nuevo mas tarde.")

    print("se deberia haber mandado el mensaje")


def build_menu(buttons,

               n_cols,

               header_buttons=None,

               footer_buttons=None):

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:

        menu.insert(0, [header_buttons])

    if footer_buttons:

        menu.append([footer_buttons])

    return menu


comando_data_argentina = CommandHandler("avance", CoronavirusEnArgentina)
bot.dispatcher.add_handler(comando_data_argentina)

print("empieza a correr el bot")

bot.start_polling()
bot.idle()
