from cprint import cprint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from enrutamiento import cadena_con_enrutamiento

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


modelo = ChatGoogleGenerativeAI(model="gemini-3.8-flash", timeout=10)
modelo_respaldo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", timeout=15)

respuesta_generica = RunnableLambda(
    lambda x: (
        "Gracias por tu mensaje. Un miembro de nuestro "
        "equipo te va a responder pronto."
    )
)

cadena_queja = (
    PromptTemplate.from_template(
        "Responde a esta queja con empatía, reconociendo el "
        "problema antes de ofrecer una solución:\n\n{mensaje}"
    )
    | modelo
    | StrOutputParser()
)

cadena_queja_modelo_respaldo = (
    PromptTemplate.from_template(
        "Responde a esta queja con empatía, reconociendo el "
        "problema antes de ofrecer una solución:\n\n{mensaje}"
    )
    | modelo_respaldo
    | StrOutputParser()
)

cadena_queja_segura = cadena_queja.with_fallbacks(
    [cadena_queja_modelo_respaldo, respuesta_generica]
)


def fallar_a_proposito(x):
    raise Exception("Error de red simulado")


cadena_rota = RunnableLambda(fallar_a_proposito)
cadena_secundaria_rota = RunnableLambda(fallar_a_proposito)

cadena_doble_segura = cadena_rota.with_fallbacks(
    [cadena_secundaria_rota, respuesta_generica]
)
resultado = cadena_doble_segura.invoke(
    {"mensaje": "la app se cierra sola"}
)
cprint.info(resultado)

# resultado = cadena_queja_segura.invoke({"mensaje": "Estoy muy molesto con el servicio."})
# cprint.fatal(resultado)


def procesar_mensaje_seguro(mensaje):
    try:
        return cadena_con_enrutamiento.invoke(
            {"mensajes": mensaje}
        )

    except Exception as error:
        logger.error(f"Error procesando mensaje: {error}")
        return (
            "No pudimos procesar tu mensaje en este momento. "
            "Intenta de nuevo más tarde."
        )


procesar_mensaje_seguro("Pueden aplicar una fuente más grande?")
