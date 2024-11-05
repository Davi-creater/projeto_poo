from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Criação do engine e da sessão
engine = create_engine('sqlite:///banco_dados.db', echo=True)
Base = declarative_base()



