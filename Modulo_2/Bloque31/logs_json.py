import json
import logging
import sys
import contextvars
import uuid
import hashlib

from cprint import cprint

trace_id_var = contextvars.ContextVar("trace_id", default=None)
 
class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if hasattr(record, "trace_id"):
            payload["trace_id"] = record.trace_id
        if hasattr(record, "extra_data"):
            payload.update(record.extra_data)
        return json.dumps(payload, ensure_ascii=False)

def procesar(pregunta):
    token = trace_id_var.set("trace-" + uuid.uuid4().hex[:8])
    try:
        print("trace_id activo:", trace_id_var.get())
        sub_paso()
    finally:
        trace_id_var.reset(token)
         
def sub_paso():
    print("  dentro de sub_paso, mismo trace_id sin pasarlo como argumento:",trace_id_var.get())

def huella(texto):
	return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
 
 

logger = logging.getLogger("rag_pipeline")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.propagate = False
 
logger.info("consulta recibida", extra={
	"trace_id": "abc-123", "extra_data": {"pregunta_len": 42},
})
logger.info("documentos recuperados", extra={
	"trace_id": "abc-123", "extra_data": {"k": 4, "fuente_top": "manual.pdf"},
})


procesar("cual es la politica de devoluciones")
cprint.err("fuera del contexto:", trace_id_var.get())


doc1 = "Politica de devoluciones: 30 dias desde la compra."
doc2 = "Politica de devoluciones: 31 dias desde la compra."
doc3 = "Politica de envios: 5 dias habiles a todo el pais."
 
print("doc1 huella:", huella(doc1), "longitud:", len(doc1))
print("doc2 huella:", huella(doc2), "longitud:", len(doc2))
print("doc3 huella:", huella(doc3), "longitud:", len(doc3))
print("doc1 == doc2 (mismo contenido)?", huella(doc1) == huella(doc2))