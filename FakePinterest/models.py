#Cria banco de dados
from FakePinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin     # classe que gerencia logins e senhas

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # função que busca id_usuario do banco de dados


class Usuario(database.Model, UserMixin): #database.Model é a superclasse criado pra todos que compõe o banco de dados

    id = database.Column(database.Integer,primary_key=True)
    username = database.Column(database.String,nullable=False)
    email = database.Column(database.String,nullable=False,unique=True)
    senha = database.Column(database.String,nullable=False)
    fotos = database.relationship("Foto",backref="usuario",lazy=True)



class Foto(database.Model):

    id = database.Column(database.Integer,primary_key=True)
    imagem = database.Column(database.String,default="default.png")
    data_criacao = database.Column(database.DateTime,nullable=False,default=datetime.utcnow())
    id_usuario = database.Column(database.Integer,database.ForeignKey("usuario.id"),nullable=False) # argumentos de posição sempre vem antes dos vermelhos



