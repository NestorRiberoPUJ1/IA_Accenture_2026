from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

load_dotenv()
modelo = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

@tool
def calcular_costo_envio(
    peso_kg: float,
    distancia_km: float
) -> str:
    """Calcula el costo estimado de un envío
    según su peso y la distancia a recorrer.
    Usar cuando el usuario pregunta cuánto va a
    costar enviar algo."""
    costo = 500 + (peso_kg * 120) + (distancia_km * 3)
    return f"El costo estimado es de ${costo:.2f}"

herramientas = [calcular_costo_envio]
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

agente = create_tool_calling_agent(
    modelo, herramientas, prompt_agente
)

ejecutor_agente = AgentExecutor(
    agent=agente, tools=herramientas
)

historiales = {}
def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()
    return historiales[session_id]

agente_con_memoria = RunnableWithMessageHistory(
    ejecutor_agente,
    obtener_historial,
    input_messages_key="entrada",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "cliente_123"}}

resultado_1 = agente_con_memoria.invoke(
    {"entrada": (
        "¿Cuánto cuesta enviar un paquete de "
        "2kg a 300km?"
    )},
    config
)

print(resultado_1["output"])