try:
    from google.genai import types
except ImportError:
    raise SystemExit(
        "No se pudo importar google.genai. Ejecuta: pip install google-genai")

try:
    print("Modos de tuning disponibles:")
    for modo in types.TuningMode:
        print(" ", modo)

    print()
    print("Tamaños de adapter disponibles (solo aplica a PEFT):")
    for tamanio in types.AdapterSize:
        print(" ", tamanio)
except AttributeError as e:
    raise SystemExit(
        f"Tu versión del SDK no expone este tipo: {e}. Actualiza con: pip install -U google-genai")
from google.genai import types
 
for campo in ["epoch_count", "learning_rate_multiplier", "batch_size"]:
    try:
        descripcion = types.CreateTuningJobConfig.model_fields[campo].description
        print(campo, "->", descripcion)
    except KeyError:
    	print(campo, "-> este campo no existe en tu versión del SDK")


from google.genai import types
 
print("Estados posibles de un trabajo de tuning:")
for estado in types.JobState:
	print(" ", estado)


import time
 
def esperar_a_que_termine(client, nombre_trabajo, intervalo_segundos=30):
    """Consulta el estado del trabajo hasta que termine, en cualquier sentido."""
    estados_finales = {
        types.JobState.JOB_STATE_SUCCEEDED,
        types.JobState.JOB_STATE_FAILED,
        types.JobState.JOB_STATE_CANCELLED,
        types.JobState.JOB_STATE_PARTIALLY_SUCCEEDED,
    }
    while True:
        trabajo = client.tunings.get(name=nombre_trabajo)
        print(f"estado actual: {trabajo.state}")
        if trabajo.state in estados_finales:
            return trabajo
        time.sleep(intervalo_segundos)
