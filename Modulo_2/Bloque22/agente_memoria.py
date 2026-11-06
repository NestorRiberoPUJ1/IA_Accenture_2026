from dotenv import load_dotenv
from pydantic import BaseModel, Field
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
modelo = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# --- Bloque 1: herramienta con args_schema ---
class ArgumentosConsultaEnvio(BaseModel):
    numero_seguimiento: str = Field(
        description="Número de seguimiento del envío."
    )
    incluir_historial: bool = Field(
        default=False,
        description="Si es True, incluye el historial completo."
    )

ESTADOS = {
    "AR12345": {
        "actual": "en tránsito, llega en 2 días",
        "historial": [
            "recibido en depósito",
            "en tránsito",
        ],
    },
}

@tool(
    "consultar_estado_envio_con_historial",
    args_schema=ArgumentosConsultaEnvio
)
def consultar_estado_envio_detallado(
    numero_seguimiento: str,
    incluir_historial: bool = False
) -> str:
    """Consulta el estado de un envío, con la
    opción de incluir su historial completo."""
    envio = ESTADOS.get(numero_seguimiento)
    if envio is None:
        return (
            f"No se encontró un envío con el "
            f"número {numero_seguimiento}."
        )
    if not incluir_historial:
        return envio["actual"]
    historial = ", ".join(envio["historial"])
    return f"{envio['actual']} (historial: {historial})"

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
    return f"El costo estimado es de ${costo:.2f}."

# --- Bloque 2: agente y ejecutor ---
herramientas = [
    consultar_estado_envio_detallado,
    calcular_costo_envio,
]

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


# --- Bloque 3: memoria entre interacciones ---

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

config = {"configurable": {"session_id": "cliente_456"}}

resultado = agente_con_memoria.invoke(
    {"entrada": (
        "¿Cuál es el estado del envío "
        "AR12345, con su historial?"
    )},
    config
)

print(resultado["output"])