from langchain_text_splitters import RecursiveCharacterTextSplitter
 
corpus = [
    "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente. "
    "Los errores de autenticacion nunca se reintentan: fallan de inmediato con un "
    "ValueError.",
    "El costo de cada llamada se calcula a partir de totalTokenCount y la tarifa "
    "vigente por cada 1000 tokens.",
    "El servicio está disponible 24/7 con uns SLA de 99.9%"
]
metadatas = [
    {"fuente": "manual_cliente.md"},
    {"fuente": "manual_costos.md"},
    {"fuente": "manual_sla.md"}
]
 
splitter = RecursiveCharacterTextSplitter(chunk_size=90, chunk_overlap=10)
chunks = splitter.create_documents(corpus, metadatas=metadatas)
for c in chunks:
    print(repr(c.page_content), "->", c.metadata)


def formatear_contexto(chunks_recuperados):
    """Arma un bloque de contexto numerado para el prompt, y un mapa
    numero -> fuente para reconstruir la cita despues."""
    lineas = []
    citas = {}
    for i, doc in enumerate(chunks_recuperados, start=1):
        fuente = doc.metadata.get("fuente", "desconocida")
        lineas.append(f"[{i}] {doc.page_content}")
        citas[i] = fuente
    contexto = "\n\n".join(lineas)
    return contexto, citas
 
 
contexto, citas = formatear_contexto(chunks)
print(contexto)
print(citas)


PROMPT_TEMPLATE = """Responde la pregunta usando SOLO el contexto de abajo. Cita la \
fuente de cada afirmacion con su numero entre corchetes, como [1]. Si el contexto no \
alcanza para responder, dilo explicitamente en vez de inventar.
 
Contexto:
{contexto}
 
Pregunta: {pregunta}
 
Respuesta:"""
 
prompt = PROMPT_TEMPLATE.format(
    contexto=contexto,
    pregunta="Que hace el cliente si hay un TimeoutError?",
)
print(prompt)
