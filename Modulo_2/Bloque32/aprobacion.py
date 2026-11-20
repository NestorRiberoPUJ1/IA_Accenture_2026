from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import uuid
 

from cprint import cprint  

class Estado(TypedDict):
    version_nueva: str
    aprobado: bool
 
def proponer_version(estado: Estado):
    print("nodo: proponer_version, version propuesta:", estado["version_nueva"])
    return {}
 
def punto_de_supervision(estado: Estado):
    decision = interrupt({
        "motivo": "aprobar despliegue de nueva version de prompt a produccion",
        "version_propuesta": estado["version_nueva"],
    })
    return {"aprobado": decision}
 
def desplegar(estado: Estado):
    print("nodo: desplegar. aprobado =", estado["aprobado"])
    if estado["aprobado"]:
        print("  -> version", estado["version_nueva"], "desplegada a produccion")
    else:
        print("  -> despliegue RECHAZADO, version anterior se mantiene")
    return {}
 
def nuevo_thread_id(prefijo="despliegue"):
	return f"{prefijo}-{uuid.uuid4().hex[:8]}"

def resolver(app, config, aprobar):
    snapshot = app.get_state(config)
    if not snapshot.next:
        raise ValueError("este thread_id no tiene ninguna aprobacion pendiente")
    return app.invoke(Command(resume=aprobar), config=config)
 

conn = sqlite3.connect("checkpoints.db", check_same_thread=False) 

grafo = StateGraph(Estado)
grafo.add_node("proponer_version", proponer_version)
grafo.add_node("punto_de_supervision", punto_de_supervision)
grafo.add_node("desplegar", desplegar)
grafo.add_edge(START, "proponer_version")
grafo.add_edge("proponer_version", "punto_de_supervision")
grafo.add_edge("punto_de_supervision", "desplegar")
grafo.add_edge("desplegar", END)
 
#app = grafo.compile(checkpointer=InMemorySaver())
app = grafo.compile(checkpointer=SqliteSaver(conn))
config = {"configurable": {"thread_id": nuevo_thread_id()}}
 
resultado = app.invoke({"version_nueva": "v3", "aprobado": False}, config=config)
cprint.info("estado tras primera corrida (interrumpido):")
cprint.err(resultado)

print(resolver(app, config, True)) # primera reanudacion

try: # segunda reanudacion, ya no hay aprobacion pendiente
	resolver(app, config, True)
except ValueError as e:
	print("ValueError:", e)