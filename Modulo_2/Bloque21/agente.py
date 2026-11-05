from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from dotenv import load_dotenv
from cprint import cprint

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash", timeout=10)


@tool(description="Selecciona la maquinaria adecuada según la consulta.")
def seleccionar_maquinaria(consulta: str) -> str:
    articulos = {
        "mover tierra": (
            "Para el movimiento de tierra, se recomienda utilizar excavadoras y cargadores frontales."
        ),
        "cimentacion": (
            "Para la cimentación, se recomienda utilizar hormigoneras y compactadoras."
        ),
        "elevacion": (
            "Para la elevación de materiales, se recomienda utilizar grúas y montacargas."
        ),
    }
    for clave, texto in articulos.items():
        if clave in consulta.lower():
            return texto
    return "No encontré información para esa consulta."


@tool(description="Evalúa una expresión aritmética simple.")
def calcular(expresion: str) -> str:
    permitido = set("0123456789+-*/(). ")
    if not set(expresion) <= permitido:
        return "Expresión no permitida."
    try:
        return str(eval(expresion))
    except Exception as e:
        return f"Error al evaluar la expresión: {e}"


if __name__ == "__main__":
    resultado = seleccionar_maquinaria.invoke(
        "¿Qué maquina necesito mover tierra?")
    cprint.err(resultado)

    herramientas = [seleccionar_maquinaria, calcular]

    prompt_agente = ChatPromptTemplate.from_messages([
        (
            "system",
            "Eres un asistente que responde preguntas "
            "usando las herramientas disponibles cuando "
            "las necesites.",
        ),
        ("human", "{entrada}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agente = create_tool_calling_agent(modelo, herramientas, prompt_agente)

    ejecutor_agente = AgentExecutor(
        agent=agente, 
        tools=herramientas, 
        verbose=True,
        return_intermediate_steps=True
        )

    #resultado = ejecutor_agente.invoke({"entrada": "¿Qué maquina necesito mover tierra?"})
    #cprint.err(resultado["output"])
    #resultado = ejecutor_agente.invoke({"entrada": "¿Cuánto es 12 * 5?"})
    #cprint.err(resultado["output"])
    resultado = ejecutor_agente.invoke({"entrada": "¿Qué color combina con el rojo?"})
    for accion, observacion in resultado["intermediate_steps"]:
        cprint.info(accion.tool, accion.tool_input, "->", observacion)
