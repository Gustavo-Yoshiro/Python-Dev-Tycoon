from abc import ABC, abstractmethod
from Intermediario.Persistencia.Entidade.Dialogo import DialogoNo, DialogoOpcao

# --- Interface para DialogoNo ---
class DialogoNoPersistencia(ABC):
    
    @abstractmethod
    def salvar(self, no):
        pass

    @abstractmethod
    def buscar_no_inicial(self, id_projeto):
        pass

    @abstractmethod
    def buscar_por_id(self, id_no):
        pass

# --- Interface para DialogoOpcao ---
class DialogoOpcaoPersistencia(ABC):

    @abstractmethod
    def salvar(self, opcao):
        pass

    @abstractmethod
    def buscar_opcoes_por_no_origem(self, id_no_origem):
        pass
