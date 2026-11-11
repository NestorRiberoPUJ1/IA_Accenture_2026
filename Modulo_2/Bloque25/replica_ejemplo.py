import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

EMBEDDINGS = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")

if not os.environ.get("GEMINI_API_KEY"):
	raise SystemExit('Falta GEMINI_API_KEY. Defínela en tu archivo ".env" y vuelve a ejecutar.')


corpus_ejemplo = [
    "Los pedidos se pueden cancelar dentro de las primeras 24 horas despues de "
    "realizados, sin costo adicional.",
    "Las devoluciones se aceptan hasta 30 dias despues de la entrega, siempre que "
    "el producto este sin usar.",
    "El reembolso se procesa en un plazo de 5 a 10 dias habiles despues de recibir "
    "el producto devuelto.",
    "Los productos en oferta o liquidacion no tienen devolucion, salvo defecto de "
    "fabrica.",
    "El envio de una devolucion corre por cuenta del cliente, excepto cuando el "
    "producto llego danado.",
]


def validar_chunks(chunks,corpus):
    vacios = [i for i, c in enumerate(chunks) if not c.page_content.strip()]
    textos = [c.page_content for c in chunks]
    hay_duplicados = len(textos) != len(set(textos))
    total_chars_chunks = sum(len(c.page_content) for c in chunks)
    total_chars_corpus = sum(len(d) for d in corpus)
    es_valido= (len(vacios) == 0) and (not hay_duplicados) and (total_chars_chunks == total_chars_corpus)
    return es_valido


def indexar_corpus(corpus, persist_directory, chunk_size=200, chunk_overlap=30):
    """Parte, calcula embeddings y persiste un corpus. Devuelve el vector store."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.create_documents(corpus)

    print(f"{len(chunks)} chunks generados")
    for i, chunk in enumerate(chunks):
        print(f"--- chunk {i} ({len(chunk.page_content)} caracteres) ---")
        print(chunk.page_content)

    
    try:
        if not validar_chunks(chunks, corpus):
            raise ValueError("Los chunks generados no son válidos: hay vacíos, duplicados o la suma de caracteres no coincide con el corpus original.")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=EMBEDDINGS,
            persist_directory=persist_directory,
        )
        print(f"Indexados {len(chunks)} chunks en {persist_directory}")
        return vectorstore
    except Exception as error:
        mensaje = str(error)
        if "429" in mensaje or "RESOURCE_EXHAUSTED" in mensaje:
            print("Límite de peticiones alcanzado. Espera un minuto y vuelve a ejecutar.")
        elif "API key" in mensaje or "401" in mensaje or "403" in mensaje:
            print('La API rechazó tu clave. Revisa el valor de GEMINI_API_KEY en tu ".env".')
        else:
            print("No se pudo indexar el corpus:", type(error).__name__)
        print("Detalle técnico:", mensaje)
        raise SystemExit(1)

def cargar_vectorstore(persist_directory):
    """Reconecta a un vector store ya indexado, sin recalcular nada."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

if __name__ == "__main__":
    indexar_corpus(corpus_ejemplo, "vectorstore_ejemplo/", 150, 20)
    vectorstore = cargar_vectorstore("vectorstore_ejemplo/")
    print(vectorstore._collection.count())
