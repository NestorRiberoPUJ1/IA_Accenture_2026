from cprint import cprint

def recomendar_estrategia(respuestas):
    puntos = {"RAG": 0, "Fine-tuning completo": 0, "PEFT": 0}
 
    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3
    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1
    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1
    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1
    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2
 
    # puntos.values() son solo los puntajes (por ejemplo [0, 3, 3]); max() toma el mayor.
    maximo = max(puntos.values())
    # puntos.items() entrega pares (tecnica, puntaje). La comprension de listas se lee:
    # "para cada par, guarda la tecnica si su puntaje es igual al maximo".
    # Asi se conservan TODAS las empatadas, no solo la primera que encuentra max().
    ganadoras = [tecnica for tecnica, p in puntos.items() if p == maximo]
    return puntos, ganadoras

# caso: clasificador de errores del cliente (Bloque 29) -- dataset grande,
# sin necesidad de conocimiento externo que cambie
respuestas_caso2 = {
	"informacion_cambia_seguido": False,
	"problema_de_formato_o_tono": True,
	"dataset_grande_y_de_calidad": True,
	"presupuesto_limitado_o_iterar_rapido": False,
	"necesita_multiples_variantes": False,
}
 
puntos2, ganadoras2 = recomendar_estrategia(respuestas_caso2)
print("caso 2:", puntos2)
print("candidatas empatadas:", ganadoras2)

for clave in respuestas_caso2:
	variante = dict(respuestas_caso2)
	variante[clave] = not variante[clave]
	puntos_v, ganadoras_v = recomendar_estrategia(variante)
	cambio = "CAMBIA" if set(ganadoras_v) != set(ganadoras2) else "igual"
	cprint.info(f"{clave} -> {not respuestas_caso2[clave]}: {ganadoras_v}  [{cambio}]")