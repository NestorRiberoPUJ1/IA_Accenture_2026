from pydantic import BaseModel, Field
from langchain_core.tools import tool

from cprint import cprint


class ArgumentosConsultaEnvio(BaseModel):

    numero_seguimiento: str = Field(
        description=(
            "Número de seguimiento del envío, "
            "por ejemplo 'AR12345'."
        ),
    )
    incluir_historial: bool = Field(
        default=False,
        description=(
            "Si es True, incluye el historial "
            "completo de estados, no solo el "
            "actual."
        ),
    )


ESTADOS = {
    "AR12345": {
        "actual": "en tránsito, llega en 2 días",
        "historial": [
            "recibido en depósito",
            "en tránsito",
        ],
    },
}


@tool(
    "consultar_estado_envio_con_historial",
    args_schema=ArgumentosConsultaEnvio
)
def consultar_estado_envio_detallado(
    numero_seguimiento: str,
    incluir_historial: bool = False
) -> str:
    """Consulta el estado de un envío, con la
    opción de incluir su historial completo."""
    envio = ESTADOS.get(numero_seguimiento)
    if envio is None:
        return (
            f"No se encontró un envío con el "
            f"número {numero_seguimiento}."
        )
    if not incluir_historial:
        return envio["actual"]
    historial = ", ".join(envio["historial"])
    return f"{envio['actual']} (historial: {historial})"


if __name__ == "__main__":
    resultado_1 = (
        consultar_estado_envio_detallado.invoke({
            "numero_seguimiento": "AR12345",
            "incluir_historial": True
        })
    )
    cprint.err(resultado_1)
