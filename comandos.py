import requests
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class FuncionesCoronaBot:

    def __init__(self, bot):
        self.bot = bot

    def CoronavirusEnArgentina(self, mensaje, context):
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
            😁Recuperados: {} \n\
            💀Muertes: {} \n\
            ".format(fecha_ultima_actualizacion, actual["Confirmed"], actual["Recovered"], actual["Deaths"])

        #mensaje.message.reply_text(respuesta)

        try:

            self.bot.bot.send_message(mensaje.message.chat_id, respuesta)

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

            self.bot.bot.send_photo(mensaje.message.chat_id, file)

        except Exception as e:

            print("Se rompio por {}".format(e))

            self.bot.bot.send_message(
                mensaje.message.chat_id, "Bot fuera de funcionamiento, intente de nuevo mas tarde.")

        print("se deberia haber mandado el mensaje")


    def _build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])

        if footer_buttons:
            menu.append([footer_buttons])

        return menu


    def listado_de_paises(self, mensaje, context):

        try:

            df = pd.DataFrame(requests.get(
                "https://api.covid19api.com/countries").json())

            df = df.sort_values(by="Country")

            botones = []

            for i in df["Country"].values:

                botones.append(InlineKeyboardButton(i, callback_data="prueba"))

            reply_markup = InlineKeyboardMarkup(self._build_menu(botones, n_cols=4))

            self.bot.bot.send_message(mensaje.message.chat_id,
                                "Zonas disponibles:", reply_markup=reply_markup)

        except Exception as e:

            print(e)


    def sintomas(self, mensaje, context):
        responder = "*Síntomas más frecuentes:* \n\
            - Fiebre. \n\
            - Tos seca. \n\
            - Cansancio.\n" +\
            "*Síntomas menos frecuentes:* \n\
            - Dolores y molestias. \n\
            - Congestion nasal. \n\
            - Dolor de cabeza. \n\
            - Conjuntivitis. \n\
            - Dolor de cabeza. \n\
            - Diarrea. \n\
            - Perdida del gusto o del olfato. \n\
            - Erupciones cutáneas. \n\
            - Cambios de color en los dedos de las manos o los pies. \n" + \
            "*Sintomas graves:* \n\
            - Dificultad para respirar. \n\
            - Dolor u opresión en el pecho \n\
            - Dificultades para hablar o moverse. \n\
            \n\
            \n\
            *Fuente*: https://www.who.int/es/emergencies/diseases/novel-coronavirus-2019/advice-for-public/q-a-coronaviruses#:~:text=sintomas"
        mensaje.message.reply_text(responder, parse_mode="markdown")


    def telefonos(self, mensaje, context):
        respuestas = "Acá tenes algunos *telefonos que te pueden ser útiles* en esta situación de cuarentena: \n\
            - 120 (telefono del ministerio de salud, atienden las 24hrs) \n" +\
            "*Provincia de Buenos Aires*: \n\
            - 148 (Es una línea de atención rápida para las personas que hayan viajado a los países con circulación del virus, o que hayan tenido contacto con una persona infectada.)\n\
            - 134 (telefono del ministerio de seguridad, para denunciar violaciones a la cuarentena)\n" +\
            "*Ciudad autonoma de Buenos Aires*: \n\
            - 107 \n" +\
            "*Córdoba*:\n\
            - 0800-122-1444 (Consultas y síntomas del covid) \n\
            - 0800-888-0054 (Denuncias e incumplimiento por la cuarentena) \n" +\
            "*Catamarca*:\n\
            - 383154238872 \n" +\
            "*Chaco*:\n\
            - 0800-444-0829 \n" +\
            "*Chubut*: \n\
            - 0800-222-2676 \n" +\
            "*Corrientes*:\n\
            - 03794974811 (fijo) \n\
            - 3794895124 (celular) \n" +\
            "*Entre Ríos*:\n\
            - 0800-777-8476 \n" +\
            "*Formosa*: \n\
            - 107 \n" +\
            "*Jujuy*: \n\
            - 0800-888-4767"
        mensaje.message.reply_text(respuestas, parse_mode="markdown")
