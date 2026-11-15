from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

casos_evaluacion = [
	{"pregunta": "Cual es el accesorio más usado en excavadoras", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Cual es la capacidad de carga de una grúa", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Que tipo de aceite se usa en excavadoras", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Cual es la vida útil de una excavadora", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Que medidas de seguridad se deben tomar", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Cual es el mantenimiento preventivo", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Que tipo de combustible utilizan las excavadoras", "ids_relevantes": {"id_del_chunk_correcto"}},
	{"pregunta": "Cual es el peso de una excavadora", "ids_relevantes": {"id_del_chunk_correcto"}},
]


 

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma(persist_directory="vectorstore/", embedding_function=embeddings)
print(vectorstore.get()["ids"])