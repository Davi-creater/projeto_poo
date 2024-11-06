from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError, DataError

# Criação do engine e da sessão
engine = create_engine('sqlite:///locadora.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Classe Pessoa
class Pessoa(Base):
    __tablename__ = 'pessoas'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String)

    

# Classe Cliente herda de Pessoa
class Cliente(Pessoa):
    __tablename__ = 'clientes'

    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    cpf = Column(String)

    def __repr__(self):
        return f'\n{"-" * 40}\nCliente:\nId = {self.id}\nNome = {self.nome}\nCpf = {self.cpf}\nEndereço = {self.endereco}\nTelefone = {self.telefone}\n{"-" * 40}'

# Classe Midia
class Midia(Base):
    __tablename__ = 'midias'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    tipo = Column(String)  # Ex: Filme, Série, Documentário
    genero = Column(String)

    def __repr__(self):
        return f'\n{"-" * 40}\nMidia:\nTitulo = {self.titulo}\nTipo = {self.tipo}\nGenero = {self.genero}\n{"-" * 40}'

# Classe Locacao
class Locacao(Base):
    __tablename__ = 'locacoes'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    midia_id = Column(Integer, ForeignKey('midias.id'))
    data_locacao = Column(DateTime, default=datetime.now)
    data_devolucao = Column(DateTime)

    cliente = relationship('Cliente', back_populates='locacoes')
    midia = relationship('Midia', back_populates='locacoes')

    def __repr__(self):
        
        data_locacao = self.data_locacao.strftime('%d/%m/%Y') if self.data_locacao else 'Não informada'
        data_devolucao= self.data_devolucao.strftime('%d/%m/%Y') if self.data_devolucao else 'Não informada'
        return f'\n{"-" * 40}\nLocacao:\ncliente = {self.cliente.nome}\nmidia = {self.midia.titulo}\ndata_locacao = {data_locacao}\ndata_devolucao = {data_devolucao}\n{"-" * 40}'

Cliente.locacoes = relationship('Locacao', back_populates='cliente')
Midia.locacoes = relationship('Locacao', back_populates='midia')

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Funções para manipular dados com tratamento de exceções
def adicionar_cliente(nome, endereco, telefone, cpf):
    try:
        cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf)
        session.add(cliente)
        session.commit()
        print("Cliente adicionado com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (exemplo: dados duplicados): {e}")
    except DataError as e:
        session.rollback()
        print(f"Erro de dados inválidos (tipo incompatível): {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao adicionar cliente: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar cliente: {e}")

def adicionar_midia(titulo, tipo, genero):
    try:
        midia = Midia(titulo=titulo, tipo=tipo, genero=genero)
        session.add(midia)
        session.commit()
        print("Mídia adicionada com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (exemplo: dados duplicados): {e}")
    except DataError as e:
        session.rollback()
        print(f"Erro de dados inválidos (tipo incompatível): {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao adicionar mídia: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar mídia: {e}")

def registrar_locacao(cliente_id, midia_id, data_devolucao):
    try:
        locacao = Locacao(cliente_id=cliente_id, midia_id=midia_id, data_devolucao=data_devolucao)
        session.add(locacao)
        session.commit()
        print("Locação registrada com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (violação de chave estrangeira ou dados duplicados): {e}")
    except OperationalError as e:
        session.rollback()
        print(f"Erro de operação no banco de dados: {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao registrar locação: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao registrar locação: {e}")

def consultar_midias():
    try:
        midias = session.query(Midia).all()
        for midia in midias:
            print(midia)
    except SQLAlchemyError as e:
        print(f"Erro ao consultar mídias: {e}")
    except Exception as e:
        print(f"Erro inesperado ao consultar mídias: {e}")

def consultar_clientes():
    try:
        clientes = session.query(Cliente).all()
        for cliente in clientes:
            print(cliente)
    except SQLAlchemyError as e:
        print(f"Erro ao consultar clientes: {e}")
    except Exception as e:
        print(f"Erro inesperado ao consultar clientes: {e}")

def consultar_locacoes():
    try:
        locacoes = session.query(Locacao).all()
        for locacao in locacoes:
            print(locacao)
    except SQLAlchemyError as e:
        print(f"Erro ao consultar locações: {e}")
    except Exception as e:
        print(f"Erro inesperado ao consultar locações: {e}")

# Função principal com tratamento de exceção nas entradas de usuário
def main():
    while True:
        try:
            print('\nEscolha uma opção:')
            print('1. Adicionar Cliente')
            print('2. Adicionar Mídia')
            print('3. Registrar Locação')
            print('4. Consultar Mídias')
            print('5. Consultar Clientes')
            print('6. Consultar Locações')
            print('7. Sair')

            opcao = input('Opção: ')
            if opcao == '1':
                nome = input('Nome do Cliente: ')
                endereco = input('Endereço: ')
                telefone = input('Telefone: ')
                cpf = input('CPF: ')
                adicionar_cliente(nome, endereco, telefone, cpf)
            elif opcao == '2':
                titulo = input('Título da Mídia: ')
                tipo = input('Tipo (Filme/Série/Documentário): ')
                genero = input('Gênero: ')
                adicionar_midia(titulo, tipo, genero)
            elif opcao == '3':
                try:
                    cliente_id = int(input('ID do Cliente: '))
                    midia_id = int(input('ID da Mídia: '))
                    data_devolucao = input('Data de Devolução (DD/MM/YYYY): ')
                    data_devolucao = datetime.strptime(data_devolucao, '%d/%m/%Y')
                    registrar_locacao(cliente_id, midia_id, data_devolucao)
                except ValueError as e:
                    print(f"Erro de valor: {e}")
                except Exception as e:
                    print(f"Erro inesperado ao registrar locação: {e}")
            elif opcao == '4':
                consultar_midias()
            elif opcao == '5':
                consultar_clientes()
            elif opcao == '6':
                consultar_locacoes()
            elif opcao == '7':
                break
            else:
                print('Opção inválida. Tente novamente.')
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
