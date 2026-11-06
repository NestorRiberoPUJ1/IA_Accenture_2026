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

from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from dotenv import load_dotenv
from cprint import cprint

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", timeout=10)

historiales = {}


def normalizar_respuesta(resultado):
    contenido = resultado["output"]

    if isinstance(contenido, list):
        contenido = "".join(
            bloque["text"]
            for bloque in contenido
            if isinstance(bloque, dict)
            and bloque.get("type") == "text"
        )

    return {
        **resultado,
        "output": AIMessage(content=contenido)
    }


def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()
    return historiales[session_id]


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
        MessagesPlaceholder("chat_history"),
        ("human", "{entrada}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agente = create_tool_calling_agent(modelo, herramientas, prompt_agente)

    ejecutor_agente = AgentExecutor(
        agent=agente,
        tools=herramientas,
        verbose=False,
        return_intermediate_steps=True
    )
    agente_normalizado = (
        ejecutor_agente
        | RunnableLambda(normalizar_respuesta)
    )

    agente_con_memoria = RunnableWithMessageHistory(
        agente_normalizado,
        obtener_historial,
        input_messages_key="entrada",
        history_messages_key="chat_history",
        output_messages_key="output",
    )

    config = {"configurable": {"session_id": "cliente_123"}}

    # resultado = ejecutor_agente.invoke({"entrada": "¿Qué maquina necesito mover tierra?"})
    # cprint.err(resultado["output"])
    resultado = agente_con_memoria.invoke(
        {"entrada": "¿Cuánto es 12 * 5?"}, config)
    cprint.err(resultado["output"])

    resultado = agente_con_memoria.invoke(
        {"entrada": "y si en vez de multiplicarlos los sumo cuánto es?"}, config)
    cprint.err(resultado["output"])

    config = {"configurable": {"session_id": "cliente_1234"}}
    resultado = agente_con_memoria.invoke(
        {"entrada": "divide el resultado por 3"}, config)
    cprint.err(resultado["output"])

    config = {"configurable": {"session_id": "cliente_123"}}
    resultado = agente_con_memoria.invoke(
        {"entrada": "divide el resultado por 3"}, config)
    cprint.err(resultado["output"])
    
