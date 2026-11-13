from cprint import cprint

casos_evaluacion = [
	{"pregunta": "que hace el cliente si una llamada tarda demasiado",
 	"ids_relevantes": {"doc0"}},
	{"pregunta": "que pasa si la clave de api es invalida",
 	"ids_relevantes": {"doc1"}},
	{"pregunta": "como se calcula el costo de una llamada",
 	"ids_relevantes": {"doc2"}},
	{"pregunta": "como decide el agente que herramienta usar",
 	"ids_relevantes": {"doc3"}},
]

ids_recuperados_por_pregunta = {
	"que hace el cliente si una llamada tarda demasiado": ["doc0", "doc4", "doc2"],
	"que pasa si la clave de api es invalida": ["doc2", "doc4", "doc3"],
	"como se calcula el costo de una llamada": ["doc2", "doc0", "doc4"],
	"como decide el agente que herramienta usar": ["doc4", "doc3", "doc1"],
}
 

def precision_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float:
    """Fraccion de los ids recuperados que son relevantes.
	Devuelve 0.0 si el retriever no devolvio ningun id."""
    if not ids_recuperados:
        return 0.0
    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_recuperados)
 
 
def recall_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float | None:
    """Fraccion de los ids relevantes que se recuperaron.
	Devuelve None si el caso no tiene ids relevantes (no hay nada que recuperar)."""
    if not ids_relevantes:
        return None
    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_relevantes)

def f1(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
 
def promediar(valores) -> float:
	"""Promedio que ignora los None y evita dividir por cero."""
	validos = [v for v in valores if v is not None]
	return sum(validos) / len(validos) if validos else 0.0
 
 
def evaluar_recuperacion(retriever, casos, k=3):
    """Corre cada caso contra el retriever real y promedia precision y recall."""
    resultados = []
    for caso in casos:
        chunks = retriever.invoke(caso["pregunta"])
        ids_recuperados = [c.id for c in chunks][:k]
        p = precision_at_k(ids_recuperados, caso["ids_relevantes"])
        r = recall_at_k(ids_recuperados, caso["ids_relevantes"])
        resultados.append({"pregunta": caso["pregunta"], "precision": p, "recall": r})
 
    precision_promedio = promediar(x["precision"] for x in resultados)
    recall_promedio = promediar(x["recall"] for x in resultados)
    return resultados, precision_promedio, recall_promedio


def evaluar_recuperacion_simulada(casos, k=3):
    resultados = []
    for caso in casos:
        ids_recuperados = ids_recuperados_por_pregunta[caso["pregunta"]][:k]
        p = precision_at_k(ids_recuperados, caso["ids_relevantes"])
        r = recall_at_k(ids_recuperados, caso["ids_relevantes"])
        resultados.append({
            "pregunta": caso["pregunta"][:40],
            "precision": round(p, 3),
            "recall": r,
        })
    precision_promedio = promediar(x["precision"] for x in resultados)
    recall_promedio = promediar(x["recall"] for x in resultados)
    return resultados, round(precision_promedio, 3), round(recall_promedio, 3)
 
 
resultados, p_prom, r_prom = evaluar_recuperacion_simulada(casos_evaluacion)
for r in resultados:
	cprint.info(r)
cprint.err(f"precision promedio: {p_prom}")
cprint.ok(f"recall promedio: {r_prom}")
f1=f1(p_prom, r_prom)
cprint.ok(f"F1 promedio: {f1:.3f}")