from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from cprint import cprint

texto = (
    "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente "
    "entre intento e intento.\n\n"
    "Los errores de autenticacion nunca se reintentan: fallan de inmediato con un "
    "ValueError, sin ninguna espera.\n\n"
    "El costo de cada llamada se acumula en una variable de sesion mientras el "
    "programa sigue corriendo."
)



splitter_fijo = CharacterTextSplitter(
    separator="", chunk_size=210, chunk_overlap=0
)
chunks_fijo = splitter_fijo.split_text(texto)

for i, chunk in enumerate(chunks_fijo):
    cprint.err(f"--- chunk {i} ({len(chunk)} caracteres) ---")
    cprint.info(chunk)


splitter_recursivo = RecursiveCharacterTextSplitter(
    chunk_size=210, chunk_overlap=20,
)
chunks_recursivo = splitter_recursivo.split_text(texto)

for i, chunk in enumerate(chunks_recursivo):
    cprint.ok(f"--- chunk {i} ({len(chunk)} caracteres) ---")
    cprint.info(chunk)