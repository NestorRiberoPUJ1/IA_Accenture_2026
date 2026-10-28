
from collections import Counter
import re


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

if __name__ == "__main__":
    texto = "El gato y el perro"
    texto_limpio = limpiar_texto(texto)
    print(texto_limpio)
    tokens = tokenizar(texto_limpio)
    print(tokens)
    vectores = vectorizar(tokens)
    print(vectores)