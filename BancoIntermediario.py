from Intermediario.Persistencia.Impl.Banco import BancoDeDadosIntermediario

banco = BancoDeDadosIntermediario()
banco.apagarTabelas()
banco.criarBanco()