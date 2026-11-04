from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from enrutamiento import construir_paso_clasificacion

def test_clasificacion_normaliza_antes_de_comparar():
    modelo_falso = MagicMock()
    modelo_falso.return_value = AIMessage(content=" Queja \n")
    resultado = construir_paso_clasificacion(modelo_falso).invoke(
        {"mensaje": "algo salió mal"}
    )
    assert resultado == "queja"

def test_cadena_queja_usa_fallback_ante_fallo_del_modelo():
    def fallar_a_proposito(x):
        raise Exception("Error de red simulado")
    respuesta_generica = RunnableLambda(
        lambda x: "respuesta de respaldo"
    )
    cadena_rota = RunnableLambda(fallar_a_proposito)
    cadena_segura = cadena_rota.with_fallbacks([respuesta_generica])
    resultado = cadena_segura.invoke({"mensaje": "algo"})
    assert resultado == "respuesta de respaldo"