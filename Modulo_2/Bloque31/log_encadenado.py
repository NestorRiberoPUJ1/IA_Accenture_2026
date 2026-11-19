
from typing import List
 
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableLambda
 
 
class RetrieverFijo(BaseRetriever):
    documentos: List[Document] = []
 
    def _get_relevant_documents(self, query, *, run_manager=None):
        return self.documentos
 
 
class HandlerDeCadena(BaseCallbackHandler):
    def __init__(self):
        self.raiz = None
        self.eventos = []
 
    def on_chain_start(self, serialized, inputs, *, run_id,
                   	parent_run_id=None, **kwargs):
        if parent_run_id is None:
            self.raiz = run_id  # la cadena completa no tiene padre
 
    def on_retriever_start(self, serialized, query, *, run_id,
                       	parent_run_id=None, metadata=None, **kwargs):
        self.eventos.append(("retriever", parent_run_id, metadata))
 
    def on_llm_start(self, serialized, prompts, *, run_id,
                 	parent_run_id=None, metadata=None, **kwargs):
    	self.eventos.append(("llm", parent_run_id, metadata))
 
 
docs = [Document(page_content="Politica de devoluciones: 30 dias.")]
retriever = RetrieverFijo(documentos=docs)
a_contexto = RunnableLambda(lambda documentos: documentos[0].page_content)
llm = FakeListLLM(responses=["Respuesta simulada."])
cadena = retriever | a_contexto | llm
 
handler = HandlerDeCadena()
cadena.invoke(
	"cual es la politica de devoluciones",
	config={"callbacks": [handler], "metadata": {"trace_id": "abc-123"}},
)
 
for etapa, padre, metadata in handler.eventos:
	print(f"{etapa}: hijo de la cadena = {padre == handler.raiz}, "
      	f"trace_id = {metadata['trace_id']}")