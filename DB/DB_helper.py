from sqlalchemy import create_engine, Column, Integer, String,Boolean, ForeignKey,DateTime
from geoalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import datetime
#from DB_Names import *  (dont work in RestApi.py -->fix it)

Base = declarative_base()

NOME_BANCO = "LinkUpWomen"
TABELA_USUARIO = 'Usuarios'
TABELA_GRUPOS = 'Grupos'
TABELA_ALERTAS = 'Alertas'
TABELA_USUARIO_GRUPO = 'Usuario_grupo'
TABELA_LOCAL = 'Locais'

TABELA_USUARIO_ID = 'ID'
TABELA_USUARIO_CPF = 'CPF'
TABELA_USUARIO_LOGIN = 'Login'
TABELA_USUARIO_SENHA = 'Senha'
TABELA_USUARIO_NOME_COMPLETO = 'Nome_completo'
TABELA_USUARIO_EMAIL = 'Email'

TABELA_ALERTAS_ID = 'ID'
TABELA_ALERTAS_TITULO = 'Titulo'
TABELA_ALERTAS_DESCRICAO = 'Descricao'
TABELA_ALERTAS_DATA = 'Data'
TABELA_ALERTAS_LOCAL = 'Local'

TABELA_GRUPOS_ID = 'ID'
TABELA_GRUPOS_DATA_PARTIDA='Partida'
TABELA_GRUPOS_DONO_ID = 'ID_Dono'
TABELA_GRUPOS_LOCAL_DESTINO = 'Destino'
TABELA_GRUPOS_LOCAL_PARTIDA = 'Local_Partida'
TABELA_GRUPOS_DESCRICAO = 'Descricao'
TABELA_GRUPOS_QUANTIDADE = 'Quantidade'

TABELA_USUARIO_GRUPO_ID ='ID'
TABELA_USUARIO_GRUPO_ID_USUARIO = 'ID_Usuario'
TABELA_USUARIO_GRUPO_ID_GRUPO = 'ID_Grupo'

TABELA_LOCAL_ID = 'ID'
TABELA_LOCAL_NOME = 'Nome'
TABELA_LOCAL_LATITUDE = 'Latitude'
TABELA_LOCAL_LONGITUDE = 'Longitude'


class Local(Base):
    __tablename__= TABELA_LOCAL

    id= Column(TABELA_LOCAL_ID,Integer,primary_key=True)
    nome = Column(TABELA_LOCAL_NOME,String(255), nullable=False)
    latitude = Column(TABELA_LOCAL_LATITUDE,String(255), nullable=False)
    longitude = Column(TABELA_LOCAL_LONGITUDE,String(255), nullable=False)
    
class Usuario(Base):
    __tablename__= TABELA_USUARIO

    id= Column(TABELA_USUARIO_ID,Integer,primary_key=True)
    cpf = Column(TABELA_USUARIO_CPF, String(255),nullable=True)
    usuario = Column(TABELA_USUARIO_LOGIN,String(255), nullable=False)
    senha= Column(TABELA_USUARIO_SENHA, String(255), nullable= False)
    email = Column(TABELA_USUARIO_EMAIL,String(255),nullable=True)
    nome = Column(TABELA_USUARIO_NOME_COMPLETO,String(255), nullable=False)

class Alerta(Base):
    __tablename__= TABELA_ALERTAS

    id= Column(TABELA_ALERTAS_ID,Integer,primary_key=True)
    titulo = Column(TABELA_ALERTAS_TITULO, String(255),nullable=False)
    descricao = Column(TABELA_ALERTAS_DESCRICAO,String(255), nullable=False)
    local= Column(TABELA_ALERTAS_LOCAL, Integer,ForeignKey(Local.id), nullable= False)
    data = Column(TABELA_ALERTAS_DATA,DateTime,nullable=False)

class Grupo(Base):
    __tablename__= TABELA_GRUPOS

    id= Column(TABELA_GRUPOS_ID,Integer,primary_key=True)
    descricao = Column(TABELA_GRUPOS_DESCRICAO, String(255),nullable=False)
    dono = Column(TABELA_GRUPOS_DONO_ID,Integer,ForeignKey(Usuario.id), nullable=False)
    destino = Column(TABELA_GRUPOS_LOCAL_DESTINO, Integer,ForeignKey(Local.id), nullable= False)
    dataPartida = Column(TABELA_GRUPOS_DATA_PARTIDA,DateTime,nullable=False)
    localPartida= Column(TABELA_GRUPOS_LOCAL_PARTIDA, Integer,ForeignKey(Local.id), nullable= False)
    quantidade = Column(TABELA_GRUPOS_QUANTIDADE, Integer,nullable=True)

class UsuarioGrupo(Base):
    __tablename__= TABELA_USUARIO_GRUPO

    id= Column(TABELA_USUARIO_GRUPO_ID,Integer,primary_key=True)
    usuario = Column(TABELA_USUARIO_GRUPO_ID_USUARIO, Integer,ForeignKey(Usuario.id),nullable=False)
    grupo = Column(TABELA_USUARIO_GRUPO_ID_GRUPO,Integer,ForeignKey(Grupo.id), nullable=False)


def getEngine():

    user ="root"
    password=""
    adress="localhost"
    database_name="LinkUpWomen"
    engine = create_engine('mysql+pymysql://%s:%s@%s/%s'%(user, password, adress, database_name), echo=True)

    return engine

def INIT_API():
    engine = getEngine()
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)

def getSession():
    engine = getEngine()
    return sessionmaker(bind=engine)
	
	
def inserirUsuario(json_adress):

    Session = getSession()
    session=Session()
    usuario = Usuario()
    usuario.cpf=json_adress[TABELA_USUARIO_CPF]
    usuario.usuario =json_adress[TABELA_USUARIO_LOGIN]
    usuario.senha=json_adress[TABELA_USUARIO_SENHA]
    usuario.nome=json_adress[TABELA_USUARIO_NOME_COMPLETO]
    usuario.email=json_adress[TABELA_USUARIO_EMAIL]
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    id=usuario.id
    session.close()
    return id

def verificarUsuarioCadastrado(json):
    Session = getSession()
    session=Session()
    response=session.query(Usuario).filter(Usuario.usuario == json[TABELA_USUARIO_LOGIN]).all()
    if len(response)==1:
        r=response[0]
        return r.id
    else:
        return


def inserirAlerta(json_adress):
    Session = getSession()
    session=Session()
    alerta = Alerta()
    alerta.titulo=json_adress[TABELA_ALERTAS_TITULO]
    alerta.descricao =json_adress[TABELA_ALERTAS_DESCRICAO]
    alerta.data=datetime.strptime(json_adress[TABELA_ALERTAS_DATA],'%d-%m-%Y %H:%M')
    alerta.local=json_adress[TABELA_ALERTAS_LOCAL]
    session.add(alerta)
    session.commit()
    session.refresh(alerta)
    id=alerta.id
    session.close()
    return id

def inserirGrupo(json_adress):
    Session = getSession()
    session=Session()
    grupo = Grupo()
    grupo.descricao=json_adress[TABELA_GRUPOS_DESCRICAO]
    grupo.dono =json_adress[TABELA_GRUPOS_DONO_ID]
    grupo.dataPartida=datetime.strptime(json_adress[TABELA_GRUPOS_DATA_PARTIDA],'%d-%m-%Y %H:%M')
    grupo.destino=json_adress[TABELA_GRUPOS_LOCAL_DESTINO]
    grupo.localPartida=json_adress[TABELA_GRUPOS_LOCAL_PARTIDA]
    grupo.quantidade=json_adress[TABELA_GRUPOS_QUANTIDADE]
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    id=grupo.id
    session.close()
    return id

def getTodosGrupos():
    Session=getSession()
    session=Session()
    response=session.query(Grupo).all()
    result = {}
    counter=0
    for r in response:
        result[counter]={TABELA_GRUPOS_QUANTIDADE:r.quantidade,TABELA_GRUPOS_ID:r.id,TABELA_GRUPOS_DATA_PARTIDA:r.dataPartida,TABELA_GRUPOS_LOCAL_DESTINO:getLocal(r.destino),TABELA_GRUPOS_DONO_ID:r.dono,TABELA_GRUPOS_DESCRICAO:r.descricao,TABELA_GRUPOS_LOCAL_PARTIDA:getLocal(r.localPartida)}
        counter+=1
    print(result)
    return result

def getUsuario(json_company):
    login=json_company['Login']
    senha=json_company['Senha']
    Session=getSession()
    session=Session()
    response= session.query(Usuario).filter(Usuario.usuario == login , Usuario.senha==senha).all()
    if len(response)==1:
        c=response[0]
        dicCompany=1
        response= dicCompany
    else:
        response=False
    return response

def getLocal(id):
    Session = getSession()
    session=Session()
    response=session.query(Local).filter(Local.id == id).all()
    print(response[0].nome)
    return response[0].nome

def getLocal(nome):
    Session = getSession()
    session=Session()
    response=session.query(Local).filter(Local.nome == nome).all()
    return response[0].id
    


