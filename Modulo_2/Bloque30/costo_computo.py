from dotenv import load_dotenv
from google import genai
 
load_dotenv()
client = genai.Client()
 
# el valor de trabajo.name que guardaste al enviar tu trabajo en la lección anterior
nombre_trabajo = "NOMBRE_DE_TU_TRABAJO"
 
try:
	trabajo = client.tunings.get(name=nombre_trabajo)
except Exception as error:
	raise SystemExit(f"No se pudo consultar el trabajo de tuning: {error}")
 
if trabajo.tuning_data_stats is None or trabajo.tuning_data_stats.supervised_tuning_data_stats is None:
	raise SystemExit("El trabajo todavía no tiene estadísticas de datos. Espera a que termine y vuelve a ejecutar.")
 
stats = trabajo.tuning_data_stats.supervised_tuning_data_stats
 
print("ejemplos usados:", stats.tuning_dataset_example_count)
print("ejemplos truncados:", stats.total_truncated_example_count)
print("tokens facturables totales:", stats.total_billable_token_count)
print("caracteres facturables totales:", stats.total_billable_character_count)
print("pasos de entrenamiento:", stats.tuning_step_count)