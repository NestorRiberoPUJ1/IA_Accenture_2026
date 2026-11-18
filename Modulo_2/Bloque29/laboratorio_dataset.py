import json
from google.genai import types
from collections import Counter
 
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
 
print(len(examples), "ejemplos construidos")
print(examples[0])

def validar_dataset(examples, claves_esperadas=("categoria", "accion_sugerida")):
    problemas = []
    vistos = set()
    for i, ej in enumerate(examples):
        if not ej.text_input or not ej.text_input.strip():
            problemas.append(f"ejemplo {i}: text_input vacio")
        if not ej.output or not ej.output.strip():
            problemas.append(f"ejemplo {i}: output vacio")
            continue
        if ej.text_input in vistos:
            problemas.append(f"ejemplo {i}: text_input duplicado")
        vistos.add(ej.text_input)
        try:
            salida = json.loads(ej.output)
        except json.JSONDecodeError:
            problemas.append(f"ejemplo {i}: output no es JSON valido")
            continue
        for clave in claves_esperadas:
            if clave not in salida:
                problemas.append(f'ejemplo {i}: output no tiene la clave "{clave}"')
    return problemas
 
 
problemas = validar_dataset(examples)
print(f"{len(examples)} ejemplos, {len(problemas)} problemas encontrados")
for p in problemas:
	print(" -", p)


def chequear_balance(ejemplos_raw):
	categorias = Counter(salida["categoria"] for _, salida in ejemplos_raw)
	return categorias
 
 
balance = chequear_balance(ejemplos_raw)
for categoria, cuenta in balance.most_common():
	print(f"{categoria}: {cuenta}")
 
maximo = max(balance.values())
minimo = min(balance.values())
print()
print(f"categoria mas representada: {maximo} ejemplos")
print(f"categoria menos representada: {minimo} ejemplos")
print(f"razon max/min: {maximo / minimo:.1f}x")