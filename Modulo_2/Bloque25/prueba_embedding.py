import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


def indexar_corpus(corpus, persist_directory, chunk_size=200, chunk_overlap=30):
    """Parte, calcula embeddings y persiste un corpus. Devuelve el vector store."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.create_documents(corpus)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    print(f"Indexados {len(chunks)} chunks en {persist_directory}")
    return vectorstore


def cargar_vectorstore(persist_directory):
    """Reconecta a un vector store ya indexado, sin recalcular nada."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001")
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)


if __name__ == "__main__":
    corpus = [
        "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente.",
        "El costo de cada llamada se calcula a partir de totalTokenCount.",
        "Las pruebas unitarias del cliente usan mocks y corren en menos de un segundo.",
    ]

    indexar_corpus(corpus, "vectorstore/")

    vectorstore = cargar_vectorstore("vectorstore/")
    print(vectorstore._collection.count())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=30
    )
    nuevos_chunks = splitter.create_documents(["... un documento nuevo del corpus ..."])
 
    # ids explicitos: permiten reemplazar o borrar chunks puntuales mas adelante
    ids_nuevos = [f"doc_nuevo_{i}" for i in range(len(nuevos_chunks))]
    
    vectorstore.add_documents(nuevos_chunks, ids=ids_nuevos)
    print(f"Agregados {len(nuevos_chunks)} chunks nuevos, sin recalcular los existentes")

    vectorstore = cargar_vectorstore("vectorstore/")
    print(vectorstore._collection.count())
    
    # borrar chunks puntuales por id, sin tocar el resto del indice
    vectorstore.delete(ids=["doc_nuevo_0"])

    vectorstore = cargar_vectorstore("vectorstore/")
    print(vectorstore._collection.count())
