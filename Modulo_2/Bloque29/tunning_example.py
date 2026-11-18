from google.genai import types
from dotenv import load_dotenv
from google import genai
import json
 
load_dotenv()

ejemplos_raw = [
	("TimeoutError: la conexion tardo mas de 10 segundos en responder.",
 	{"categoria": "red", "accion_sugerida": "reintentar con backoff exponencial"}),
	("ValueError: la clave de API no tiene el formato esperado.",
 	{"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
	("429 RESOURCE_EXHAUSTED: se supero el limite de peticiones por minuto.",
 	{"categoria": "cuota", "accion_sugerida": "esperar y reintentar, con backoff"}),
	("API key not valid. Please pass a valid API key.",
 	{"categoria": "autenticacion", "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"}),
	("RuntimeError: Your system has an unsupported version of sqlite3.",
 	{"categoria": "entorno", "accion_sugerida": "instalar pysqlite3-binary"}),
	("ModuleNotFoundError: No module named langchain_chroma.",
 	{"categoria": "entorno", "accion_sugerida": "instalar dependencia faltante"}),
	("PermissionError al crear la carpeta del vector store.",
 	{"categoria": "entorno", "accion_sugerida": "revisar permisos de escritura"}),
	("InvalidArgumentError: Collection expecting embedding with dimension of 768, got 1536.",
 	{"categoria": "consistencia_indice", "accion_sugerida": "reindexar con el mismo modelo de embeddings"}),
]
 
examples = [
	types.TuningExample(text_input=texto, output=json.dumps(salida, ensure_ascii=False))
	for texto, salida in ejemplos_raw
]

client = genai.Client()
 
dataset = types.TuningDataset(examples=examples)
 
config = types.CreateTuningJobConfig(
	tuning_mode=types.TuningMode.TUNING_MODE_PEFT_ADAPTER,
	adapter_size=types.AdapterSize.ADAPTER_SIZE_FOUR,
	epoch_count=5,
	tuned_model_display_name="clasificador-errores-cliente",
)
 
try:
	trabajo = client.tunings.tune(
    	base_model="models/gemini-2.0-flash",
    	training_dataset=dataset,
    	config=config,
	)
	print(trabajo)
except Exception as error:
	print("No se pudo crear el trabajo de tuning:", error)