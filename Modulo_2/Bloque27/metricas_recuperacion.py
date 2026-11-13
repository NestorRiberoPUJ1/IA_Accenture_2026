
from cprint import cprint

# Función para calcular la precisión en k resultados recuperados
def precision_at_k(ids_recuperados, ids_relevantes):
	"""Fraccion de los ids recuperados que de verdad son relevantes."""
	acertados = [i for i in ids_recuperados if i in ids_relevantes]
	return len(acertados) / len(ids_recuperados)

# Función para calcular el recall en k resultados recuperados
def recall_at_k(ids_recuperados, ids_relevantes):
	"""Fraccion de los ids relevantes que efectivamente se recuperaron."""
	acertados = [i for i in ids_recuperados if i in ids_relevantes]
	return len(acertados) / len(ids_relevantes)

# Función para calcular la medida F1
def f1(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

corpus = {
	"doc0": "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente.",
	"doc1": "Los errores de autenticacion nunca se reintentan: fallan de inmediato con un ValueError.",
	"doc2": "El costo de cada llamada se calcula a partir de totalTokenCount y la tarifa vigente por cada 1000 tokens.",
	"doc3": "El agente de la Unidad 2.4 decide por si mismo que herramienta usar, segun la descripcion de cada una.",
	"doc4": "Las pruebas unitarias del cliente usan mocks, de forma que la suite completa corre en menos de un segundo.",
}
pregunta = "que hace el cliente si una llamada tarda demasiado?"
 
ids_relevantes = {"doc0"}
ids_recuperados = ["doc2", "doc0", "doc4"]
ranked = ["doc2", "doc4", "doc0", "doc1", "doc3"]

cprint.err(precision_at_k(ids_recuperados, ids_relevantes))
cprint.info(recall_at_k(ids_recuperados, ids_relevantes))

for k in range(1, 6):
	sub = ranked[:k]
	p = precision_at_k(sub, ids_relevantes)
	r = recall_at_k(sub, ids_relevantes)
	cprint.ok(f"k={k}: precision={p:.3f}  recall={r:.3f}  recuperados={sub}")
	
for k in range(1, 6):
	sub = ranked[:k]
	p = precision_at_k(sub, ids_relevantes)
	r = recall_at_k(sub, ids_relevantes)
	cprint.info(f"k={k}: F1={f1(p, r):.3f}")