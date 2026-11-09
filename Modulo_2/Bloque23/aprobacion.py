import select
import sys
from datetime import datetime
from langchain_core.tools import tool

registro_aprobaciones = []

def esperar_aprobacion(
    mensaje: str,
    tiempo_limite_segundos: int = 300
) -> bool:
    print(mensaje)
    listo, _, _ = select.select(
        [sys.stdin], [], [], tiempo_limite_segundos
    )
    if not listo:
        return False
    respuesta = sys.stdin.readline()
    return respuesta.strip().lower() == "s"

def registrar_aprobacion(
    herramienta: str,
    argumentos: dict,
    aprobado: bool,
) -> None:
    registro_aprobaciones.append({
        "herramienta": herramienta,
        "argumentos": argumentos,
        "aprobado": aprobado,
        "momento": datetime.now().isoformat(),
    })

@tool
def generar_reembolso(numero_pedido: str, monto: float) -> str:
    """Genera un reembolso para un pedido. Acción
    irreversible: requiere aprobación humana antes
    de ejecutarse."""
    mensaje = (
        f"El agente quiere reembolsar ${monto} "
        f"para el pedido {numero_pedido}. "
        f"¿Aprobar? (s/n): "
    )
    aprobado = esperar_aprobacion(mensaje)
    registrar_aprobacion(
        herramienta="generar_reembolso",
        argumentos={"numero_pedido": numero_pedido, "monto": monto},
        aprobado=aprobado,
    )

    if not aprobado:
        return (
            "Reembolso no aprobado por el "
            "supervisor humano."
        )

    return (
        f"Reembolso de ${monto} generado para "
        f"el pedido {numero_pedido}."
    )

if __name__ == "__main__":
    resultado = generar_reembolso.invoke(
        {"numero_pedido": "PED789", "monto": 1500.0}
    )
    print(resultado)
    print("registro:", registro_aprobaciones)