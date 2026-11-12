from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from cprint import cprint
 
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(persist_directory="vectorstore/", embedding_function=embeddings)
 
resultados = vectorstore.similarity_search(
    "Puedo devolver algo que pedí hoy mismo?",
    k=1,
)
for r in resultados:
    cprint.fatal (r.page_content)

resultados_con_score = vectorstore.similarity_search_with_score(
    "Puedo devolver algo que pedí hoy mismo?", k=5
)
for doc_, score in resultados_con_score:
    print(round(score, 4), doc_.page_content[:50])

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
resultados = retriever.invoke("Si no me gustó el producto la devolución es gratis?")
for r in resultados:
    print(r.page_content, "|", r.metadata)

