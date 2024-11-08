from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError, DataError
import sys

# Criação do engine e da sessão
engine = create_engine('sqlite:///dados.db')
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


# Classe Funcionario herda de Pessoa
class Funcionario(Pessoa):
    __tablename__ = 'funcionarios'

    id = Column(Integer, ForeignKey('pessoas.id'), primary_key=True)
    

    def __repr__(self):
        return f'\n{"-" * 40}\nFuncionario:\nId = {self.id}\nNome = {self.nome}\nEndereço = {self.endereco}\nTelefone = {self.telefone}\n{"-" * 40}'


# Classe Midia
class Midia(Base):
    __tablename__ = 'midias'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    tipo = Column(String)  # Ex: Filme, Série, Documentário
    genero = Column(String)

    def __repr__(self):
        return f'\n{"-" * 40}\nMidia:\nID = {self.id}\nTitulo = {self.titulo}\nTipo = {self.tipo}\nGenero = {self.genero}\n{"-" * 40}'


# Classe Locacao
class Locacao(Base):
    __tablename__ = 'locacoes'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    midia_id = Column(Integer, ForeignKey('midias.id'))
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))  # Vincula a locação ao funcionário
    data_locacao = Column(DateTime, default=datetime.now)
    data_devolucao = Column(DateTime)

    cliente = relationship('Cliente', back_populates='locacoes')
    midia = relationship('Midia', back_populates='locacoes')
    funcionario = relationship('Funcionario', back_populates='locacoes')

    def __repr__(self):
        data_locacao = self.data_locacao.strftime('%d/%m/%Y') if self.data_locacao else 'Não informada'
        data_devolucao = self.data_devolucao.strftime('%d/%m/%Y') if self.data_devolucao else 'Não informada'
        return f'\n{"-" * 40}\nLocacao:\nCliente = {self.cliente.nome}\nMídia = {self.midia.titulo}\nFuncionario = {self.funcionario.nome}\nData Locação = {data_locacao}\nData Devolução = {data_devolucao}\n{"-" * 40}'

Cliente.locacoes = relationship('Locacao', back_populates='cliente')
Midia.locacoes = relationship('Locacao', back_populates='midia')
Funcionario.locacoes = relationship('Locacao', back_populates='funcionario')

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)

# Função para adicionar um cliente
def adicionar_cliente(nome, endereco, telefone, cpf):
    try:
        cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf)
        session.add(cliente)
        session.commit()
        print("Cliente adicionado com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (dados duplicados): {e}")
    except DataError as e:
        session.rollback()
        print(f"Erro de dados inválidos (tipo incompatível): {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao adicionar cliente: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar cliente: {e}")

# Função para consultar todos os clientes
def consultar_clientes():
    try:
        clientes = session.query(Cliente).all()
        if clientes:
            for cliente in clientes:
                print(cliente)
        else:
            print("Nenhum cliente encontrado.")
    except SQLAlchemyError as e:
        print(f"Erro ao consultar clientes: {e}")

# Função para adicionar um funcionário
def adicionar_funcionario(nome, endereco, telefone):
    try:
        funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone)
        session.add(funcionario)
        session.commit()
        print("Funcionário adicionado com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (dados duplicados): {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao adicionar funcionário: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar funcionário: {e}")

# Função para consultar todos os funcionários
def consultar_funcionarios():
    try:
        funcionarios = session.query(Funcionario).all()
        if funcionarios:
            for funcionario in funcionarios:
                print(funcionario)
        else:
            print("Nenhum funcionário encontrado.")
    except SQLAlchemyError as e:
        print(f"Erro ao consultar funcionários: {e}")

# Função para adicionar uma mídia
def adicionar_midia(titulo, tipo, genero):
    try:
        midia = Midia(titulo=titulo, tipo=tipo, genero=genero)
        session.add(midia)
        session.commit()
        print("Mídia adicionada com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"Erro de integridade (dados duplicados): {e}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro SQLAlchemy ao adicionar mídia: {e}")
    except Exception as e:
        session.rollback()
        print(f"Erro inesperado ao adicionar mídia: {e}")

# Função para consultar todas as mídias
def consultar_midias():
    try:
        midias = session.query(Midia).all()
        if midias:
            for midia in midias:
                print(midia)
        else:
            print("Nenhuma mídia encontrada.")
    except SQLAlchemyError as e:
        print(f"Erro ao consultar mídias: {e}")

# Função para registrar uma locação com funcionário
def registrar_locacao(cliente_id, midia_id, funcionario_id, data_devolucao):
    try:
        # Verificar se o cliente existe
        cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            print(f"Cliente com ID {cliente_id} não encontrado!")
            return
        
        # Verificar se a mídia existe
        midia = session.query(Midia).filter(Midia.id == midia_id).first()
        if not midia:
            print(f"Mídia com ID {midia_id} não encontrada!")
            return
        
        # Verificar se o funcionário existe
        funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
        if not funcionario:
            print(f"Funcionário com ID {funcionario_id} não encontrado!")
            return

        # Registrar a locação
        locacao = Locacao(cliente_id=cliente.id, midia_id=midia.id, funcionario_id=funcionario.id, data_devolucao=data_devolucao)
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

# Função para contar o número de locações de cada funcionário
def contar_locacoes_por_funcionario():
    try:
        funcionarios = session.query(Funcionario).all()
        if not funcionarios:
            print("Nenhum funcionário encontrado!")
            return
        for funcionario in funcionarios:
            num_locacoes = session.query(Locacao).filter(Locacao.funcionario_id == funcionario.id).count()
            print(f"{funcionario.nome} participou de {num_locacoes} locações.")
    except SQLAlchemyError as e:
        print(f"Erro ao contar locações por funcionário: {e}")

# Função para consultar todas as locações
def consultar_locacoes():
    try:
        locacoes = session.query(Locacao).all()
        if locacoes:
            for locacao in locacoes:
                print(locacao)
        else:
            print("Nenhuma locação encontrada.")
    except SQLAlchemyError as e:
        print(f"Erro ao consultar locações: {e}")

# Função principal com menu para o usuário
def main():
    while True:
        try:
            print('\nEscolha uma opção:')
            print('1. Adicionar Cliente')
            print('2. Adicionar Funcionario')
            print('3. Adicionar Mídia')
            print('4. Registrar Locação')
            print('5. Consultar Mídias')
            print('6. Consultar Clientes')
            print('7. Consultar Funcionários')
            print('8. Contar Locações por Funcionário')
            print('9. Consultar Locações')
            print('10. Sair')

            opcao = input('Opção: ')
            if opcao == '1':
                nome = input('Nome do Cliente: ')
                endereco = input('Endereço: ')
                telefone = input('Telefone: ')
                cpf = input('CPF: ')
                adicionar_cliente(nome, endereco, telefone, cpf)
            elif opcao == '2':  # Adicionar funcionário
                nome = input('Nome do Funcionário: ')
                endereco = input('Endereço: ')
                telefone = input('Telefone: ')
                adicionar_funcionario(nome, endereco, telefone)
            elif opcao == '3':
                titulo = input('Título da Mídia: ')
                tipo = input('Tipo (Filme/Série/Documentário): ')
                genero = input('Gênero: ')
                adicionar_midia(titulo, tipo, genero)
            elif opcao == '4':
                cliente_id = int(input('ID do Cliente: '))
                midia_id = int(input('ID da Mídia: '))
                funcionario_id = int(input('ID do Funcionário responsável pela locação: '))
                data_devolucao = input('Data de Devolução (DD/MM/YYYY): ')
                data_devolucao = datetime.strptime(data_devolucao, '%d/%m/%Y')
                registrar_locacao(cliente_id, midia_id, funcionario_id, data_devolucao)
            elif opcao == '5':
                consultar_midias()
            elif opcao == '6':
                consultar_clientes()
            elif opcao == '7':
                consultar_funcionarios()
            elif opcao == '8':  # Contar locações por funcionário
                contar_locacoes_por_funcionario()
            elif opcao == '9':
                consultar_locacoes()
            elif opcao == '10':
                break
            else:
                print('Opção inválida. Tente novamente.')
        except Exception as e:
            print(f"Erro inesperado: {e}")
            sys.exit(1)  # Sai do programa em caso de erro crítico.

if __name__ == "__main__":
    main()
