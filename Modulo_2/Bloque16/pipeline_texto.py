
from collections import Counter
import re
from cliente import consultar_modelo
import json


def limpiar_texto(texto: str) -> str:
    """Normaliza el texto: minúsculas y sin puntuación."""
    if not isinstance(texto, str):
        raise ValueError("El argumento debe ser una cadena de texto.")
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokenizar(texto_limpio: str) -> list[str]:
    """Convierte texto limpio en una lista de tokens."""
    return texto_limpio.split()


def vectorizar(tokens: list[str]) -> Counter:
    """Cuenta cuántas veces aparece cada token."""
    return Counter(tokens)


def procesar_texto(texto: str) -> list[str]:
    texto_limpio = limpiar_texto(texto)
    return tokenizar(texto_limpio)


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())


def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado


def calcular_metricas(texto_referencia, texto_respuesta):

    tokens_referencia = procesar_texto(texto_referencia)

    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )
def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }

if __name__ == "__main__":
    pregunta = "Qué Colombiano estuvo cerca de ganarle a Federer en Wimbledon?"
    instruccion = "Solo Nombre completo"
    referencia = "Alejandro Falla"
    respuesta = consultar_modelo(pregunta, instruccion)

    resultados = calcular_metricas(referencia, respuesta)
    print(f"Resultados: {resultados}")

    casos = [

        (
            "¿Qué es Python?",
            "Python es un lenguaje de programación interpretado.",
        ),

        ("¿Cuándo se creó Python?", "Python fue creado en 1991."),

        (
            "¿Qué es una lista en Python?",
            "Una lista es una colección ordenada y modificable.",
        ),

    ]


    resultados = []

    for consulta, referencia in casos:

        respuesta = consultar_modelo(consulta, "Proporciona una respuesta breve y precisa.")

        metricas = calcular_metricas(referencia, respuesta)

        resultados.append({
            "consulta": consulta,
            "respuesta": respuesta,
            **metricas,
        })


    with open(
        "resultados_metricas.json", "w", encoding="utf-8"
    ) as archivo:

        json.dump(resultados, archivo, indent=2, ensure_ascii=False)

    resumen = resumir_metricas(resultados)
    print(f"Resumen de métricas: {resumen}")