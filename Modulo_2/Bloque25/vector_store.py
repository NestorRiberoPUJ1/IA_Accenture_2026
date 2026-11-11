import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

import time

load_dotenv()

PERSIST_DIR = os.path.abspath("vectorstore")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = Chroma(
    collection_name="corpus_ejemplo",
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)

print("Ruta del índice:", PERSIST_DIR)
print("Colección:", vectorstore._collection.name)
print("Chunks:", vectorstore._collection.count())


def con_reintentos(operacion, max_intentos=4, espera_inicial=5):
    espera = espera_inicial
    for intento in range(1, max_intentos + 1):
        try:
            return operacion()
        except Exception as error:
            mensaje = str(error)
            es_limite = "429" in mensaje or "RESOURCE_EXHAUSTED" in mensaje
            if not es_limite or intento == max_intentos:
                raise
            print(
                f"Límite de peticiones alcanzado. Reintento {intento} de {max_intentos - 1} en {espera} s...")
            time.sleep(espera)
            espera *= 2


vectorstore = con_reintentos(
    lambda: Chroma.from_documents(
        documents=[],
        embedding=embeddings,
        collection_name="corpus_ejemplo",
        persist_directory=PERSIST_DIR,
    )
)
