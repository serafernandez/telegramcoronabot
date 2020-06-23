from telegram.ext import CallbackQueryHandler, Filters
import locale
from telegram.ext import Updater, CommandHandler
from comandos import FuncionesCoronaBot
import os

locale.setlocale(locale.LC_TIME, "C.UTF-8")

bot = Updater(os.getenv("TOKEN_TG"),
              use_context=True)

funciones_bot = FuncionesCoronaBot(bot)


def echo(update, context):
    try:
        data = update.callback_query.data
        if data.startswith("getInfoCountry_"):
            country = data.split("_")[1]
            country_full_name = data.split("_")[2]
            funciones_bot.enviar_datos_de_pais(country_full_name, country, update.effective_chat.id)
    except Exception as e:
        print(e)


echo_handler = CallbackQueryHandler(echo)
bot.dispatcher.add_handler(echo_handler)


comando_sintomas = CommandHandler("sintomas", funciones_bot.sintomas)
comando_data_argentina = CommandHandler("avance", funciones_bot.CoronavirusEnArgentina)
comando_data_zonas = CommandHandler("zonas", funciones_bot.listado_de_paises)
comando_telefonos = CommandHandler("telefonos", funciones_bot.telefonos)
bot.dispatcher.add_handler(comando_telefonos)
bot.dispatcher.add_handler(comando_sintomas)
bot.dispatcher.add_handler(comando_data_argentina)
bot.dispatcher.add_handler(comando_data_zonas)

print("empieza a correr el bot")

bot.start_polling()
bot.idle()

#Como hacerle frente al estrés, personas que estan solas, personas que tienen  problemas familiares, etc.
#estresores y deporte
#esto es argentina sabemos que los controles no son rigurosos, sean responsables y controlados

#https://www.intramed.net/contenidover.asp?contenidoid=95688#comentarios
