import os
from importlib.metadata import version, PackageNotFoundError
 
from dotenv import load_dotenv
 
load_dotenv()
 
try:
	print("google-genai instalado, versión", version("google-genai"))
except PackageNotFoundError:
	raise SystemExit("Falta la librería. Ejecuta: pip install google-genai python-dotenv")
 
if os.environ.get("GEMINI_API_KEY"):
	print("GEMINI_API_KEY detectada")
else:
	raise SystemExit('Falta GEMINI_API_KEY. Agrégala al archivo ".env" de tu proyecto.')
