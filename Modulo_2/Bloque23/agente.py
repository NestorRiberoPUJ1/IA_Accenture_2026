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

from pydantic import BaseModel, Field

import json
from datetime import datetime, timezone

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


def registrar_traza(
    session_id: str,
    entrada: str,
    resultado: dict,
) -> None:
    """Guarda una interacción del agente como una
    línea JSON en trazas_agente.jsonl: qué se
    preguntó, qué herramientas se usaron y con qué
    argumentos, y la respuesta final. Si "resultado"
    no trae "intermediate_steps" (por ejemplo, con
    return_intermediate_steps=False), acciones queda
    como una lista vacía en vez de fallar."""

    registro = {
        "timestamp": datetime.now(timezone.utc)
        .isoformat(),
        "session_id": session_id,
        "entrada": entrada,
        "acciones": [
            {
                "herramienta": accion.tool,
                "argumentos": accion.tool_input,
                "observacion": observacion,
            }
            for accion, observacion in resultado.get(
                "intermediate_steps", [])
        ],
        "respuesta_final": resultado["output"].content
    }

    with open(
        "trazas_agente.jsonl", "a", encoding="utf-8"
    ) as archivo:
        archivo.write(
            json.dumps(registro, ensure_ascii=False)
            + "\n"
        )


class ConsultaMaquinaria(BaseModel):
    consulta: str = Field(
        description=(
            """ Consulta del usuario sobre qué tipo de maquinas usar segun la actividad"""
            """ Las categorias son: [movimiento de tierra, cimentación, elevación]"""
        )
    )


@tool(
    "escoger_maquinaria_segun_actividad",
    args_schema=ConsultaMaquinaria
)
def consultar_maquinaria(consulta: str) -> str:
    """Consulta sobre qué tipo de maquinaria usar según la actividad."""
    if "movimiento de tierra" in consulta.lower():
        return "Para movimiento de tierra, se recomienda usar excavadoras y bulldozers."
    elif "cimentación" in consulta.lower():
        return "Para cimentación, se recomienda usar pilotes y grúas."
    elif "elevación" in consulta.lower():
        return "Para elevación, se recomienda usar grúas torre y montacargas."
    else:
        return "No se encontró una recomendación específica para la consulta proporcionada."


if __name__ == "__main__":

    herramientas = [consultar_maquinaria]

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
        verbose=True,
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
    resultado_1 = agente_con_memoria.invoke(
        {"entrada": "¿Qué máquina necesito nivelar un terreno?"}, config)
    cprint.err(resultado_1["output"])
    # Registrar la traza de la interacción
    registrar_traza(
        session_id=config["configurable"]["session_id"],
        entrada="¿Qué máquina necesito nivelar un terreno?",
        resultado=resultado_1
    )
